
import paho.mqtt.client as mqtt
import json
import datetime

client = mqtt.Client("ventilation-controller")

# sensing topics
# 326project/smartbuilding/hvac/<floorno>/<roomno>/temperature
tempSensorTopic = "326project/smartbuilding/hvac/0/0/temperature"

# 326project/smartbuilding/hvac/<floorno>/<roomno>/humidity
humidSensorTopic = "326project/smartbuilding/hvac/0/0/humidity"

# 326project/smartbuilding/hvac/<floorno>/<roomno>/pressure
presSensorTopic = "326project/smartbuilding/hvac/0/0/pressure"

# 326project/smartbuilding/ocupancy/<floorno>/<roomno>/count
countTopic = "326project/smartbuilding/ocupancy/0/0/count"


# control topics
# 326project/smartbuilding/hvac/<floorno>/<roomno>/control/set-temperature
tempControlTopic = "326project/smartbuilding/hvac/0/0/control/set-temperature"

# 326project/smartbuilding/hvac/<floorno>/<roomno>/control/ahu/blower
blowerControlTopic = "326project/smartbuilding/hvac/0/0/control/ahu/blower"

# 326project/smartbuilding/hvac/<floorno>/<roomno>/control/ahu/airflowrate
airFlowRateControl = "326project/smartbuilding/hvac/0/0/control/ahu/airflowrate"




# change threasholds
tempThreasholdChangeTopic = "326project/smartbuilding/hvac/control/temp-thresh"
humidThreasholdChangeTopic = "326project/smartbuilding/hvac/control/humid-thresh"
flowRateThreasholdChangeTopic = "326project/smartbuilding/hvac/control/flowrate-thresh"


tempThreashold = 30 # default
humidThreashold = 30 # default
flowRateThreashold = 30 # default

tempPrevious = 30 # default
humidityPrevious = 30 # default

# allowed ranges
tempCanChange = 2
humidCanChange = 2
flowRateCanChange = 2

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

# changing humid threashold
def on_message_for_humid_threshold(client, userdata, message):
    data = json.loads(message.payload)

    global humidThreashold
    values = list(data.values())
    humidThreashold = values[1]
    print()
    print("**********************************")
    print("new threashold humidity is " + str(humidThreashold))
    print("**********************************")
    print()

# changing flowRate threashold
def on_message_for_flowRate_threshold(client, userdata, message):
    data = json.loads(message.payload)

    global flowRateThreashold
    values = list(data.values())
    flowRateThreashold = values[1]
    print()
    print("**********************************")
    print("new threashold flowrate is " + str(flowRateThreashold))
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





# -------------------------------------------------------------------------------------------------------------------





client.message_callback_add(tempSensorTopicFromColdAirDuct, on_message_for_cold_air_duct)
client.message_callback_add(tempSensorTopicFromHotAirDuct, on_message_for_hot_air_duct)
client.message_callback_add(tempThreasholdColdAirChangeTopic, on_message_for_temp_threshold_cold_air)
client.message_callback_add(tempThreasholdHotAirChangeTopic, on_message_for_temp_threshold_hot_air)
client.message_callback_add(tempThreasholdChangeTopic, on_message_for_temp_threshold)

client.connect("10.40.18.10", port=1883)
client.subscribe([(tempSensorTopicFromColdAirDuct, 0), (tempSensorTopicFromHotAirDuct, 0), (tempThreasholdColdAirChangeTopic, 0), (tempThreasholdHotAirChangeTopic, 0), (tempThreasholdChangeTopic, 0)])
client.loop_forever()


