import paho.mqtt.client as mqtt
import json
from time import asctime, time, sleep
from math import exp
from sys import argv

# ambient temprature Model


def temprature_model(temp_low, temp_high, time):
    return temp_low + ((temp_high - temp_low) / (temp_high)) * time * exp(
        -1 * round(time / 100, 2)
    )


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


# Initialize start time
start_time = time()


floorno = argv[1]
roomno = argv[2]

# MQTT info
broker_addr = "10.40.18.10"
broker_port = 1883
ambient_topic = "326project/smartbuilding/hvac/ambient_temperature"


# Create MQTT client instance and connect to broker
client = mqtt.Client(f"Floor{floorno}Room{roomno}Temp")
client.connect(broker_addr, broker_port)
print("Connected to broker")


client.on_message = on_message


# Subscribe to relevant topics
client.subscribe(ambient_topic)
print(f"Subscribed to {ambient_topic}")


# Publish sensor readings
while True:
    elapsed_time = time() - start_time
    # Update temp value
    temp = temprature_model(25, 28, elapsed_time)

    # Publish to MQTT topic
    data = json.dumps({"time": asctime(), "amb_temprature": round(temp, 2)})
    print(client.publish(ambient_topic, data))
    print(round(temp, 2))
    sleep(1)

    if elapsed_time > 180:
        break


# Never runs but added for safety
client.loop_stop()
