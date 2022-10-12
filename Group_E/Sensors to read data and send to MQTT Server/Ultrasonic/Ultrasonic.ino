const int trigPin1 = 16;
const int echoPin1 = 15;
const int trigPin2 = 18;
const int echoPin2 = 14;

//define sound velocity in cm/uS
#define SOUND_VELOCITY 0.034
#define CM_TO_INCH 0.393701

long duration1,duration2;
float distance1,distance2;
float distanceInch;

void setup() {
  Serial.begin(9600); // Starts the serial communication
  pinMode(trigPin1, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin1, INPUT); // Sets the echoPin as an Input
  pinMode(trigPin2, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin2, INPUT); // Sets the echoPin as an Input
}

void loop() {
  // Clears the trigPin
  digitalWrite(trigPin1, LOW);
  delay(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin1, HIGH);
  delay(10);
  digitalWrite(trigPin1, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration1 = pulseIn(echoPin1, HIGH);
  delay(2);

  // Clears the trigPin
  digitalWrite(trigPin2, LOW);
  delay(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin2, HIGH);
  delay(10);
  digitalWrite(trigPin2, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration2 = pulseIn(echoPin2, HIGH);
  
  // Calculate the distance
  distance1 = duration1 * SOUND_VELOCITY/2;
  distance2 = duration2 * SOUND_VELOCITY/2;

  int diff = distance1 - distance2;

  if (diff > 2){
    Serial.println("Out");
    Serial.println();
    delay(2000);
  }
  else if (diff < -2){
    Serial.println("In");
    Serial.println();
    delay(2000);
  }
  
  delay(100);
}
