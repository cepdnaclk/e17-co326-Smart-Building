void setup() {
  // put your setup code here, to run once:
  Serial.begin(11520);
  pinMode(D6,OUTPUT);
}

void loop() {
  digitalWrite(D6,HIGH);
  delay(500);
  digitalWrite(D6,LOW);
  delay(500);
  // put your main code here, to run repeatedly:

}
