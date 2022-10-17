import paho.mqtt.client as paho

broker="10.40.18.10"
port= 8883

def on_publish(client,userdata, result):
    print("data pubilished \n")

client1 = paho.Client("control1")
client1.on_publish = on_publish
client1.connect(broker, port)
ret = client1.publish("co326/test/publish","test")
