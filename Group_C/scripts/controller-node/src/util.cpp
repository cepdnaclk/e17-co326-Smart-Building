
#include <PubSubClient.h>
#include <ArduinoJson.h>

extern const int PIN_lighting;
extern const int PIN_sprinkler;
extern const int PIN_alarm;
extern const char *topic_alarm;
extern const char *topic_sprinkler;
extern const char *topic_lighting;

int parse(char *message)
{
    Serial.println("parser started");
    StaticJsonDocument<200> doc;
    // Deserialize the JSON document
    DeserializationError error = deserializeJson(doc, message);
    Serial.println("deserialized");

    // Test if parsing succeeds.
    if (error)
    {
        Serial.print(F("deserializeJson() failed: "));
        Serial.println(error.f_str());
        return 0;
    }

    Serial.println("acessing state");
    const int state = doc["state"];
    Serial.println(state);
    Serial.println("state accessed");
    return state;
}

void controller(char *topic, char *message)
{
    Serial.println(F("inside controller"));
    Serial.println(F(topic_alarm));
    Serial.println(F(topic));

    if (strcmp(topic, topic_alarm) == 0)
    {
        Serial.println(F("topic alarm"));

        if (parse(message))
        {
            digitalWrite(PIN_alarm, HIGH);
            Serial.println(F("alarm: HIGH"));
        }
        else
        {
            digitalWrite(PIN_alarm, LOW);
            Serial.println(F("alarm: LOW"));
        }
    }
    if (strcmp(topic, topic_sprinkler) == 0)
    {
        Serial.println(F("topic sprinkler"));
        if (parse(message))
        {
            digitalWrite(PIN_alarm, HIGH);
            Serial.println(F("alarm: HIGH"));
        }
        else
        {
            digitalWrite(PIN_alarm, LOW);
            Serial.println(F("alarm: LOW"));
        }
    }
    if (strcmp(topic, topic_lighting) == 0)
    {
        Serial.println(F("topic lighting"));
        if (parse(message))
        {
            digitalWrite(PIN_alarm, HIGH);
            Serial.println(F("alarm: HIGH"));
        }
        else
        {
            digitalWrite(PIN_alarm, LOW);
        }
    }
}