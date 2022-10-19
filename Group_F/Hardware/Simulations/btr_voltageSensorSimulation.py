## Batter output voltage sensor simulation
import paho.mqtt.client as mqtt
import json
import time

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
    btrVoltageArray = [200,200,200,200,200,200,199,199,199,198,198] 
    for v in btrVoltageArray:
      x = float(v)
    
      payload = json.dumps(x)
      client.publish(topic, payload=payload, qos=0, retain=False)
      print("Published voltage : ", payload)

      client.loop()
      time.sleep(2)
	


# client.loop_forever()
