import csv
import paho.mqtt.client as mqtt
import json
from time import asctime, time, sleep
from math import exp


# MQTT info
broker_addr = "10.40.10.18"
broker_port = 1883
topic_smoke = "esp32/smoke"
topic_temp = "esp32/temp"


def on_publish(client, userdata, result):  # create function for callback
    print("data published \n")
    pass


# Create MQTT client instance and connect to broker
client = mqtt.Client("esp32")
client.on_publish = on_publish
client.connect(broker_addr, broker_port)
print("Connected to broker")


# # Listen for messages
# client.on_message = on_message
# client.loop_start()
count = 1
smokeReadings = []  # smokesensor readings
tempReadings = []  # temp readings
with open("model.csv", 'r') as file:
    csvreader = csv.DictReader(file)

    for row in csvreader:
        #         print(row['readings'])
        i = row['gas']
        smokeReadings.append(i)
        j = row['temp']
        tempReadings.append(j)
        # count = count + 1
        # if (count >= 50):  # size of count
        #     break

#  print(rows)

for k in range(0, len(smokeReadings)):
    smoke = {
        "time": asctime(),
        "smoke_Reading": smokeReadings[k]
    }
    payload_smoke = json.dumps(smoke)
    client.publish(topic_smoke, payload=payload_smoke, qos=0, retain=False)
    sleep(1)
    temp = {
        "time": asctime(),
        "temperature": tempReadings[k]

    }
    payload_temp = json.dumps(temp)
    client.publish(topic_temp, payload_temp, qos=0, retain=False)
    sleep(1)
