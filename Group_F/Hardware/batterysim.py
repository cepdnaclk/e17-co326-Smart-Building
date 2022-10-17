from pydoc import cli
import time
import json
import threading
import numpy as np
from scipy.interpolate import interp1d
import paho.mqtt.client as mqtt

BAT_CAPACITY = 65000 # mAh
MQTT_SERVER = "10.40.18.10"
MQTT_PORT = 1883
MQTT_TOPIC = "326project/smartbuilding/pv"

c = threading.Condition()
c1 = threading.Condition()
c2 = threading.Condition()
c3 = threading.Condition()
pwm_duty = 0
loading = False
ready = False

"""
    This module simulates a battery and publishes the battery voltage to the MQTT server.

    NOTE: A second in real-time is a minute in simulated time.
"""
class Battery(object):
    def __init__(self, battery_capacity, SoC, charging_power):
        self.battery_capacity = battery_capacity
        self.SoC = SoC
        self.charging_power = charging_power
        # Source: https://footprinthero.com/lead-acid-battery-voltage-charts
        voc = [11.63, 11.7, 11.81, 11.96, 12.11, 12.23, 12.41, 12.51, 12.65, 12.78, 12.89]
        soc = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        f = interp1d(soc, voc, kind='cubic')
        soc = np.arange(0, 100, 0.1)
        voc = f(soc)
        self.voc_lookup = {"%.1f" % k: v for k, v in zip(soc, voc)}
        self.voc = self.voc_lookup["%.1f" % self.SoC]
        self.fully_charged = False

    def charge(self):
        power_per_min = self.charging_power / 60
        charge_in_kw = (self.SoC / 100) * self.battery_capacity
        charge_in_kw += power_per_min
        soc = charge_in_kw / self.battery_capacity * 100
        if soc < 100:
            self.SoC = soc
            self.voc = self.voc_lookup["%.1f" % self.SoC]
        elif round(soc) - 100 <= 1 and not self.fully_charged:
            self.SoC = 100
            # self.voc = self.voc_lookup["%.1f" % soc]
            self.fully_charged = True
        time.sleep(1)

    # Assumption: the relationship between SoC vs Voltage is the same in both charging and discharging.
    # Ignore internal resistance.
    def load(self, load):
        if self.SoC > 0:
            power_per_min = load / 60
            charge_in_kw = (self.SoC / 100) * self.battery_capacity
            charge_in_kw -= power_per_min
            self.SoC = charge_in_kw / self.battery_capacity * 100
            self.voc = self.voc_lookup["%.1f" % self.SoC]
            self.fully_charged = False
            time.sleep(1)

    def set_charging_power(self, charging_power):
        self.charging_power = charging_power

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Client " + client._client_id.decode() + " connected to MQTT server.", "with result code " + str(rc))
    else:
        print("Connection failed with result code " + str(rc))

def on_disconnect(client, userdata, rc):
    print("Client " + client._client_id.decode() + " disconnected from MQTT server.")

battery = Battery(BAT_CAPACITY, 0, 0)

if __name__ == '__main__':
    clients = []

    def sample_load():
        global loading, ready, battery
        while True:
            c1.acquire()
            if not loading:
                c1.release()
                continue
            print("Battery loading...")
            c1.release()
            c3.acquire()
            # 20 kWh load
            battery.load(20000)
            soc = battery.SoC
            c3.release()
            c2.acquire()
            if soc < 60 and ready:
                ready = False
            c2.release()

    def subscribing_sw1():
        client = mqtt.Client("Battery Simulator - SW1")
        client.connect(MQTT_SERVER, MQTT_PORT, 60)
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        def on_message(client, userdata, message):
            global pwm_duty
            payload = json.loads(message.payload.decode("utf-8"))
            pwm = payload["pwm_duty"]
            c.acquire()
            if pwm_duty != pwm:
                pwm_duty = pwm
            c.release()
        client.message_callback_add(f"{MQTT_TOPIC}/controls/sw1", on_message)
        client.loop_start()
        client.subscribe(topic=f"{MQTT_TOPIC}/controls/sw1", qos=2)
        clients.append(client)

    def subscribing_sw2():
        client = mqtt.Client("Battery Simulator - SW2")
        client.connect(MQTT_SERVER, MQTT_PORT, 60)
        client.on_connect = on_connect
        client.on_disconnect = on_disconnect
        def on_message(client, userdata, message):
            global loading
            payload = json.loads(message.payload.decode("utf-8"))
            c1.acquire()
            if payload["sw2"] == "ON" and not loading:
                loading = True
                time.sleep(1)
                print("Load thread started")
                time.sleep(1)
            elif payload["sw2"] == "OFF" and loading:
                loading = False
                print("Load thread stopped")
            c1.release()
        client.message_callback_add(f"{MQTT_TOPIC}/controls/sw2", on_message)
        client.loop_start()
        client.subscribe(topic=f"{MQTT_TOPIC}/controls/sw2", qos=2)
        clients.append(client)

    load_thread = threading.Thread(target=sample_load)
    subscribing_sw1_thread = threading.Thread(target=subscribing_sw1)
    subscribing_sw2_thread = threading.Thread(target=subscribing_sw2)

    load_thread.start()
    time.sleep(1)
    subscribing_sw1_thread.start()
    time.sleep(1)
    subscribing_sw2_thread.start()
    time.sleep(1)

    client = mqtt.Client("Battery Simulator - Battery")
    client.connect(MQTT_SERVER, MQTT_PORT, 60)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.loop_start()
    while True:
        try:
            # Charging power is regulated by PWM duty cycle.
            c.acquire()
            c3.acquire()
            battery.set_charging_power(pwm_duty * BAT_CAPACITY / 100)
            battery.charge()
            soc, voc = battery.SoC, battery.voc
            c3.release()
            client.publish(f"{MQTT_TOPIC}/battery/voltage", json.dumps({ "time": time.time(), "value": voc }))
            print(f"pwm duty: {pwm_duty}, SoC: {soc}%, Voc: {voc}V")
            c.release()
            c2.acquire()
            if soc >= 60 and not ready:
                ready = True
                client.publish(f"{MQTT_TOPIC}/battery/ready", json.dumps({ "time": time.time(), "value": True }))
            c2.release()
        except KeyboardInterrupt:
            client.loop_stop()
            client.disconnect()
            for client in clients:
                client.loop_stop()
                client.disconnect()
            break

    load_thread.join()
    subscribing_sw1_thread.join()
    subscribing_sw2_thread.join()
