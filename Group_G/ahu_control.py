import paho.mqtt.client as mqtt
import json
from time import asctime, time, sleep
from math import log
from sys import argv

start_time = time()

floorno = argv[1]
roomno = argv[2]

# MQTT info
broker_addr = "10.40.18.10"
broker_port = 1883

ahu_topic = f"326project/smartbuilding/hvac/{floorno}/{roomno}/control/ahu"
room_temp_topic = f"326project/smartbuilding/hvac/{floorno}/{roomno}/temperature"
occupant_topic = f"326project/smartbuilding/occupancy/{floorno}/{roomno}/occupants"
amb_temp = "326project/smartbuilding/hvac/ambient_temperature"

# Get duct temps and AHU data via MQTT
def on_message(client, userdata, message):
    global start_time, occupant_r, temp, amb_temprature

    # Store prev values
    old_temp = temp
    old_amb_temprature = amb_temprature
    old_occupant_r = occupant_r

    # Update values based on MQTT data
    if message.topic == room_temp_topic:
        data = json.loads(message.payload.decode("utf-8"))
        temp = data["temp"]
        # print(f"Chiller: {chiller_temp}")

    elif message.topic == occupant_topic:
        data = json.loads(message.payload.decode("utf-8"))
        occupant_r = data["occupants"] / 31

    else:
        data = json.loads(message.payload.decode("utf-8"))
        amb_temprature = data["amb_temprature"]
        # print(f"AHU: {speed}, {ratio}")

    # Update elapsed time on change of values
    if (
        (temp != old_temp)
        or (amb_temprature != old_amb_temprature)
        or (occupant_r != old_occupant_r)
    ):
        start_time = time()


# Create MQTT client instance and connect to broker
client = mqtt.Client(f"Floor{floorno}Room{roomno}Temp")
client.connect(broker_addr, broker_port)
print("Connected to broker")

# Subscribe to relevant topics
client.subscribe(ahu_topic)
print(f"Subscribed to {ahu_topic}")

client.subscribe(room_temp_topic)
print(f"Subscribed to {room_temp_topic}")

client.subscribe(occupant_topic)
print(f"Subscribed to {occupant_topic}")

client.subscribe(amb_temp)
print(f"Subscribed to {amb_temp}")

# Listen for messages
client.on_message = on_message
client.loop_start()

temp = 30
amb_temprature = 30
occupant_r = 0

# Publish sensor readings
while True:
    elapsed_time = time() / 1000 - start_time / 1000

    # Update temp value
    temp = temp + occupant_r * log(elapsed_time)

    # Publish to MQTT topic
    data = json.dumps({"time": asctime(), "temp": round(temp, 2)})
    client.publish(room_temp_topic, data)

    print(round(temp, 2))
    sleep(1)


# Never runs but added for safety
client.loop_stop()
