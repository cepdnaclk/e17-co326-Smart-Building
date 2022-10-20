import paho.mqtt.client as mqtt
import json
import datetime
import random
import time


mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("Threashold temp value changer")
# client.connect(mqttBroker)

topic = "326project/smartbuilding/hvac/change/temp-threash"

client.connect("vpn.ce.pdn.ac.lk", port=8883)
x = {
    "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
    "new-temp": random.uniform(0, 100)
}

client.publish(topic, json.dumps(x))
print("published " + str(x) + " to topic " + topic)




