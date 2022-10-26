# PV cell voltage sensor simulation
import paho.mqtt.client as mqtt
import json
import time
import csv
mqtt_server = "10.40.18.10"
mqtt_port = 1883

topic = "326project/smartbuilding/pv/pvVoltage"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

client = mqtt.Client()
client.on_connect = on_connect
time.sleep(2)
client.connect(mqtt_server, port=mqtt_port, keepalive=60)
client.loop_start()

#client.subscribe(topic_sub, qos=0)
print("MQTT Data generator is started...")

# max voltage output 31.6v
csvreader = list(csv.reader(open("..\\..\\Data\\simulation_data\\Plant_2_Time_vs_DCPower_Data.csv", 'r')))
while(1):
	try:
		for row in csvreader:
			print(row[0])
			x = float(row[0])
			x = int((x/15000) * 31.6)
			payload = json.dumps({ "time": time.time(), "value": x })
			client.publish(topic, payload=payload, qos=0, retain=False)
			print("Published", payload)
			time.sleep(1)
	except KeyboardInterrupt:
		csvreader.close()
		client.loop_stop()
		client.disconnect()
		break
