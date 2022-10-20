
import paho.mqtt.client as mqtt
import json
import datetime

from pyparsing import one_of

client = mqtt.Client("room-controller")

# sensing topics
# 326project/smartbuilding/hvac/<floorno>/<roomno>/temperature
tempSensorTopic = "326project/smartbuilding/hvac/0/0/temperature"
tempSensorTopic2 = "326project/smartbuilding/hvac/0/1/temperature"
# 326project/smartbuilding/hvac/<floorno>/<roomno>/pressure
presSensorTopic = "326project/smartbuilding/hvac/0/0/pressure"
presSensorTopic2 = "326project/smartbuilding/hvac/0/1/pressure"

# control topics
# 326project/smartbuilding/hvac/<floorno>/<roomno>/control/ahu
ahuControlTopic = "326project/smartbuilding/hvac/0/0/control/ahu"
ahuControlTopic2 = "326project/smartbuilding/hvac/0/1/control/ahu"


# change threasholds
# 326project/smartbuilding/hvac/<floorno>/<roomno>/control/temp-thresh
tempThreasholdChangeTopic = "326project/smartbuilding/hvac/0/0/control/temp-thresh"
tempThreasholdChangeTopic2 = "326project/smartbuilding/hvac/0/1/control/temp-thresh"
# 326project/smartbuilding/hvac/<floorno>/<roomno>/control/pressure-thresh
pressureThreasholdChangeTopic = "326project/smartbuilding/hvac/0/0/control/pressure-thresh"
pressureThreasholdChangeTopic2 = "326project/smartbuilding/hvac/0/1/control/pressure-thresh"

tempThreashold = 30 # default
tempThreashold2 = 30 # default

pressureThreashold = 1 # default
pressureThreashold2 = 1 # default

# allowed ranges
tempCanChange = 1
tempCanChange2 = 1

pressureCanChange = 0.1
pressureCanChange2 = 0.1

# previous values
previousBlowerSpeed = 40 # default
previousBlowerSpeed2 = 40 # default

previousRatio = 0.3 # default
previousRatio2 = 0.3 # default

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
            "ratio": round(previousRatio, 2)
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
            "ratio": round(previousRatio, 2)
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
        previousBlowerSpeed = min(previousBlowerSpeed+1, 100)
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "speed": previousBlowerSpeed,
            "ratio": round(previousRatio, 2)
        }
        client.publish(ahuControlTopic, json.dumps(x))
        print("published to topic " + ahuControlTopic + " new blower speed - " + str(previousBlowerSpeed))

    elif (pressure > pressureThreashold + pressureCanChange):
        previousBlowerSpeed = max(previousBlowerSpeed-1, 0)
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "speed": previousBlowerSpeed,
            "ratio": round(previousRatio, 2)
        }
        client.publish(ahuControlTopic, json.dumps(x))
        print("published to topic " + ahuControlTopic + " new blower speed - " + str(previousBlowerSpeed))


##### Change threasholds

# changing temp threashold
def on_message_for_temp_threshold(client, userdata, message):
    data = json.loads(message.payload)

    global tempThreashold
    values = list(data.values())
    tempThreashold = values[1]
    print()
    print("**********************************")
    print("new threashold temperature is " + str(tempThreashold))
    print("**********************************")
    print()


# changing pressure threashold
def on_message_for_pressure_threshold(client, userdata, message):
    data = json.loads(message.payload)
    global pressureThreashold
    values = list(data.values())
    pressureThreashold = values[1]
    print()
    print("**********************************")
    print("new threashold pressure is " + str(pressureThreashold))
    print("**********************************")
    print()


# ---------------------------------------------------------------------------------------------------------------------
def on_message_for_temp2(client, userdata, message):
    data = json.loads(message.payload)
    values = list(data.values())
    temperature = values[1]

    global previousBlowerSpeed2
    global previousRatio2

    if (temperature < (tempThreashold2 - tempCanChange2)):  # increase the ratio by 0.1
        previousRatio2 += 0.1
        if previousRatio2 > 1:
            previousRatio2 = 1
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "speed": previousBlowerSpeed2,
            "ratio": round(previousRatio2, 2)
        }
        client.publish(ahuControlTopic2, json.dumps(x))
        print("published to topic " + ahuControlTopic2 + " new ratio - " + str(previousRatio2))

    elif (temperature > tempThreashold2 + tempCanChange2):
        previousRatio2 -= 0.1
        if previousRatio2 < 0:
            previousRatio2 = 0

        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "speed": previousBlowerSpeed2,
            "ratio": round(previousRatio2, 2)
        }
        client.publish(ahuControlTopic2, json.dumps(x))
        print("published to topic " + ahuControlTopic2 + " new ratio - " + str(previousRatio2))


def on_message_for_pressure2(client, userdata, message):
    data = json.loads(message.payload)
    values = list(data.values())
    pressure = values[1]

    global previousBlowerSpeed2
    global previousRatio2

    if (pressure < (pressureThreashold2 - pressureCanChange2)):  # increase the blower speed by 1
        previousBlowerSpeed2 = min(previousBlowerSpeed2+1, 100)
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "speed": previousBlowerSpeed2,
            "ratio": round(previousRatio2, 2)
        }
        client.publish(ahuControlTopic2, json.dumps(x))
        print("published to topic " + ahuControlTopic2 + " new blower speed - " + str(previousBlowerSpeed2))

    elif (pressure > pressureThreashold2 + pressureCanChange2):
        previousBlowerSpeed2 = max(previousBlowerSpeed2-1, 0)
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "speed": previousBlowerSpeed2,
            "ratio": round(previousRatio2, 2)
        }
        client.publish(ahuControlTopic2, json.dumps(x))
        print("published to topic " + ahuControlTopic2 + " new blower speed - " + str(previousBlowerSpeed2))


##### Change threasholds

# changing temp threashold2
def on_message_for_temp_threshold2(client, userdata, message):
    data = json.loads(message.payload)

    global tempThreashold2
    values = list(data.values())
    tempThreashold2 = values[1]
    print()
    print("**********************************")
    print("new threashold temperature is " + str(tempThreashold2))
    print("**********************************")
    print()


# changing pressure threashold
def on_message_for_pressure_threshold2(client, userdata, message):
    data = json.loads(message.payload)

    global pressureThreashold2
    values = list(data.values())
    pressureThreashold2 = values[1]
    print()
    print("**********************************")
    print("new threashold pressure is " + str(pressureThreashold2))
    print("**********************************")
    print()



client.message_callback_add(tempSensorTopic, on_message_for_temp)
client.message_callback_add(presSensorTopic, on_message_for_pressure)
client.message_callback_add(tempThreasholdChangeTopic, on_message_for_temp_threshold)
client.message_callback_add(pressureThreasholdChangeTopic, on_message_for_pressure_threshold)

client.message_callback_add(tempSensorTopic2, on_message_for_temp2)
client.message_callback_add(presSensorTopic2, on_message_for_pressure2)
client.message_callback_add(tempThreasholdChangeTopic2, on_message_for_temp_threshold2)
client.message_callback_add(pressureThreasholdChangeTopic2, on_message_for_pressure_threshold2)

client.connect("10.40.18.10", port=1883)

client.subscribe([(tempSensorTopic, 0), (presSensorTopic, 0),
                  (tempThreasholdChangeTopic, 0), (pressureThreasholdChangeTopic, 0),
                  (tempSensorTopic2, 0), (presSensorTopic2, 0),
                  (tempThreasholdChangeTopic2, 0), (pressureThreasholdChangeTopic2, 0)
                  ])
client.loop_forever()


