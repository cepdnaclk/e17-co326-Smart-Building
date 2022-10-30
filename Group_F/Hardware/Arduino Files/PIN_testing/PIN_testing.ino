void setup() {
  // put your setup code here, to run once:
  Serial.begin(11520);
  pinMode(D6,OUTPUT);
  pinMode(D5,OUTPUT);
  pinMode(D2,OUTPUT);
  pinMode(D3,OUTPUT);
}

void loop() {
  digitalWrite(D6,HIGH);
  digitalWrite(D5,HIGH);
  digitalWrite(D2,HIGH);
  digitalWrite(D3,HIGH);
  delay(500);
  digitalWrite(D6,LOW);
  digitalWrite(D5,LOW);
  digitalWrite(D2,LOW);
  digitalWrite(D3,LOW);
  
  delay(500);
  // put your main code here, to run repeatedly:

}
