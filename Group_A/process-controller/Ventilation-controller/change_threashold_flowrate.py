import paho.mqtt.client as mqtt
import json
import datetime
import random
import time


client = mqtt.Client("Threashold flowrate value changer")
# client.connect(mqttBroker)

topic = "326project/smartbuilding/hvac/change/flowrate-threash"

client.connect("10.40.18.10", port=1883)
x = {
    "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
    "new-flowrate": random.uniform(0, 100)
}

client.publish(topic, json.dumps(x))
print("published " + str(x) + " to topic " + topic)




