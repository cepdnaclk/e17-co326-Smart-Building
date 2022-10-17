#include <LiquidCrystal.h>
#include <WiFi.h>
#include <PubSubClient.h>

int LED_OCCUPANCY1 = 25; 
int LED_OCCUPANCY2 = 26;
// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(19, 23, 18, 17, 16, 15);
// Update these with values suitable for your network.


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
  
  Serial.println(int(*payload));

  if(strcmp(topic, "326project/smartbuilding/occupancy/0/1/lcd") == 0){
    if(brightness[0]=='t'){ 
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Crowded");
      lcd.setCursor(0, 1);
      lcd.print("Limit Exceeded");
      digitalWrite(LED_OCCUPANCY1,LOW);
      digitalWrite(LED_OCCUPANCY2,HIGH);
      delay(1000);
    }
  }

  if(strcmp(topic, "326project/smartbuilding/occupancy/0/1/ledred") == 0){
    if(brightness[0]=='t'){ 
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("Green");
      lcd.setCursor(0, 1);
      lcd.print("Access Granted");
      digitalWrite(LED_OCCUPANCY1,HIGH);
      digitalWrite(LED_OCCUPANCY2,LOW);
      delay(1000);
    }
    else{
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("RED");
      lcd.setCursor(0, 1);
      lcd.print("Access Denied");
      digitalWrite(LED_OCCUPANCY1,LOW);
      digitalWrite(LED_OCCUPANCY2,HIGH);
      delay(1000);
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
      client.subscribe("esp32/test"); 
      client.subscribe("326project/smartbuilding/occupancy/0/1/lcd");  
      client.subscribe("326project/smartbuilding/occupancy/0/1/ledred");     

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
  // set up the LCD's number of columns and rows:
  pinMode(LED_OCCUPANCY1, OUTPUT);
  pinMode(LED_OCCUPANCY2, OUTPUT);
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("CO326 Group 5");    
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

}
