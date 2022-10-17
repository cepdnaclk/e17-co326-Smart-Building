
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


def on_message_for_pressure(client, userdata, message):
    data = json.loads(message.payload)
    values = list(data.values())
    pressure = values[1]

    if (pressure < (pressureThreashold - pressureCanChange)):  # increase the blower speed by 1
        global previousBlowerSpeed
        global previousRatio
        previousBlowerSpeed += 1
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "speed": previousBlowerSpeed,
            "ratio": previousRatio
        }
        client.publish(ahuControlTopic, json.dumps(x))
        print("published to topic " + ahuControlTopic + " new blower speed - " + previousBlowerSpeed)

    elif (airFlowRate > flowRateThreashold + flowRateCanChange):
        global previousBlowerSpeed
        global previousRatio
        previousBlowerSpeed -= 1
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "speed": previousBlowerSpeed,
            "ratio": previousRatio
        }
        client.publish(ahuControlTopic, json.dumps(x))
        print("published to topic " + ahuControlTopic + " new blower speed - " + previousBlowerSpeed)





