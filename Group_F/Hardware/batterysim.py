import time
import json
import numpy as np
from scipy.interpolate import interp1d
import paho.mqtt.client as mqtt

BAT_CAPACITY = 45000 # mAh
MQTT_SERVER = "vpn.ce.pdn.ac.lk"
MQTT_PORT = 8883
MQTT_TOPIC = "326project/smartbuilding/pv"

pwm_duty = 0

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
        if self.SoC < 100:
            power_per_sec = self.charging_power / 60
            charge_in_kw = (self.SoC / 100) * self.battery_capacity
            charge_in_kw += power_per_sec
            self.SoC = charge_in_kw / self.battery_capacity * 100
            self.voc = self.voc_lookup["%.1f" % self.SoC]
            time.sleep(1)
        else:
            self.fully_charged = True

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
    print("Connected with result code " + str(rc))
    client.subscribe(topic=f"{MQTT_TOPIC}/pvVoltage", qos=2)

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code " + str(rc))

def on_message(client, userdata, message):
    print("Received message: " + message)
    global pwm_duty
    payload = json.loads(message.payload.decode("utf-8"))
    pwm_duty = payload["pwm_duty"]

if __name__ == '__main__':
    battery = Battery(BAT_CAPACITY, 0, 0)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_log = lambda client, userdata, level, buf: print("log: ", buf)
    client.connect(MQTT_SERVER, MQTT_PORT, 60)
    client.loop_start()
    while True:
        try:
            # Charging power is regulated by PWM duty cycle.
            battery.set_charging_power(pwm_duty * BAT_CAPACITY / 100)
            battery.charge()
            client.publish(f"{MQTT_TOPIC}/battery/voltage", json.dumps({ "time": time.time(), "value": battery.voc }))
            print(f"Battery voltage: {battery.voc}V, SoC: {battery.SoC}%")
        except KeyboardInterrupt:
            client.loop_stop()
            client.disconnect()
            break