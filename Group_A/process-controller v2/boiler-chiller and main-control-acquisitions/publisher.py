import paho.mqtt.client as mqtt
import random
import time
import json
import datetime

mqttBroker = "mqtt.eclipseprojects.io"
client =mqtt.Client("Thermostat")
# client.connect(mqttBroker)

topic = "326project/smartbuilding/hvac/sensor/temperature/floorX/roomX"

tempSensorTopicFromColdAirDuct = "326project/smartbuilding/hvac/coldairduct/temperature"
tempSensorTopicFromHotAirDuct = "326project/smartbuilding/hvac/hotairduct/temperature"
tempThreasholdColdAirChangeTopic = "326project/smartbuilding/hvac/control/temp-thresh-coldairduct"
tempThreasholdHotAirChangeTopic = "326project/smartbuilding/hvac/control/temp-thresh-hotairduct"
tempThreasholdChangeTopic = "326project/smartbuilding/hvac/control/temp-thresh"

while True:
    client.connect("10.40.18.10", port=1883)
    x = {
        "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
        "test": random.uniform(0, 100)
    }

    client.publish(tempThreasholdChangeTopic, json.dumps(x))
    print("published " + str(x) + " to topic " + topic)
    time.sleep(5)

