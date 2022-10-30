___
# Smart Building
___

### Introduction

The optimization of services like heating, ventilation, and air conditioning (HVAC), as well as energy usage and efficiency, is crucial. Building-integrated photovoltaics are a great solution for smart building management.

**Main Systems**
  1. Heating / Ventilation/ Air Conditioning
  2. Lighting
  3. Safety
  4. Energy Usage
  5. Occupancy/Access Control
  6. Photovoltaic
  7. Overall Control  
  
**Each system should have followings**
  1. Sensors to read data and send to MQTT Server.
  2. Read data from MQTT Server and take decisions and control actuators.
  3. Read data from MQTT Server display status of the system on SCADA.
  4. Inputs from the SCADA should send to the MQTT server.
  5. Process controller with operating and optimizing process and algorithms.
  6. MQTT Data, Commands and events should be stored in the database.
  7. Web interface or SCADA pages should display the data in the database.
  8. Data analytics: Prediction Optimization. Correlation.


### The Aim of the Project

The computer engineers build systems containing hardware and software components that are parts of a larger system. The aim of the course is to identify different technologies that can be used to develop a complex computer controlled system such that the design has maximum impact and effect at the system level. 
The project component of the CO326 requires you to implement a real-world control system. It could be from smart cities or smart grid like massive distributed systems or mission-critical aircraft or vehicle control systems.
In industrial automation, Industry 4.0 is focusing on using data originated from the sensors directly at the enterprise level and the cloud level. At enterprise level the sensor data is used for coordinating, managing and optimizing the industry process as well as associated supply chain management. At the cloud level, the data is used for analytics giving the direction for the enterprise management. This would be the foundation of Industry 5.0.
IoT and IIoT are common terms used with Industry 4.0 where the sensors are communicating directly with all levels of automation beyond SCADA focusing on enterprise and cloud levels. IoT is focusing on the consumer applications where as the IIoT is for mission-critical industry applications.
The project encompasses implementation of all aspects of Industry 4.0. The open source or trial versions of software components used by the industry will be used. In addition to making a sample smart industrial implementation, it is aimed to develop an IIoT application framework so the future projects can be based on the framework.

### Proposed Framework

1. Implementing MQTT Broker  
    * Mosquitto Broker is installed in the Dept server, but needs to be tested.  
    * Any other MQTT broker may be considered. All groups can share the server or data can be moved between brokers.

2. Making IIoT devices     
    * Making MQTT enabled IoT device using Arduino/ESP8266/ESP32  
      Get inputs from standard sensors  
      Publish in MQTT  
  Or  
    * Making MQTT gateways using Arduino/ESP8266/ESP32  
      Any industry protocol is converted to MQTT  
      Inputs are published in MQTT   

3. Implementing a SCADA
    * Use open source/industry ready SCADA
    * Connect to the broker
    * Display status, alarms and control actuators

4. Implementing analytic platform 
    * Subscribe to broker
    * Store data in a database
    * Provide/Display historical information
    * Provide/Display simple analytics



