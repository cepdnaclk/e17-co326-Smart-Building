try:
    import paho.mqtt.client as mqtt 
except:
    import pip
    pip.main(['install','paho-mqtt'])

# Imports 
import time
import paho.mqtt.client as mqtt 

topic = "G1A/CDR/DATA"
mqttBroker = "vpn.ce.pdn.ac.lk" #Must be connected to the vpn
mqttPort = 8883

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode("utf-8")))

client = mqtt.Client("G1A") #Group 1A (Classified Document Room)


try:
    client.connect(mqttBroker,mqttPort) 
    client.on_connect = on_connect
    client.on_message = on_message
    client.loop_forever()
except:
    print("Connection to MQTT broker failed!")
    exit(1)
