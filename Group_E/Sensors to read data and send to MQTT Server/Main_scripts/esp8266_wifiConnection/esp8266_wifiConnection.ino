//Inclde libaries
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <SoftwareSerial.h>

// Update these with values suitable for your network.
const char* ssid = "Eng-Student";
const char* password = "3nG5tuDt";

const char* mqtt_server = "10.40.18.10";
const char* sensorTopic = "326project/smartbuilding/occupancy/0/1/ultrasonic";
const char* rfidTopic = "326project/smartbuilding/occupancy/0/1/rfid";
const char* keyPadTopic = "326project/smartbuilding/occupancy/0/1/keypad";

const int port = 1883;

//Create a wifi client
WiFiClient espClient;
PubSubClient client(espClient);

unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE  (50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

SoftwareSerial mySerial (D1,D2); //Rx & Tx pins

//Function to setup the wifi connection
void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

//Function for reconnect the wifi connection
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  mySerial.begin(9600);
  delay(2000);
  Serial.println("==========================================");
  Serial.println("             Smart Building");
  Serial.println("==========================================");
  Serial.println();
  Serial.println("Occupancy and Access Control");
  Serial.println("............................");
  Serial.println();
  
  setup_wifi();
  client.setServer(mqtt_server, port);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  String msg ;
  unsigned long now = millis();
  msg = mySerial.readStringUntil('\r'); 
  String payload = mySerial.readStringUntil('\r');

  //If the is a entrance/exit or rfid or password
  if (msg == "A" || msg == "B" || msg == "C"  ){

    //For entrance or exit
    if (msg == "A"){
      Serial.println();
      Serial.println("A person detected");
      Serial.println(payload);
      client.publish(sensorTopic, payload.c_str());
      delay(2000);
    }

    //For rfid
    else if (msg == "B"){
      Serial.println();
      Serial.println(F("An RFID card detected"));
      Serial.println(payload);
      client.publish(rfidTopic, payload.c_str());
    }

    //For a password
    else if (msg == "C"){
      Serial.println();
      Serial.println(F("A password entered"));
      Serial.println(payload);
      client.publish(keyPadTopic, payload.c_str());    
      delay(2000);
    }
    msg = "";
    
  }
  delay(500); 
}