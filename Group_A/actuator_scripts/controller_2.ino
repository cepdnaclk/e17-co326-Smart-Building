//Microcontroller 2: To get data from the server and control actuators
//Boiler controller, Chiller controller, AHU controller zone 1, AHU controller zone 2 - B_LED, C_LED, A_LED, D_LED respectively
 
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Arduino_JSON.h>

//Define LED pins -- change pins??
const int B_LED = 4; //Boiler indicator
const int C_LED = 12; //Chiller indicator
const int A_LED = 13; //AHU indicator - Zone 1
const int D_LED = 14; //AHU indicator - Zone 2

const char* ssid = "Nokia 6.1 Plus"; //change
const char* password =  "imesh123"; //change

const char* mqtt_server = "broker.hivemq.com"; 
const int mqtt_port = 1883;


WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

//Handle received data from server and control actuators
void callback(char* topic, byte* payload, unsigned int length) {
  String topicStr = topic;
  String msg = "";
  //char buf [50];
  
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.println("] ");
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    msg += String((char)payload[i]); 
  }
  Serial.println();

  //Jsonify received string
  //msg.toCharArray(buf, 50);
  //JSONVar received = JSON.parse(buf);
  JSONVar received = JSON.parse(msg);

  int state = (int) received["state"];

  Serial.println(state);
  
  //Check key list for approriate key and get value
  //JSONVar key_list = received.keys();

  //Handle payload and control boiler, chiller and ahu LEDs
  //Boiler controller
  if (topicStr == "326project/smartbuilding/hvac/control/boiler"){//get the condition from payload
    //Change
    Serial.println("B_LED");
    (state)? digitalWrite(B_LED, HIGH) : digitalWrite(B_LED, LOW);
    //client.publish("326project/smartbuilding/hvac/control/#","test");  
  }
  
  //Chiller controller
  if(topicStr == "326project/smartbuilding/hvac/control/chiller"){//get the condition from payload
    //Change
    Serial.println("C_LED");
    (state)? digitalWrite(C_LED, HIGH) : digitalWrite(C_LED, LOW);
    //client.publish("326project/smartbuilding/hvac/control/#","test");
  }
  
  //AHU controller
  //Zone 1
  if(topicStr == "326project/smartbuilding/hvac/control/ahu/zone1"){//get the condition from payload
    //Change
    Serial.println("A_LED");
    (state)? digitalWrite(A_LED, HIGH) : digitalWrite(A_LED, LOW);
    //client.publish("326project/smartbuilding/hvac/control/#","test");
  }

  //Zone 2
  if(topicStr == "326project/smartbuilding/hvac/control/ahu/zone2"){//get the condition from payload
    //Change
    Serial.println("D_LED");
    (state)? digitalWrite(D_LED, HIGH) : digitalWrite(D_LED, LOW);
    //client.publish("326project/smartbuilding/hvac/control/#","test");
  }

}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID          //////Change
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    
    // Attempt to connect
    if (client.connect(clientId.c_str())) { 
      Serial.println("connected");
      // Subscribe to topics
      client.subscribe("326project/smartbuilding/hvac/control/boiler");
      client.subscribe("326project/smartbuilding/hvac/control/chiller");
      client.subscribe("326project/smartbuilding/hvac/control/ahu/zone1");
      client.subscribe("326project/smartbuilding/hvac/control/ahu/zone2");
      
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() 
{
  pinMode(B_LED, OUTPUT);
  pinMode(C_LED, OUTPUT);
  pinMode(A_LED, OUTPUT);
  pinMode(D_LED, OUTPUT);
  
  Serial.begin(9600);
  setup_wifi(); 

  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
  
}



void loop() 
{
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  delay(2000);
  
  
}
