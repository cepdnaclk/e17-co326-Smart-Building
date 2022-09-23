## Starting nodered
node-red

## Mosquitto
sudo systemctl status mosquitto

## install mosquitto client
sudo apt install mosquitto-clients

## pub 
mosquitto_pub -t smartbuilding/hvac/humid -m "humidity: 63.3"

## pub (json)
 mosquitto_pub -h localhost -t topic/humid -m "{\"humidity\":6.4,\"timestamp\":20231230,\"floorno\":2,\"roomno\":4}"
## sub
mosquitto_sub -t smartbuilding/hvac/humid

## SQL 
sudo systemctl start mysql

## Check running port 
SHOW GLOBAL VARIABLES LIKE 'PORT';

