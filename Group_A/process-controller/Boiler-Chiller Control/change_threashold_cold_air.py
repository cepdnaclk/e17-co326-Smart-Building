import paho.mqtt.client as mqtt
import json
import datetime
import random
import time


mqttBroker = "mqtt.eclipseprojects.io"
client = mqtt.Client("Cold Air Temperature Threashold  value changer")
# client.connect(mqttBroker)

topic = "326project/smartbuilding/hvac/change/temp-threash-coldair"

client.connect("vpn.ce.pdn.ac.lk", port=8883)
x = {
    "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
    "new-humid": random.uniform(20, 30)
}

client.publish(topic, json.dumps(x))
print("published " + str(x) + " to topic " + topic)




