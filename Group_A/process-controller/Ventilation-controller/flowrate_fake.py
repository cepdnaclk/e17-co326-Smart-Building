import paho.mqtt.client as mqtt
import random
import time
import json
import datetime

mqttBroker = "vpn.ce.pdn.ac.lk"
client =mqtt.Client("Cold Air duct")
topic = "326project/smartbuilding/hvac/coldairduct/airflowrate"

while True:
    client.connect("10.40.18.10", port=1883)
    x = {
        "time": datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S'),
        "airflow": random.uniform(10, 30)
    }

    client.publish(topic, json.dumps(x))
    print("published " + str(x) + " to topic " + topic)
    time.sleep(5)

