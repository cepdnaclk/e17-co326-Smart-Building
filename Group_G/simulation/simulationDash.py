# You cana install dependencies using following command:
# pip install paho-mqtt

import paho.mqtt.client as mqtt
import json
import time
from random import seed
from random import randint
import datetime

mqtt_server = "127.0.0.1"
mqtt_port = 1883

#mosquitto_pub -h localhost -t smartbuilding/hvac/humid -m "{\"humidity\":6.4,\"timestamp\":20231230,\"floorno\":2,\"roomno\":4}"
topicb = "smartbuilding/hvac/control/boiler"
topicc = "smartbuilding/hvac/control/chiller"
topich = "smartbuilding/hvac/0/1/humid"
topic_arr_h = topich.split("/")
topict = "smartbuilding/hvac/0/1/temp"
topic_arr_t = topict.split("/")

topic_light = "smartbuilding/lighting/0/1"
topic_arr_light = topic_light.split("/")


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
        "state": randint(0,1),
        "timestamp": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    } 
    # time.time()
    y = {
        "state": randint(0,1),
        "timestamp": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    }
    hum = {
        "humidity": randint(0,10),
        "floorno": topic_arr_h[2], # randint(0,2),
        "roomno": topic_arr_h[3], #randint(0,10),
		"timestamp": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
	}
    tem = {
        "temperature": randint(15,35),
        "floorno": topic_arr_t[2], # randint(0,2),
        "roomno": topic_arr_t[3], #randint(0,10),
		"timestamp": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
	}
    light = {
        "lightlevel": randint(0,100),
        "floorno": topic_arr_light[2], # randint(0,2),
        "roomno": topic_arr_light[3], #randint(0,10),
        "timestamp": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
    }

    payload = json.dumps(light)
    client.publish(topic_light, payload=payload, qos=0, retain=False)
    payload = json.dumps(hum)
    client.publish(topich, payload=payload, qos=0, retain=False)
    payload = json.dumps(tem)
    client.publish(topict, payload=payload, qos=0, retain=False)
    payload = json.dumps(x)
    client.publish(topicb, payload=payload, qos=0, retain=False)
    time.sleep(randint(0, 2))
    payload = json.dumps(y)
    client.publish(topicc, payload=payload, qos=0, retain=False)
    print("Published", payload)

    client.loop()
    time.sleep(randint(0, 2))

	


# client.loop_forever()
