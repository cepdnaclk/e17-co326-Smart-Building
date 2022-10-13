#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Update these with values suitable for your network.

const char* ssid = "Eng-Student";
const char* password = "3nG5tuDt";

const char* mqtt_server = "10.40.18.10";
const char* topic_voltageSensor = "326project/smartbuilding/pv/pvVoltage";
const char* topic_kwhMeter = "326project/smartbuilding/pv/controls/kwhMeter2";
const char* topic_sw1 = "326project/smartbuilding/pv/controls/sw1";
const char* topic_sw2 = "326project/smartbuilding/pv/controls/sw2";

//const int LDR = A0; // Defining LDR PIN 
const int relay = D7;
int input_val = 0;  // Varible to store Input values

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE	(50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

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
      client.subscribe(topic_voltageSensor);
      client.subscribe(topic_sw1);
      client.subscribe(topic_sw2);
      
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void callback(String topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // Feel free to add more if statements to control more GPIOs with MQTT

  // If a message is received on the topic room/lamp, you check if the message is either on or off. Turns the lamp GPIO according to the message
  if(topic==topic_sw1){
      Serial.print("Changing Room lamp to ");
      if(messageTemp == ""){
        digitalWrite(relay, HIGH);
        Serial.print("On");
      }
      else{
        digitalWrite(relay, LOW);
        Serial.print("Off");
      }
  }
  else if(topic==topic_sw2){
     if(messageTemp == "Battery"){
        //Battery is normally Open
        digitalWrite(relay,LOW);
        Serial.print("Trying to Switch on the light By Battery");
     }
     else if(messageTemp == "Grid"){
        //Grid is normally closed
        digitalWrite(relay,HIGH);
        Serial.print("Trying to Switch on the light By Grid");
      }
  }
  Serial.println();
}

void setup() {
 pinMode(relay, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(115200);
  setup_wifi();
  // client.setServer(mqtt_server, 8883);
  client.setServer(mqtt_server, 1883);  // public
  client.setCallback(callback);
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();

unsigned long now = millis();
if (now - lastMsg > 15000) { // publish every two seconds
  lastMsg = now;
//    input_val = analogRead(LDR);      // Reading Input
  int randNumber = random(0,2);
  snprintf (msg, MSG_BUFFER_SIZE, "%d", randNumber);
  Serial.print("Publish message: ");
  Serial.println(randNumber);
  client.publish(topic_kwhMeter, msg);
  }
}
