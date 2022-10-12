

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
int LED_OCCUPANCY = 15;  //D8
int LED_TIME = 14;       //D5
int LED_INTENSITY = 13;  //D7


// Update these with values suitable for your network.
//3nG5tuDt
//Eng-Student //39829828
const char* ssid = "Eng-Student";
const char* password = "3nG5tuDt";
const char* mqtt_server = "10.40.18.10";
//test.mosquitto.org

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
    Serial.print("connecting..");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  char brightness[length];
  for (int i = 0; i < length; i++) {
    brightness[i] = (char)payload[i];
    Serial.print(brightness[i]);
    
  }
  
  Serial.println(int(*payload));
  if(strcmp(topic, "326project/smartbuilding/lighting/0/1/switch/inside/1") == 0){  
  // Switch on the LED if an 1 was received as first character
      if ((char)payload[0] == '0') {
        digitalWrite(LED_OCCUPANCY, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
        client.publish("326project/smartbuilding/lighting/0/1/led/inside/1", "OFF");    
      } else if ((char)payload[0] == '1') {
        analogWrite(LED_OCCUPANCY, 127);  // Turn the LED off by making the voltage HIGH
        client.publish("326project/smartbuilding/lighting/0/1/led/inside/1", "DIM"); 
      }else {
        digitalWrite(LED_OCCUPANCY, HIGH);  // Turn the LED off by making the voltage HIGH
        client.publish("326project/smartbuilding/lighting/0/1/led/inside/1", "ON"); 
      }
    }
    if(strcmp(topic, "326project/smartbuilding/lighting/0/1/switch/inside/2") == 0){  
      //326project/smartbuilding/lighting/control/timesheduling/1/1/2
  // Switch on the LED if an 1 was received as first character
      if ((char)payload[0] == '0') {
        digitalWrite(LED_TIME, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
        client.publish("326project/smartbuilding/lighting/0/1/led/inside/2", "OFF");    
      } else if ((char)payload[0] == '1') {
        analogWrite(LED_TIME, 127);  // Turn the LED off by making the voltage HIGH
        client.publish("326project/smartbuilding/lighting/0/1/led/inside/2",  "DIM"); 
      }else {
        digitalWrite(LED_TIME, HIGH);  // Turn the LED off by making the voltage HIGH 
        client.publish("326project/smartbuilding/lighting/0/1/led/inside/2", "ON"); 
      }
    }
    
    if(strcmp(topic, "326project/smartbuilding/lighting/0/1/switch/outside/1") == 0){  
  // Switch on the LED if an 1 was received as first character
      if ((char)payload[0] == '0') {
        digitalWrite(LED_INTENSITY, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is active low on the ESP-01)
        client.publish("326project/smartbuilding/lighting/0/1/led/outside/1", "OFF");    
      } else if ((char)payload[0] == '1') {
        analogWrite(LED_INTENSITY, 127);  // Turn the LED off by making the voltage HIGH
        client.publish("326project/smartbuilding/lighting/0/1/led/outside/1", "DIM"); 
      }else {
        digitalWrite(LED_INTENSITY, HIGH);  // Turn the LED off by making the voltage HIGH
        client.publish("326project/smartbuilding/lighting/0/1/led/outside/1", "ON"); 
      }
    }       

  
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
      // Once connected, publish an announcement...
      client.publish("326project/smartbuilding/lighting/0/1/led/inside/1", "MQTT server connected");
      client.publish("326project/smartbuilding/lighting/0/1/led/inside/2", "MQTT server connected");
      client.publish("326project/smartbuilding/lighting/0/1/led/outside/1", "MQTT server connected");
      //326project/smartbuilding/lighting/0/1/led/inside/1
      //326project/smartbuilding/lighting/0/1/led/inside/2
      //326project/smartbuilding/lighting/0/1/led/outside/1
      //326project/smartbuilding/lightning/control/timescheduling/1/1/2
      //326project/smartbuilding/lightning/control/occupancy/1/1/1
      //326project/smartbuilding/lightning/control/intensity/1/1/3    
      // ... and resubscribe
      client.subscribe("326project/smartbuilding/lighting/0/1/switch/inside/1");
      client.subscribe("326project/smartbuilding/lighting/0/1/switch/inside/2"); 
      client.subscribe("326project/smartbuilding/lighting/0/1/switch/outside/1");
      client.subscribe("326project/smartbuilding/lighting/ishini");        

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
  pinMode(LED_OCCUPANCY, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  pinMode(LED_INTENSITY, OUTPUT);
  pinMode(LED_TIME, OUTPUT);  
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883); //8883
  client.setCallback(callback);
}

void loop() {

  short reading;
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > 2000) {
    //pinMode(LED,INPUT);
    //reading = digitalRead(LED);  
    lastMsg = now;
    ++value;
    snprintf (msg, MSG_BUFFER_SIZE, "hello world #%ld", value);
    Serial.print("Publish message: ");
    Serial.println(msg);
    //client.publish("326project/smartbuilding/lightning/1/1/led/1", msg);
  }
}
