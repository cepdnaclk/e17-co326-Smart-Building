# You cana install dependencies using following command:
# pip install paho-mqtt

import paho.mqtt.client as mqtt
import json
import time
from random import seed
from random import randint
import datetime

mqtt_server = "172.17.0.11"
mqtt_port = 8883

#mosquitto_pub -h localhost -t smartbuilding/hvac/humid -m "{\"humidity\":6.4,\"timestamp\":20231230,\"floorno\":2,\"roomno\":4}"
topic = "326project/smartbuilding/sensor/temp"
topic_sub = ""


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	payload = str(msg.payload, 'utf-8')
	print("Received: ", msg.topic)
	print("\t", json.dumps(payload))

seed(1)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
time.sleep(2)
client.loop()

client.connect(mqtt_server, port=mqtt_port, keepalive=60)

# client.subscribe(topic_sub, qos=0)
print("MQTT Data generator is started...")

while(1):
	# Upload the data in 'x' variable continuously with 2 second interval 
	x = {
        "humidity": randint(0,10),
        "floorno": randint(0,2),
        "roomno": randint(0,10),
		"timestamp": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
	} 
    # time.time()

	payload = json.dumps(x)
	client.publish(topic, payload=payload, qos=0, retain=False)
	print("Published", payload)

	client.loop()
	time.sleep(2)

	


# client.loop_forever()
