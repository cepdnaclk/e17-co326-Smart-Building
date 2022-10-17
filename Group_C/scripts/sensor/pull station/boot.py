from machine import Pin
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import esp
import json
esp.osdebug(None)
import gc
gc.collect()

ssid = 'Eng-Student'
password = '3nG5tuDt'
mqtt_server = '10.40.18.10'  #Replace with your MQTT Broker IP

client_id = ubinascii.hexlify(machine.unique_id())
# change the topic below as necessary
topic_pub = b'esp32/pullstation'

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())