#publishes temperature data periodically

import paho.mqtt.client as mqtt
import json
import time
import random

mqtt_server = "10.40.18.10"
mqtt_port = 1883

topic_temp = "326project/smartbuilding/hvac/0/0/temperature"
topic_humid = "326project/smartbuilding/hvac/0/0/humidity"
topic_pressure = "326project/smartbuilding/hvac/0/0/pressure"
topic_fireAlarm = "326project/smartbuilding/safety/0/0/firealarm"
# topic_sub = "co326/test/subscribe"


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
	# Upload the data in 'x' variable continuously with 2 second interval 
	temp = {
            "time":"test_time",
            "temp":random.randint(20,40)
        }

	payload_temp = json.dumps(temp)
	client.publish(topic_temp, payload=payload_temp, qos=0, retain=False)
	print("Published", payload_temp)

	#publish humidity
	humidity = {
            "time":"test_time",
            "humid":random.randint(20,80)
        }

	payload_humid = json.dumps(humidity)
	client.publish(topic_humid, payload=payload_humid, qos=0, retain=False)
	print("Published", payload_humid)

	#publish pressure
	pressure = {
            "time":"test_time",
            "pressure":random.randint(0,10)
        }

	payload_pressure = json.dumps(pressure)
	client.publish(topic_pressure, payload=payload_pressure, qos=0, retain=False)
	print("Published", payload_pressure)


	#publish fireAlarm status
	fireAlarm = {
            "time":"test_time",
            "state": random.randint(0,1)
        }

	payload_fireAlarm = json.dumps(fireAlarm)
	client.publish(topic_fireAlarm, payload=payload_fireAlarm, qos=0, retain=False)
	print("Published", payload_fireAlarm)

	client.loop()
	time.sleep(2)

	


# client.loop_forever()
