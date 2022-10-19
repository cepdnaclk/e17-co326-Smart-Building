import paho.mqtt.client as mqtt
import random
import time
import json
import datetime

mqttBroker = "mqtt.eclipseprojects.io"
client =mqtt.Client("Thermostat")
# client.connect(mqttBroker)

topic = "326project/smartbuilding/hvac/sensor/humidity/floorX/roomX"

while True:
    client.connect("vpn.ce.pdn.ac.lk", port=8883)
    x = {
        "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
        "humid": random.uniform(0, 100)
    }
    client.publish(topic, json.dumps(x))
    print("published " + str(x) + " to topic " + topic)
    time.sleep(5)

