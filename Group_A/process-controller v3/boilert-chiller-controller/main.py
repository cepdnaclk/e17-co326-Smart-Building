
import paho.mqtt.client as mqtt
import json
import datetime

client = mqtt.Client("main-controller")

# sensing topics
tempSensorTopicFromColdAirDuct = "326project/smartbuilding/hvac/coldairduct/temperature"
tempSensorTopicFromHotAirDuct = "326project/smartbuilding/hvac/hotairduct/temperature"

# control topics
boilerControlTopic = "326project/smartbuilding/hvac/control/boiler"
chillerControlTopic = "326project/smartbuilding/hvac/control/chiller"

# change threasholds
tempThreasholdColdAirChangeTopic = "326project/smartbuilding/hvac/control/temp-thresh-coldairduct"
tempThreasholdHotAirChangeTopic = "326project/smartbuilding/hvac/control/temp-thresh-hotairduct"
tempThreasholdChangeTopic = "326project/smartbuilding/hvac/control/temp-thresh"

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
    else:
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


