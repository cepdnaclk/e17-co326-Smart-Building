

import paho.mqtt.client as mqtt
import json
import datetime

client = mqtt.Client("blower-controller")

# for temperature
tempSensorTopic = "326project/smartbuilding/hvac/sensor/temperature/floorX/roomX"
tempThreashold = 50
tempCanChange = 5

# for humidity
humidSensorTopic = "326project/smartbuilding/hvac/sensor/humidity/floorX/roomX"
humidThreashold = 50
humidCanChange = 5

tempPrevious = 50 # default value
humidityPrevious = 50 # default value

blowerControlTopic = "326project/smartbuilding/hvac/control/blower/"

tempThreasholdChangeTopic = "326project/smartbuilding/hvac/change/temp-threash"
humidThreasholdChangeTopic = "326project/smartbuilding/hvac/change/humid-threash"

# changing temp threashold value
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

# changing humid threashold value
def on_message_for_humid_threshold(client, userdata, message):
    data = json.loads(message.payload)

    global humidThreashold
    values = list(data.values())
    humidThreashold = values[1]
    print()
    print("**********************************")
    print("new humidThreashold humidity is " + str(humidThreashold))
    print("**********************************")
    print()

# controlling temperature
def on_message_for_temp(client, userdata, message):
    data = json.loads(message.payload)
    print(data)

    # data validation
    length = len(data)
    keys = list(data.keys())
    values = list(data.values())
    if (length != 2 or keys[0] != 'time' or keys[1] != 'temp'):
        return

    tempPrevious = values[1]

    create_blower_control_command(tempPrevious, humidityPrevious)


# controlling humidity
def on_message_for_humid(client, userdata, message):

    data = json.loads(message.payload)
    print(data)

    # data validation
    length = len(data)
    keys = list(data.keys())
    values = list(data.values())
    if (length != 2 or keys[0] != 'time' or keys[1] != 'humid'):
        return

    humidityPrevious = values[1]

    create_blower_control_command(tempPrevious, humidityPrevious)


def create_blower_control_command(temp, humid):

    # if temp and humid are higher
    if ((tempThreashold+tempCanChange) < temp):
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "speed": 0.5
        }
        client.publish(blowerControlTopic, json.dumps(x))
        print("published 'Increase fan speed ' to topic " + blowerControlTopic)

    # if temp and humid are lower
    elif ((tempThreashold-tempCanChange) > temp):
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "speed": -0.5
        }
        client.publish(blowerControlTopic, json.dumps(x))
        print("published 'Decrease fan speed ' to topic " + blowerControlTopic)

    # otherwise no change
    else:
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "speed": 0
        }
        client.publish(blowerControlTopic, json.dumps(x))
        print("published 'Don't change fan speed ' to topic " + blowerControlTopic)

    print()


#
client.message_callback_add(tempSensorTopic, on_message_for_temp)
client.message_callback_add(humidSensorTopic, on_message_for_humid)
client.message_callback_add(tempThreasholdChangeTopic, on_message_for_temp_threshold)
client.message_callback_add(humidThreasholdChangeTopic, on_message_for_humid_threshold)
client.connect("vpn.ce.pdn.ac.lk", port=8883)
client.subscribe([(tempSensorTopic, 0), (humidSensorTopic, 0), (tempThreasholdChangeTopic, 0), (humidThreasholdChangeTopic, 0)])
client.loop_forever()
#








