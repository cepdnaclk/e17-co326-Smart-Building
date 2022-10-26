# How To Use

The designed HVAC system consists of a hardware actuator control script written for a NodeMCU ESP8266 microcontroller, several Python scripts to model temperature and pressure sensor behaviour, a system controller written in Python, and a SCADA dashboard created using Node-RED. 

**NOTE:** This system utilizes MQTT for communication between the various hardware/software nodes and, hence, require connection to an MQTT broker to function properly. The current setting is as follows to use the cepdnaclk MQTT broker.
```
  Broker Address: 10.40.18.10
  Broker Port: 1883
```

In order to use a different MQTT broker, the broker configuration has to be changed in each of the scripts.


## Actuator Controller

The controller script must be uploaded to an ESP8266 microcontroller and the hardware components connected as provided in the schematics.

**NOTE:** The ESP8266 is intended to connect to the MQTT broker over WiFi. The current configuration is set up to connect to the `Eng-Student` WiFi available at the faculty. The controller script must be recompiled with the new configuration and uploaded to the microcontroller for use with a different WiFi network.


## Sensor Scripts

The sensor scripts are intended to model the behaviour of sensors placed at various locations in the system in response to actuator activation. The scripts are written in Python and require `paho-mqtt` as a dependency.

The `room_temp.py` and `room_pressure.py` scripts expect a floor number and room number as CLI arguments. These can be provided at launch as follows.
```
  python room_temp.py <floorno> <roomno>
  python room_pressure.py <floorno> <roomno>
```


## Process Controller

The process controller is also written in Python and requires the `paho-mqtt` package as a dependency. It controls the overall behaviour of the system by monitoring sensor data and controlling actuators accordingly. It consists of two components: the boiler-chiller control script found at `process-controller v3/boilert-chiller-controller/main.py` and the room control script found at `process-controller v3/room-controller.py`
