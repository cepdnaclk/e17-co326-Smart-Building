# Battery output current sensor simulation
import paho.mqtt.client as mqtt
import json
import time
import csv
mqtt_server = "10.40.18.10"
mqtt_port = 1883

topic = "326project/smartbuilding/pv/battery/current"



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
    btrCurrentArray = [100,100,100,100,99,99,99,98,98,98,98,98,98,97,97,97,96,96,96,95]
    for c in btrCurrentArray:
      x = float(c)
    
      payload = json.dumps(x)
      client.publish(topic, payload=payload, qos=0, retain=False)
      print("Published current : ", payload)

      client.loop()
      time.sleep(2)
	


# client.loop_forever()
