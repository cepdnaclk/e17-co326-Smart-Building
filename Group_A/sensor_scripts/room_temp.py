import paho.mqtt.client as mqtt
import json
from time import asctime, time, sleep
from math import exp


# AHU Model
target_temp = lambda r, Tb, Tc : r * Tb  +  (1-r) * Tc

def ahu_model(speed, temp, r, Tb, Tc, t):
    target = target_temp(r, Tb, Tc)

    return target + (temp - target)*exp(-t/ (4000*speed))


# Initialize start time
start_time = time()
boiler_temp = 30
chiller_temp = 30
ratio = 0
speed = 0
temp = 30
# humidity = 0


# MQTT info
broker_addr = "10.40.18.10"
broker_port = 1883
chiller_temp_topic = "326project/smartbuilding/hvac/sensor/chiller"
boiler_temp_topic = "326project/smartbuilding/hvac/sensor/boiler"
ahu_topic = "326project/smartbuilding/hvac/actuator/ahu/0/1"
room_temp_topic = "326project/smartbuilding/hvac/temperature/room1"
room_humidity_topic = "326project/smartbuilding/hvac/humidity/room1"


# Get duct temps and AHU data via MQTT
def on_message(client, userdata, message):
    global boiler_temp, chiller_temp, ratio, speed, start_time

    # Store prev values
    old_boiler_temp = boiler_temp
    old_chiller_temp = chiller_temp
    old_ratio = ratio
    old_speed = speed

    # Update values based on MQTT data
    if message.topic == chiller_temp_topic:
        data = json.loads(message.payload.decode("utf-8"))
        chiller_temp = data['temp']
        #print(f"Chiller: {chiller_temp}")

    elif message.topic == boiler_temp_topic:
        data = json.loads(message.payload.decode("utf-8"))
        boiler_temp = data['temp']
        #print(f"Boiler: {boiler_temp}")

    else:
        data = json.loads(message.payload.decode("utf-8"))
        speed = data['speed']
        ratio = data['ratio']
        #print(f"AHU: {speed}, {ratio}")

    # Update elapsed time on change of values
    if (boiler_temp != old_boiler_temp) or (chiller_temp != old_chiller_temp) or (ratio != old_ratio) or (speed != old_speed):
        start_time = time()
    

# Create MQTT client instance and connect to broker
client = mqtt.Client("Room0Temp")
client.connect(broker_addr, broker_port)
print("Connected to broker")

# Subscribe to relevant topics
client.subscribe(chiller_temp_topic)
print(f"Subscribed to {chiller_temp_topic}")

client.subscribe(boiler_temp_topic)
print(f"Subscribed to {boiler_temp_topic}")

client.subscribe(ahu_topic)
print(f"Subscribed to {ahu_topic}")

# Listen for messages
client.on_message = on_message
client.loop_start()


# Publish sensor readings
while True:
    elapsed_time = time() - start_time

    # Update temp value
    temp = ahu_model(speed, temp, ratio, boiler_temp, chiller_temp, elapsed_time)

    # Publish to MQTT topic
    data = json.dumps({"time": asctime(), "temp": round(temp, 2)})
    client.publish(room_temp_topic, data)

    print(round(temp,2))
    sleep(1)


# Never runs but added for safety
client.loop_stop()
