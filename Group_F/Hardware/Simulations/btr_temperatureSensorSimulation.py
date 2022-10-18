# Battery Temperature sensor simulation
import paho.mqtt.client as mqtt
import json
import time


mqtt_server = "10.40.18.10"
mqtt_port = 1883

topic = "326project/smartbuilding/pv/battery/temperature"



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


while(1):
    tempArray = [ 40,45.2,40.1,40.1,40.1,42.0,41.2,46,45,42,40.6]
    for temp in tempArray:
      print(temp)
      x = temp
      
      
      
      payload = json.dumps(x)
      client.publish(topic, payload=payload, qos=0, retain=False)
      print("Published temperature : ", payload)

      client.loop()
      time.sleep(2)
	


# client.loop_forever()
