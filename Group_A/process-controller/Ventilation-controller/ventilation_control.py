import paho.mqtt.client as mqtt
import json

mqttBroker = "vpn.ce.pdn.ac.lk"
client = mqtt.Client("boiler-chiller-controller")

#Air flowrate mqtt topic
airFlowrateSensorTopic = "326project/smartbuilding/hvac/coldairduct/airflowrate"  #subscriber
airFlowrateControlTopic = "326project/smartbuilding/hvac/control/coldairduct/airflowrate"     #publisher
airFlowrateThreashold = 25

flowrateThreasholdChangeTopic = "326project/smartbuilding/hvac/change/flowrate-threash"

#flowrate allowed
flowrateCanChange = 2


# changing temp threashold value of flow rate
def on_message_for_flowrate_threshold(client, userdata, message):
    data = json.loads(message.payload)

    global airFlowrateThreashold
    values = list(data.values())
    airFlowrateThreashold = values[1]
    print()
    print("**********************************")
    print("new threashold flow rate of Cold Air is " + str(airFlowrateThreashold))
    print("**********************************")
    print()



def on_message_for_airflow(client, userdata, message):

    data = json.loads(message.payload)
    # print(data)
    
    # data validation
    length = len(data)
    keys = list(data.keys())
    values = list(data.values())

    #check 'airflow'
    if (length != 2 or keys[0] != 'time' or keys[1] != 'airflow'):
        return
    
    airFlowrate = values[1]
    print("Received Air Flowrate from cold air duct " + str(airFlowrate))
    
    if (airFlowrate > (airFlowrateThreashold + flowrateCanChange)):
        client.publish(airFlowrateControlTopic , "Provide Outside Air")
        print("published 'Provide Outside Air' to topic " + airFlowrateControlTopic)

    #on desired tairFlowRates
    elif (airFlowrate < (airFlowrateThreashold - flowrateCanChange) ):
        client.publish(airFlowrateControlTopic , "Remove inside air")
        print("published 'Remove inside air' to topic " + airFlowrateControlTopic)

    # ==
    else:
        client.publish(airFlowrateControlTopic , "Maintain current flowrate")
        print("published 'Maintain current flowrate' to topic " + airFlowrateControlTopic)


    print()

client.message_callback_add(airFlowrateSensorTopic, on_message_for_airflow)
client.message_callback_add(flowrateThreasholdChangeTopic, on_message_for_flowrate_threshold)
client.connect("10.40.18.10", port=1883)
client.subscribe([(airFlowrateSensorTopic, 0), (flowrateThreasholdChangeTopic, 0)])
client.loop_forever()
