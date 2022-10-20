from http import client
import pandas as pd
import paho.mqtt.client as mqtt
import time
import os

broker = "10.40.18.10"
port = 1883
topic_temp = "326project/smartbuilding/hvac/0/1/temperature"
topic_humid = "326project/smartbuilding/hvac/0/1/humidity"

# read csv file
df = pd.read_csv('KAG_energydata_complete.csv')
# print(df.head())

# extract data from columns T1 and RH_1
df1 = df[['T1', 'RH_1']]
# print(df1.head())

#check mqtt connection
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
        global Connected  # Use global variable
        Connected = True  # Signal connection
    else:
        print("Connection failed")

def on_message(client, userdata, message):
    print("Message received: " + message.topic + " " + str(message.payload))



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)

client.loop_start()

while True:
    # publish dummy data
    for i in range(len(df1)):
        # round up to 0 decimal places
        temp = round(df1['T1'][i], 0)
        humid = round(df1['RH_1'][i], 0)
        # publish data
        client.publish(topic_temp, temp)
        client.publish(topic_humid, humid)
        print("Published data: " + str(temp) + " " + str(humid))
        # wait for 1 second
        time.sleep(1)