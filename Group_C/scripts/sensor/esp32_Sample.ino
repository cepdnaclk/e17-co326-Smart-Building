
#include <WiFi.h>
#include <PubSubClient.h>

 
// Update these with values suitable for your network.

const char* ssid = "EngStudent_NEW";
const char* password = "3nG5tuDt";
const char* mqttServer = "10.40.18.10";   /// example 192.168.0.19
const int mqttPort = 1883;
const char* mqttUser = "";
const char* mqttPassword = "";
const char* topic = "326project/smartbuilding/safety/floor0/room0/sensor/smoke";

#define mq 2
 
WiFiClient espClient;
PubSubClient client(espClient);



int mqSensor;
boolean rc;
char msg[10];
 
void setup() {
  pinMode(mq,INPUT);
  Serial.begin(115200);
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }

  Serial.println("Connected to the WiFi network");
 
  client.setServer(mqttServer, mqttPort);
 
  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");
 
    if (client.connect("ESP32Client")) {
 
      Serial.println("connected");
 
    } else {
 
      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
 
    }
  }
 
  
 
}




void loop() {
  client.loop();
  
  mqSensor = analogRead(mq);    //input for mq2 sensor
  Serial.print("mq2 Sensor reading : ");
  Serial.println(mqSensor);
  delay(500);
  dtostrf(mqSensor,4,2,msg); //converts double to string to msg
  //Serial.println(mq2Sensor);
  if(mqSensor>=225)
  {
    rc = client.publish(topic, msg);
    delay(1000);
    Serial.println("Published");
  }
  // ... and resubscribe
  client.subscribe(topic);
}
