

#include <ESP8266WiFi.h>
#include <PubSubClient.h>
int LED_NON_ESSENTIAL = D6;  //D6
int LED_ESSENTIAL = D5;      //D5


// Update these with values suitable for your network.
//3nG5tuDt
//Eng-Student //39829828
const char* ssid = "Eng-Student"; //"Dialog 4G 730";
const char* password =   "3nG5tuDt";  //"79C1d1e1" ;
const char* mqtt_server =  "10.40.18.10"; //"broker.hivemq.com";
//test.mosquitto.org

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE	(50)
char msg[MSG_BUFFER_SIZE];
int value = 0;
//char brighness[];


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
    Serial.println("connecting..");
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
  
  Serial.print("\n");

  if(strcmp(topic, "326project/smartbuilding/energy/floor0/power/control") == 0){  
    if ((char)payload[9] == '0') {
      Serial.println((char)payload[9]);
      digitalWrite(LED_ESSENTIAL, HIGH );   // Turn the LED on (Note that LOW is the voltage level    
    }
    else if((char)payload[9] == '1'){
      digitalWrite(LED_ESSENTIAL, LOW );   // Turn the LED off (Note that LOW is the voltage level   
      Serial.print("HIGH") ;      
    }
    
  }
  
  else if(strcmp(topic, "326project/smartbuilding/energy/floor0/room0/power/control") == 0){  
    if ((char)payload[9] == '0') {
      Serial.println((char)payload[9]);
      digitalWrite(LED_ESSENTIAL, HIGH );   // Turn the LED on (Note that LOW is the voltage level    
    }
    else if((char)payload[9] == '1'){
      digitalWrite(LED_ESSENTIAL, LOW );   // Turn the LED off (Note that LOW is the voltage level   
      Serial.print("HIGH") ;      
    }
    
  }

  else{
    if(strcmp(topic, "326project/smartbuilding/energy/floor0/room2/l/power/control") == 0){  
    // Switch on the LED if an 1 was received as first character
      int pin;
      if ((char)payload[19] == 'n') {
        pin = LED_NON_ESSENTIAL;
      }
      if ((char)payload[19] == 'e') {
        pin = LED_ESSENTIAL;        
      }
      else{
        pin = LED_NON_ESSENTIAL;        
      }

      if ((char)payload[9] == '0') {
        Serial.println((char)payload[9]);
        digitalWrite(pin, HIGH );   // Turn the LED on (Note that LOW is the voltage level    
      }
      else if((char)payload[9] == '1'){
        digitalWrite(pin, LOW );   // Turn the LED off (Note that LOW is the voltage level   
        Serial.print("HIGH") ;      
      }
      // but actually the LED is on; this is because
      // it is active low on the ESP-01)
    }
    if(strcmp(topic, "326project/smartbuilding/energy/floor0/room2/b/power/control") == 0){  
    // Switch on the LED if an 1 was received as first character
      if ((char)payload[9] == '0') {
        Serial.println((char)payload[9]);
        digitalWrite(LED_ESSENTIAL, HIGH );   // Turn the LED on (Note that LOW is the voltage level    
      }
      else if((char)payload[9] == '1'){
        digitalWrite(LED_ESSENTIAL, LOW );   // Turn the LED off (Note that LOW is the voltage level   
        Serial.print("HIGH") ;      
      }
      // but actually the LED is on; this is because
      // it is active low on the ESP-01)
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
      client.subscribe("co326project/smartbuilding/energy/floor0/room2/ahu/power");
      client.subscribe("326project/smartbuilding/energy/floor0/room2/b/power/control");        
      client.subscribe("326project/smartbuilding/energy/floor0/room2/l/power/control");        
      client.subscribe("326project/smartbuilding/energy/floor0/power/control");        
      client.subscribe("326project/smartbuilding/energy/floor0/room0/power/control");        

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
  pinMode(D0, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  pinMode(LED_ESSENTIAL, OUTPUT);
  pinMode(LED_NON_ESSENTIAL, OUTPUT);  
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883); //8883
  client.subscribe("326project/smartbuilding/energy/floor0/room2/b/power/control");        
  client.subscribe("326project/smartbuilding/energy/floor0/room2/l/power/control");        
  client.subscribe("326project/smartbuilding/energy/floor0/power/control");        
  client.subscribe("326project/smartbuilding/energy/floor0/room0/power/control");        

  
  client.setCallback(callback);
}

void loop() {

  short reading;
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  /*unsigned long now = millis();
  if (now - lastMsg > 2000) {
    //pinMode(LED,INPUT);
    //reading = digitalRead(LED);  
    lastMsg = now;
    ++value;
    snprintf (msg, MSG_BUFFER_SIZE, "hello world #%ld", value);
    Serial.print("Publish message: ");
    Serial.println(msg);
    //client.publish("326project/smartbuilding/lightning/1/1/led/1", msg);
  }*/
}
