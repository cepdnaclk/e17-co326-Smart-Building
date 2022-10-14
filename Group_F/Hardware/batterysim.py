from pydoc import cli
import time
import json
import threading
import numpy as np
from scipy.interpolate import interp1d
import paho.mqtt.client as mqtt

BAT_CAPACITY = 45000 # mAh
MQTT_SERVER = "10.40.18.10"
MQTT_PORT = 1883
MQTT_TOPIC = "326project/smartbuilding/pv"

c = threading.Condition()
c1 = threading.Condition()
pwm_duty, prev_pwm_duty = 0, -1
loading = False

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
        power_per_sec = self.charging_power / 60
        charge_in_kw = (self.SoC / 100) * self.battery_capacity
        charge_in_kw += power_per_sec
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
            power_per_sec = load / 60
            charge_in_kw = (self.SoC / 100) * self.battery_capacity
            charge_in_kw -= power_per_sec
            self.SoC = charge_in_kw / self.battery_capacity * 100
            self.voc = self.voc_lookup["%.1f" % self.SoC]
            self.fully_charged = False
            time.sleep(1)

    def set_charging_power(self, charging_power):
        self.charging_power = charging_power

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT server with result code " + str(rc))
        client.subscribe(topic=f"{MQTT_TOPIC}/controls/sw1", qos=2)
    else:
        print("Connection failed with result code " + str(rc))

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code " + str(rc))

if __name__ == '__main__':
    battery = Battery(BAT_CAPACITY, 0, 0)
    client = mqtt.Client("Battery Simulator")
    client.connect(MQTT_SERVER, MQTT_PORT, 60)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_log = lambda client, userdata, level, buf: print("log: ", buf)

    def sample_load():
        global loading
        while True:
            c1.acquire()
            if not loading:
                c1.release()
                continue
            c1.release()
            battery.load(1000)
            client.publish(topic=f"{MQTT_TOPIC}/sensors/voltage", payload=json.dumps({"voltage": battery.voc}), qos=2)
            time.sleep(2)
            c1.acquire()

    def subscribing_sw1():
        def on_message(client, userdata, message):
            global pwm_duty
            print("Received message: " + str(message.payload.decode("utf-8")))
            payload = json.loads(message.payload.decode("utf-8"))
            c.acquire()
            if prev_pwm_duty != payload["pwm_duty"]:
                pwm_duty = payload["pwm_duty"]
                c.notify_all()
            else:
                c.wait()
            c.release()
        client.message_callback_add(f"{MQTT_TOPIC}/controls/sw1", on_message)
        
    def subscribing_sw2():
        def on_message(client, userdata, message):
            global loading
            payload = json.loads(message.payload.decode("utf-8"))
            if payload["sw2"] == "ON":
                c1.acquire()
                if not loading:
                    loading = True
                    print("Load thread started")
                    c.notify_all()
                else:
                    c1.wait()
                c1.release()
            else:
                c1.acquire()
                if loading:
                    loading = False
                    print("Load thread stopped")
                    c.notify_all()
                else:
                    c1.wait()
                c1.release()
        client.message_callback_add(f"{MQTT_TOPIC}/controls/sw2", on_message)

    def publishing():
        while True:
            try:
                # Charging power is regulated by PWM duty cycle.
                c.acquire()
                battery.set_charging_power(pwm_duty * BAT_CAPACITY / 100)
                battery.charge()
                client.publish(f"{MQTT_TOPIC}/battery/voltage", json.dumps({ "time": time.time(), "value": battery.voc }))
                print(f"pwm duty: {pwm_duty}, SoC: {battery.SoC}%, Voc: {battery.voc}V")
                c.wait()
                c.release()
                if battery.SoC >= 60:
                    client.publish(f"{MQTT_TOPIC}/battery/ready", json.dumps({ "time": time.time(), "value": True }))
            except KeyboardInterrupt:
                client.loop_stop()
                client.disconnect()
                break

    load_thread = threading.Thread(target=sample_load)
    subscribing_sw1_thread = threading.Thread(target=subscribing_sw1)
    subscribing_sw2_thread = threading.Thread(target=subscribing_sw2)
    publishing_thread = threading.Thread(target=publishing)

    load_thread.start()
    subscribing_sw1_thread.start()
    subscribing_sw2_thread.start()
    publishing_thread.start()
