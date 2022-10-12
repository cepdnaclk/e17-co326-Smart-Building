
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
    StaticJsonDocument<200> doc;
    // Deserialize the JSON document
    DeserializationError error = deserializeJson(doc, message);

    // Test if parsing succeeds.
    if (error)
    {
        Serial.print(F("deserializeJson() failed: "));
        Serial.println(error.f_str());
        return;
    }

    const int *state = doc["state"];
    return *state;
}

void controller(char *topic, int state, char *message)
{
    if (strcmp(topic, topic_alarm) == 0)
    {
        if (parse(message))
        {
            digitalWrite(PIN_alarm, HIGH);
        }
        else
        {
            digitalWrite(PIN_alarm, LOW);
        }
    }
    if (strcmp(topic, topic_sprinkler) == 0)
    {
        if (parse(message))
        {
            digitalWrite(PIN_alarm, HIGH);
        }
        else
        {
            digitalWrite(PIN_alarm, LOW);
        }
    }
    if (strcmp(topic, topic_lighting) == 0)
    {
        if (parse(message))
        {
            digitalWrite(PIN_alarm, HIGH);
        }
        else
        {
            digitalWrite(PIN_alarm, LOW);
        }
    }
}