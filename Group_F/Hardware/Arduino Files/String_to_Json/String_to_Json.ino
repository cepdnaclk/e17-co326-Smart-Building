#include <ArduinoJson.h>

void setup() {
 Serial.begin(115200);

 
}

void loop() {
  DynamicJsonDocument doc(1024);

//String input = "{\"sensor\":\"gps\",\"time\":1351824120,\"data\":[48.756080,2.302038]}";     
 String input1 = "{\"time\":1665913516203,\"sw2\":\"OFF\"}";
 deserializeJson(doc, input1);

  JsonObject obj = doc.as<JsonObject>();

 String time1 = obj["time"];
 String sw2 = obj["sw2"];
 
 Serial.println(time1);
 Serial.println(sw2); 
 //Serial.println(obj["time"]);
 //Serial.println(obj["sw2"]);

}
