from multiprocessing.spawn import old_main_modules
import paho.mqtt.client as mqtt
import json
from time import asctime, time, sleep
from math import exp
import csv


# Boiler On-Model
on_vals = []

with open('boiler-model.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    for row in csvreader:
        on_vals.append(float(row[1]))

def on_model(temp):
    closest_index = min(range(len(on_vals)), key=lambda i: abs(on_vals[i]-temp))

    return on_vals[closest_index+1]


# Boiler Off Model
off_model = lambda temp, t : 30 + (temp - 30)*exp(-t/120000)


# Initial values
min_temp = 30.0    # Room temp
max_temp = 88.0   # Boiler max temp
temp = min_temp
state = False

# Initialize start time
start_time = time()


# MQTT info
broker_addr = "10.40.18.10"
broker_port = 1883
boiler_topic = "326project/smartbuilding/hvac/control/boiler"
sensor_topic = "326project/smartbuilding/hvac/hotairduct/temperature"

# Get boiler state via MQTT
def on_message(client, userdata, message):
    global state, start_time

    old_state = state

    data = json.loads(message.payload.decode("utf-8"))

    # Update state and start time
    state = True if data['state'] == 1 else False

    if state != old_state:
        print(f"Boiler {'ON' if state is True else 'OFF' }")
        start_time = time()


# Create MQTT client instance and connect to broker
client = mqtt.Client("BoilerDuctTemp")
client.connect(broker_addr, broker_port)
print("Connected to broker")

# Subscribe to relevant topic
client.subscribe(boiler_topic)
print(f"Subscribed to {boiler_topic}")

# Listen for messages
client.on_message = on_message
client.loop_start()


# Publish sensor readings
while True:
    elapsed_time = time() - start_time

    # Update temp value
    match state:
        case True:
            temp = on_model(temp) if temp < max_temp else max_temp

        case False:
            # Keep temperature rising for some time after actuator shuts down
            if elapsed_time < 10:
                temp = on_model(temp) if temp < max_temp else max_temp
            else:
                temp = off_model(temp, elapsed_time) if temp > min_temp else min_temp

    # Publish to MQTT topic
    data = json.dumps({"time": asctime(), "temp": round(temp, 2)})
    client.publish(sensor_topic, data)

    print(round(temp,2))
    sleep(1)


# Never runs but added for safety
client.loop_stop()
