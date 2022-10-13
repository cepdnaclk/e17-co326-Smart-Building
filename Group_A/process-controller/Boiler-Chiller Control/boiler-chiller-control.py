import paho.mqtt.client as mqtt
import json
import datetime

mqttBroker = "vpn.ce.pdn.ac.lk"
client = mqtt.Client("boiler-chiller-controller")

#temperature at cold air duct
tempColdAirSensorTopic = "326project/smartbuilding/hvac/coldairduct/temperature" 
tempColdAirControlTopic = "326project/smartbuilding/hvac/control/chiller"
tempColdAirScadaTopic =  "326project/smartbuilding/hvac/scada/state/chiller"
tempThreasholdColdAirChangeTopic = "326project/smartbuilding/hvac/change/temp-threash-coldair"
tempColdAirThreashold = 25 #default

#temparature at hot air duct
tempHotAirSensorTopic = "326project/smartbuilding/hvac/hotairduct/temperature"
tempHotAirControlTopic = "326project/smartbuilding/hvac/control/boiler"
tempHotAirScadaTopic = "326project/smartbuilding/hvac/scada/state/boiler"
tempThreasholdHotAirChangeTopic = "326project/smartbuilding/hvac/change/temp-threash-hotair"
tempHotAirThreashold = 15 #default

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
    print("new threashold temperature of Cold Air is " + str(tempHotAirThreashold))
    print("**********************************")
    print()




def on_message_for_cold_air_duct(client, userdata, message):
    data = json.loads(message.payload)
    # print(data)
    
    # data validation
    length = len(data)
    keys = list(data.keys())
    values = list(data.values())
    if (length != 2 or keys[0] != 'time' or keys[1] != 'temp'):
        return
    
    temperature = values[1]
    print("Received Temperature from cold air duct " + str(temperature))
    
    if (temperature > (tempColdAirThreashold + tempCanChange)):
        # Chiller On
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "state": 1
        }
        
        #publish to scada
        client.publish(tempColdAirScadaTopic,json.dumps(x))
        #publish to controller
        client.publish(tempColdAirControlTopic, json.dumps(x))
        print("published 'Chiller ON' to topic " + tempColdAirControlTopic)
        
    #on desired temparatures
    elif (temperature < (tempColdAirThreashold + tempCanChange) and  temperature > (tempColdAirThreashold - tempCanChange)):
        # Chiller Off
         x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "state": 0
             }
         client.publish(tempColdAirScadaTopic,json.dumps(x))
         client.publish(tempColdAirControlTopic, json.dumps(x))
         print("published 'Chiller OFF' to topic " + tempColdAirControlTopic)
         

    print()
    

def on_message_for_hot_air_duct(client, userdata, message):
    data = json.loads(message.payload)
    # print(data)
    
    # data validation
    length = len(data)
    keys = list(data.keys())
    values = list(data.values())
    if (length != 2 or keys[0] != 'time' or keys[1] != 'temp'):
        return
    
    temperature = values[1]
    print("Received Temperature from hot air duct " + str(temperature))
    
    if (temperature < (tempHotAirThreashold - tempCanChange)):
        # Boiler On
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "state": 1
            }
        client.publish(tempHotAirScadaTopic  , json.dumps(x))
        client.publish(tempHotAirControlTopic , json.dumps(x))
        print("published 'Boiler ON' to topic " + tempHotAirControlTopic)
        
    #on desired temparatures
    elif ((temperature < (tempHotAirThreashold + tempCanChange)) and  (temperature > (tempColdAirThreashold - tempCanChange))):
         
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "state": 0
             }
        client.publish(tempHotAirScadaTopic  , json.dumps(x))
        client.publish(tempHotAirControlTopic , json.dumps(x))
        print("published 'Boiler OFF' to topic " + tempHotAirControlTopic)
    
    else:
        x = {
            "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            "state": 0
             }
        client.publish(tempHotAirScadaTopic  , json.dumps(x))
        client.publish(tempHotAirControlTopic , json.dumps(x))
        print("published 'Boiler OFF' to topic " + tempHotAirControlTopic)

    print()




print("Boiler-Chiller-Controller Started.............")
client.message_callback_add(tempColdAirSensorTopic, on_message_for_cold_air_duct)
client.message_callback_add(tempHotAirSensorTopic, on_message_for_hot_air_duct)
client.message_callback_add(tempThreasholdColdAirChangeTopic, on_message_for_temp_threshold_cold_air)
client.message_callback_add(tempThreasholdHotAirChangeTopic, on_message_for_temp_threshold_hot_air)
client.connect(mqttBroker, port=8883)
client.subscribe([("326project/smartbuilding/hvac/#",0),(tempThreasholdColdAirChangeTopic,0),(tempThreasholdHotAirChangeTopic,0)])
client.loop_forever()


# [("326project/smartbuilding/hvac/#",0),(tempThreasholdColdAirChangeTopic,0),(tempThreasholdHotAirChangeTopic,0)]