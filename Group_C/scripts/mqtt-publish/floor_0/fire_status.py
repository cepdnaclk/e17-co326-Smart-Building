#publishes temperature data periodically

import paho.mqtt.client as mqtt
import json
import time

mqtt_server = "10.40.18.10"
mqtt_port = 1883

topic_fire = "326project/smartbuilding/safety/0/3/fire"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	payload = str(msg.payload, 'utf-8')
	print("Received: ", msg.topic)
	print("\t", json.dumps(payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
time.sleep(2)
client.loop()

client.connect(mqtt_server, port=mqtt_port, keepalive=60)

# client.subscribe(topic_sub, qos=0)
# print("MQTT Data generator is started...")

while(1):
	#publish fire status
	fire = {
            "time":"test_time",
            "state": "Fire"
        }

	payload_fire = json.dumps(fire)
	client.publish(topic_fire, payload=payload_fire, qos=0, retain=False)
	print("Published", payload_fire)



	client.loop()
	time.sleep(2)

	


# client.loop_forever()
