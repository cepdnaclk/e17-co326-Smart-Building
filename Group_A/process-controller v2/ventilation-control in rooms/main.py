
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


temperatureThreashold = 30 # default
humidityThreashold = 30 # default
flowRateThreashold = 30 # default

# allowed ranges
tempCanChange = 2
humidCanChange = 2
flowRateCanChange = 2

# changing temp threashold
def on_message_for_temp_threshold(client, userdata, message):
    data = json.loads(message.payload)

    global temperatureThreashold
    values = list(data.values())
    temperatureThreashold = values[1]
    print()
    print("**********************************")
    print("new threashold temperature is " + str(temperatureThreashold))
    print("**********************************")
    print()

# changing humid threashold
def on_message_for_humid_threshold(client, userdata, message):
    data = json.loads(message.payload)

    global humidityThreashold
    values = list(data.values())
    humidityThreashold = values[1]
    print()
    print("**********************************")
    print("new threashold humidity is " + str(humidityThreashold))
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






# -------------------------------------------------------------------------------------------------------------------


tempColdAirThreashold = 25 #default
tempHotAirThreashold = 15 #default
tempThreashold = 30 #default

#temparature range that allowed
tempCanChange = 2


# changing temp threashold value of Cold Air
def on_message_for_temp_threshold_cold_air(client, userdata, message):
    data = json.loads(message.payload)

    global tempColdAirThreashold
    values = list(data.values())
    tempColdAirThreashold = values[1]
    print()
    print("**********************************")
    print("new threashold temperature of Cold Air is " + str(tempColdAirThreashold))
    print("**********************************")
    print()


# changing temp threashold value of Hot Air
def on_message_for_temp_threshold_hot_air(client, userdata, message):
    data = json.loads(message.payload)

    global tempHotAirThreashold
    values = list(data.values())
    tempHotAirThreashold = values[1]
    print()
    print("**********************************")
    print("new threashold temperature of Hot Air is " + str(tempHotAirThreashold))
    print("**********************************")
    print()



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

def on_message_for_cold_air_duct(client, userdata, message):
    data = json.loads(message.payload)
    # print(data)

    # data validation
    length = len(data)
    keys = list(data.keys())
    values = list(data.values())
    # if (length != 2 or keys[0] != 'time' or keys[1] != 'temp'):
    #     return

    temperature = values[1]
    print("Received Temperature from cold air duct " + str(temperature))

    if (temperature > (tempColdAirThreashold + tempCanChange)):
        # Chiller On
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "state": 1
        }

        #publish to controller
        client.publish(chillerControlTopic, json.dumps(x))
        print("published 'Chiller ON' to topic " + chillerControlTopic)

    #on desired temparatures
    elif (temperature < (tempColdAirThreashold + tempCanChange) and  temperature > (tempColdAirThreashold - tempCanChange)):
        # Chiller Off
         x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "state": 0
             }
         # client.publish(tempColdAirScadaTopic,json.dumps(x))
         client.publish(chillerControlTopic, json.dumps(x))
         print("published 'Chiller OFF' to topic " + chillerControlTopic)


    print()


def on_message_for_hot_air_duct(client, userdata, message):
    data = json.loads(message.payload)
    # print(data)

    # data validation
    length = len(data)
    keys = list(data.keys())
    values = list(data.values())
    # if (length != 2 or keys[0] != 'time' or keys[1] != 'temp'):
    #     return

    temperature = values[1]
    print("Received Temperature from hot air duct " + str(temperature))

    if (temperature < (tempHotAirThreashold - tempCanChange)):
        # Boiler On
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "state": 1
            }
        # client.publish(tempHotAirScadaTopic  , json.dumps(x))
        client.publish(boilerControlTopic , json.dumps(x))
        print("published 'Boiler ON' to topic " + boilerControlTopic)

    #on desired temparatures
    else:

        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "state": 0
             }
        # client.publish(tempHotAirScadaTopic  , json.dumps(x))
        client.publish(boilerControlTopic , json.dumps(x))
        print("published 'Boiler OFF' to topic " + boilerControlTopic)


    print()

client.message_callback_add(tempSensorTopicFromColdAirDuct, on_message_for_cold_air_duct)
client.message_callback_add(tempSensorTopicFromHotAirDuct, on_message_for_hot_air_duct)
client.message_callback_add(tempThreasholdColdAirChangeTopic, on_message_for_temp_threshold_cold_air)
client.message_callback_add(tempThreasholdHotAirChangeTopic, on_message_for_temp_threshold_hot_air)
client.message_callback_add(tempThreasholdChangeTopic, on_message_for_temp_threshold)

client.connect("10.40.18.10", port=1883)
client.subscribe([(tempSensorTopicFromColdAirDuct, 0), (tempSensorTopicFromHotAirDuct, 0), (tempThreasholdColdAirChangeTopic, 0), (tempThreasholdHotAirChangeTopic, 0), (tempThreasholdChangeTopic, 0)])
client.loop_forever()


