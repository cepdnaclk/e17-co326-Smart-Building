

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
int LED_OCCUPANCY = 15;  //D8 
int LED_TIME = 14;       //D5
int LED_INTENSITY = 13;  //D7

//3nG5tuDt
//Eng-Student //39829828
const char* ssid = "Eng-Student";
const char* password = "3nG5tuDt";
const char* mqtt_server = "10.40.18.10";
//test.mosquitto.org  //10.40.18.10

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
  }
  brightness[length] = '\0';

  int  n;
  n = atoi(brightness);   //get the brightness value as integer
  Serial.println(n);
  if(strcmp(topic, "326project/smartbuilding/lighting/0/1/switch/inside/1") == 0){  
  // Switch off the LED if an 0 was received as first character
    if ((char)payload[0] == '0') {
      digitalWrite(LED_OCCUPANCY, LOW);   // Turn the inside LED1 off 
      client.publish("326project/smartbuilding/lighting/0/1/led/inside/1", "OFF");    
    } else if ((char)payload[0] == '1') {
      analogWrite(LED_OCCUPANCY, 127);  // Turn the inside LED1 dim  
      client.publish("326project/smartbuilding/lighting/0/1/led/inside/1", "DIM"); 
    }else if ((char)payload[0] == '2'){
      digitalWrite(LED_OCCUPANCY, HIGH);  // Turn the inside LED1 on by making the voltage HIGH
      client.publish("326project/smartbuilding/lighting/0/1/led/inside/1", "ON"); 
    }
    else{
      digitalWrite(LED_OCCUPANCY, LOW);   // Turn the inside LED1 off 
      client.publish("326project/smartbuilding/lighting/0/1/led/inside/1", "OFF");       
    }
  }
  if(strcmp(topic, "326project/smartbuilding/lighting/0/1/switch/inside/2") == 0){  
      
      // Switch off the inside LED2 if an 0 was received as first character
    if ((char)payload[0] == '0') {
      digitalWrite(LED_TIME, LOW);   // Turn the inside LED2 off
      client.publish("326project/smartbuilding/lighting/0/1/led/inside/2", "OFF");    
    } else if ((char)payload[0] == '1') {
      analogWrite(LED_TIME, 127);  // Turn the inside LED2 dim by making the voltage HIGH
      client.publish("326project/smartbuilding/lighting/0/1/led/inside/2",  "DIM"); 
    }else if ((char)payload[0] == '2'){
      digitalWrite(LED_TIME, HIGH);  // Turn the inside LED2 on by making the voltage HIGH 
      client.publish("326project/smartbuilding/lighting/0/1/led/inside/2", "ON"); 
    }
    else{
      digitalWrite(LED_TIME, LOW);   // Turn the inside LED2 off
      client.publish("326project/smartbuilding/lighting/0/1/led/inside/2", "OFF");    }
  }
    
  if(strcmp(topic, "326project/smartbuilding/lighting/0/1/switch/outside/1") == 0){  
      // Switch off the outside LED1 if an 0 was received as first character
    if ((char)payload[0] == '0') {
      digitalWrite(LED_INTENSITY, LOW);   // Turn the outside LED1 off
      client.publish("326project/smartbuilding/lighting/0/1/led/outside/1", "OFF");    
    } else if ((char)payload[0] == '1') {
      analogWrite(LED_INTENSITY, 127);  // Turn the outside LED1 dim by making the voltage HIGH
      client.publish("326project/smartbuilding/lighting/0/1/led/outside/1", "DIM"); 
    }else if ((char)payload[0] == '2'){
      digitalWrite(LED_INTENSITY, HIGH);  // Turn the outside LED1 on by making the voltage HIGH
      client.publish("326project/smartbuilding/lighting/0/1/led/outside/1", "ON"); 
    }
    else  {
      digitalWrite(LED_INTENSITY, LOW);   // Turn the outside LED1 off
      client.publish("326project/smartbuilding/lighting/0/1/led/outside/1", "OFF");    }  
        //analogWrite(LED_INTENSITY, n);
  }

  if(strcmp(topic, "326project/smartbuilding/lighting/0/1/switch/inside/3") == 0){
    analogWrite(LED_INTENSITY, n);
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
         
      // ... and resubscribe
      client.subscribe("326project/smartbuilding/lighting/0/1/switch/inside/1");
      client.subscribe("326project/smartbuilding/lighting/0/1/switch/inside/2"); 
      client.subscribe("326project/smartbuilding/lighting/0/1/switch/outside/1");
      client.subscribe("326project/smartbuilding/lighting/0/1/switch/inside/3");        

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
  pinMode(LED_OCCUPANCY, OUTPUT);     
  pinMode(LED_INTENSITY, OUTPUT);
  pinMode(LED_TIME, OUTPUT);  
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883); //8883
  client.setCallback(callback);
}

void loop() {


  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  
}
