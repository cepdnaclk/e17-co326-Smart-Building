import paho.mqtt.client as mqtt
import json
from time import asctime, time, sleep
from math import exp
from sys import argv

# Pressure Model
target_pressure = lambda speed : 0.012 * speed

def pressure_model(speed, pressure, t):
    target = target_pressure(speed)

    return target + (pressure - target) * exp(-t / 10)


# Initialize start time
start_time = time()
speed = 0
pressure = 1

floorno = argv[1]
roomno = argv[2]

# MQTT info
broker_addr = "10.40.18.10"
broker_port = 1883
ahu_topic = f"326project/smartbuilding/hvac/{floorno}/{roomno}/control/ahu"
room_pressure_topic = f"326project/smartbuilding/hvac/{floorno}/{roomno}/pressure"


# Get duct temps and AHU data via MQTT
def on_message(client, userdata, message):
    global speed, start_time

    # Store prev values
    old_speed = speed

    # Update values based on MQTT data
    if message.topic == ahu_topic:
        data = json.loads(message.payload.decode("utf-8"))
        speed = data['speed']
        #print(f"AHU: {speed}, {ratio}")

    # Update elapsed time on change of values
    if (speed != old_speed):
        start_time = time()
    

# Create MQTT client instance and connect to broker
client = mqtt.Client("Room0Pressure")
client.connect(broker_addr, broker_port)
print("Connected to broker")

# Subscribe to relevant topic
client.subscribe(ahu_topic)
print(f"Subscribed to {ahu_topic}")

# Listen for messages
client.on_message = on_message
client.loop_start()


# Publish sensor readings
while True:
    elapsed_time = time() - start_time

    # Update temp value
    pressure = pressure_model(speed, pressure, elapsed_time)

    # Publish to MQTT topic
    data = json.dumps({"time": asctime(), "pressure": round(pressure, 2)})
    client.publish(room_pressure_topic, data)

    print(round(pressure,2))
    sleep(1)


# Never runs but added for safety
client.loop_stop()
