# You cana install dependencies using following command:
# pip install paho-mqtt

import paho.mqtt.client as mqtt
import json
import time
import csv
mqtt_server = "10.40.18.10"
mqtt_port = 1883

topic = "326project/smartbuilding/pv/battery/voltage"



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    

client = mqtt.Client()
client.on_connect = on_connect
time.sleep(2)
client.loop()

client.connect(mqtt_server, port=mqtt_port, keepalive=60)

#client.subscribe(topic_sub, qos=0)
print("MQTT Data generator is started...")


#275wattp, 31.6v
while(1):

  with open("..\\Data\\simulation_data\\Plant_2_Time_vs_DCPower_Data.csv", 'r') as file:
    csvreader = csv.reader(file)
    for row in csvreader:
      print(row[0])
      x = float(row[0])
      x = int((x/15000)* 31.6) 
      
      
      payload = json.dumps(x)
      client.publish(topic, payload=payload, qos=0, retain=False)
      print("Published", payload)

      client.loop()
      time.sleep(2)
	


# client.loop_forever()
