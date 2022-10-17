#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

#define arraySize 10
#define periodTime 2000
#define MSG_BUFFER_SIZE 50

const char* ssid = "Eng-Student";
const char* password = "3nG5tuDt";

const char* mqtt_server = "10.40.18.10";

const char* topic_batteryReady = "326project/smartbuilding/pv/battery/ready";
const char* topic_kwhmeterSensor = "326project/smartbuilding/pv/kWhmeter";
const char* topic_sw1 = "326project/smartbuilding/pv/controls/sw1";
const char* topic_sw2 = "326project/smartbuilding/pv/controls/sw2";

const int currentSensor = A0; // Defining LDR PIN 
const int relay = D7;
const int batteryReadyPin = D6;
const int batteryNotReadyPin = D5;
const int batteryChargingPin = D4;
const int batteryNotChargingPin = D3;

int input_val = 0;  // Varible to store Input values

float meterReading = 0;
float adjustedValue = 0;
float gradient = 5.0;
float offset = 2690;


int lastvalues[arraySize]; //initialize all the values to zero
int tempnew = 0;
int templast = 0;

int maxVal = -32768;//minmul int value
int minVal = 32768;//maximum int value
static int count = 0;

//INT_MIN
//INT_MAX
int difference = 0;

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
char msg[MSG_BUFFER_SIZE];
int value = 0;

char msg1[MSG_BUFFER_SIZE];
char prevGridState[MSG_BUFFER_SIZE] = "0";


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
      //client.subscribe(topic_voltageSensor);
      client.subscribe(topic_batteryReady);
      client.subscribe(topic_sw1);
      client.subscribe(topic_sw2);
      client.subscribe(topic_kwhmeterSensor);
      
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
  DynamicJsonDocument doc(1024);
  
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.println();
  Serial.print(" Message: ");
  
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  deserializeJson(doc, messageTemp);
  JsonObject obj = doc.as<JsonObject>();

  // Feel free to add more if statements to control more GPIOs with MQTT

  // If a message is received on the topic room/lamp, you check if the message is either on or off. Turns the lamp GPIO according to the message
  if(topic==topic_sw1){
    Serial.print("Battery is");
    String pwm_duty = obj["pwm_duty"];
    int pwm = pwm_duty.toInt();

    if(pwm=0){
      //Battery Charging = D3
      //Battery Not Charging = D4
      digitalWrite(batteryNotChargingPin,HIGH);
      digitalWrite(batteryChargingPin,LOW);
      Serial.print(" not charging"); 
    }
    else{
      digitalWrite(batteryNotChargingPin,LOW);
      digitalWrite(batteryChargingPin,HIGH);
      Serial.print(" Charging");  
    }
  }
  
  if(topic==topic_sw2){
      Serial.print("Battery power is ");
      String time1 = obj["time"];
      String sw2 = obj["sw2"];
      
      if(sw2 == "ON"){
        //Switch to battery
        digitalWrite(relay, LOW);
        Serial.print("On");
      }
      else if(sw2 == "OFF"){
        digitalWrite(relay, HIGH);
        Serial.print("Off");
      }
  }
  if(topic == topic_batteryReady){
      Serial.print("Battery is");
      boolean value = obj["value"];
      
      if(value == true){
          digitalWrite(batteryNotReadyPin,LOW);
          digitalWrite(batteryReadyPin,HIGH);
          Serial.print("Ready");
        }
        else{
          digitalWrite(batteryNotReadyPin,HIGH);
          digitalWrite(batteryReadyPin,LOW);
          Serial.print("Not Ready");
          }
    }
  Serial.println();
}

void setup() {
 pinMode(relay, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);  // public
  client.setCallback(callback);
}

void loop() {

  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
//Start of kWpMeter Sensor reading Function
  
  unsigned long now = millis();
  if (now - lastMsg > periodTime) { // publish every two seconds
      lastMsg = now;
       
      meterReading = analogRead(currentSensor);
      Serial.print("Sensor Vlaue = ");
      adjustedValue = meterReading*gradient - offset;
        
      for (byte i = 1; i <= arraySize; i = i + 1) {
        //a function to move values one down the array; 
        if(count<arraySize){
          lastvalues[count]=adjustedValue;
          count++;  
        }
        else{
          tempnew = lastvalues[arraySize-i];
          lastvalues[arraySize-i] = templast;
          templast = tempnew;
        }
    }
    lastvalues[arraySize-1] = adjustedValue;

    Serial.println(adjustedValue);
    
    for (byte i = 0; i < 10; i = i + 1) {
      //takes the max and min values in the array
      maxVal = max(lastvalues[i],maxVal);
      minVal = min(lastvalues[i],minVal);

      //a function to print the array values;
//      Serial.print(i);
//      Serial.print(" = ");
//      Serial.print(lastvalues[i]);
//      Serial.print(" ");
    }
    Serial.println();
    Serial.print("Max Value = ");
    Serial.print(maxVal);
    Serial.print("  Min Value = ");
    Serial.print(minVal);
    difference = maxVal - minVal;
    Serial.print("  Difference = ");
    Serial.print(difference);

  
    //making maxVal and MinVal zero for the next loop
    maxVal = -32768;
    minVal = 32768;

    if(difference<=15){
      snprintf(msg,MSG_BUFFER_SIZE,"%d",0);
      snprintf(msg1,MSG_BUFFER_SIZE,"%s","Power not available");  
    }
    else{
      snprintf(msg,MSG_BUFFER_SIZE,"%d",1);
      snprintf(msg1,MSG_BUFFER_SIZE,"%s","Power available"); 
     }
    Serial.println();
    Serial.print("Publish message: ");
    Serial.println(msg);
    
    if(msg != prevGridState){
      client.publish(topic_kwhmeterSensor, msg);
      snprintf(prevGridState,MSG_BUFFER_SIZE,"%s",msg);
    }
    
    
//End of kWpMeter Sensor reading Function
  
//    input_val = analogRead(LDR);      // Reading Input
//    
//    Serial.print("Publish message: ");
//    Serial.println(input_val);
//    client.publish(topic_kwhmeterSensor, msg);
  }
}
