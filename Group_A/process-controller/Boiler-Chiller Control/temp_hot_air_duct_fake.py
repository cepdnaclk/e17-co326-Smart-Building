import paho.mqtt.client as mqtt
import random
import time
import json
import datetime

mqttBroker = "vpn.ce.pdn.ac.lk"
client =mqtt.Client("Thermostat")
topic = "326project/smartbuilding/hvac/hotairduct/temperature"

while True:
    client.connect(mqttBroker, port=8883)
    x = {
        "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
        "temp": random.uniform(10, 20)
    }

    client.publish(topic, json.dumps(x))
    print("published " + str(x) + " to topic " + topic)
    time.sleep(5)

