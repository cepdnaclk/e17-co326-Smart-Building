
import paho.mqtt.client as mqtt
import json
import datetime

client = mqtt.Client("room-controller")

# sensing topics
# 326project/smartbuilding/hvac/<floorno>/<roomno>/temperature
tempSensorTopic = "326project/smartbuilding/hvac/0/0/temperature"
# 326project/smartbuilding/hvac/<floorno>/<roomno>/pressure
presSensorTopic = "326project/smartbuilding/hvac/0/0/pressure"

# control topics
# 326project/smartbuilding/hvac/<floorno>/<roomno>/control/ahu
ahuControlTopic = "326project/smartbuilding/hvac/0/0/control/ahu"

# change threasholds
# 326project/smartbuilding/hvac/<floorno>/<roomno>/control/temp-thresh
tempThreasholdChangeTopic = "326project/smartbuilding/hvac/0/0/control/temp-thresh"
# 326project/smartbuilding/hvac/<floorno>/<roomno>/control/pressure-thresh
pressureThreasholdChangeTopic = "326project/smartbuilding/hvac/0/0/control/pressure-thresh"

tempThreashold = 30 # default
pressureThreashold = 30 # default

# allowed ranges
tempCanChange = 2
pressureCanChange = 2

# previous values
previousBlowerSpeed = 40 # default
previousRatio = 0.3 # default

def on_message_for_temp(client, userdata, message):
    data = json.loads(message.payload)
    values = list(data.values())
    temperature = values[1]

    global previousBlowerSpeed
    global previousRatio

    if (temperature < (tempThreashold - tempCanChange)):  # increase the ratio by 0.1
        previousRatio += 0.1
        if previousRatio > 1:
            previousRatio = 1
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "speed": previousBlowerSpeed,
            "ratio": previousRatio
        }
        client.publish(ahuControlTopic, json.dumps(x))
        print("published to topic " + ahuControlTopic + " new ratio - " + str(previousRatio))

    elif (temperature > tempThreashold + tempCanChange):
        previousRatio -= 0.1
        if previousRatio < 0:
            previousRatio = 0

        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "speed": previousBlowerSpeed,
            "ratio": previousRatio
        }
        client.publish(ahuControlTopic, json.dumps(x))
        print("published to topic " + ahuControlTopic + " new ratio - " + str(previousRatio))


def on_message_for_pressure(client, userdata, message):
    data = json.loads(message.payload)
    values = list(data.values())
    pressure = values[1]

    global previousBlowerSpeed
    global previousRatio

    if (pressure < (pressureThreashold - pressureCanChange)):  # increase the blower speed by 1
        previousBlowerSpeed += 1
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "speed": previousBlowerSpeed,
            "ratio": previousRatio
        }
        client.publish(ahuControlTopic, json.dumps(x))
        print("published to topic " + ahuControlTopic + " new blower speed - " + str(previousBlowerSpeed))

    elif (pressure > pressureThreashold + pressureCanChange):
        previousBlowerSpeed -= 1
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "speed": previousBlowerSpeed,
            "ratio": previousRatio
        }
        client.publish(ahuControlTopic, json.dumps(x))
        print("published to topic " + ahuControlTopic + " new blower speed - " + str(previousBlowerSpeed))


client.message_callback_add(tempSensorTopic, on_message_for_temp)
client.message_callback_add(presSensorTopic, on_message_for_pressure)

client.connect("10.40.18.10", port=1883)

client.subscribe([(tempSensorTopic, 0), (presSensorTopic, 0)])
client.loop_forever()


