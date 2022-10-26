
/*======================================
 * For RFID
 * -------------------------------------
 *             MFRC522      Arduino Uno      
 * Signal      Pin          Pin          
 * -------------------------------------
 * RST/Reset   RST          9           
 * SPI SS      SDA(SS)      10          
 * SPI MOSI    MOSI         11 / ICSP-4   
 * SPI MISO    MISO         12 / ICSP-1   
 * SPI SCK     SCK          13 / ICSP-3   
 * 
 * For Ultrasonic sensor 1
 * -------------------------------------
 * Ultrasonic   Arduino Uno      
 * Senor Pin    Pin          
 * -------------------------------------
 * VCC          VCC           
 * TRIG         16
 * ECHO         15   
 * GND          GND   
 * 
 * For Ultrasonic sensor 2
 * -------------------------------------
 * Ultrasonic   Arduino Uno      
 * Senor Pin    Pin          
 * -------------------------------------
 * VCC          VCC           
 * TRIG         18
 * ECHO         14   
 * GND          GND  
 * 
 * For Keypad
 * -------------------------------------
 * Ultrasonic   Arduino Uno      
 * Senor Pin    Pin          
 * -------------------------------------
 * R1            17           
 * R2            6
 * R3            7   
 * R4            6
 * C1            5           
 * C2            4
 * C3            3   
 * C4            2
 * --------------------------------------
 * ======================================
 */

//==========//
//   CODE   //
//==========//

// Include Libraries
#include <SPI.h> 
#include <MFRC522.h>
#include <Keypad.h>
#include <SoftwareSerial.h>

/*--------------------------*/
//Occupancy control
//--------------------------//
/*
Ultrasonic sensor 1
-------------------
Vcc 
*/
const int trigPin1 = 16;
const int echoPin1 = 15;
const int trigPin2 = 18;
const int echoPin2 = 14;
const int vcc = 19; 

//define sound velocity in cm/uS
#define SOUND_VELOCITY 0.034
#define CM_TO_INCH 0.393701

long duration1,duration2;
float distance1,distance2;
float distanceInch;

/*--------------------------*/
//Access control
//--------------------------//

////RFID////
#define RST_PIN         9           
#define SS_PIN          10          

MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.

MFRC522::MIFARE_Key key;
byte nuidPICC[4];

////KeyPad////
const byte n_rows = 4;
const byte n_cols = 4;

int num = 0;
int pw = 0;
int count = 0;
 
char keys[n_rows][n_cols] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};
 
byte colPins[n_rows] = {5, 4, 3, 2};
byte rowPins[n_cols] = {17, 8, 7, 6};
 
Keypad myKeypad = Keypad( makeKeymap(keys), rowPins, colPins, n_rows, n_cols); 
String password = "";


/*----------------------------------------------------------------------------*/
SoftwareSerial mySerial(0, 1); // RX, TX
/*----------------------------------------------------------------------------*/

void setup() {
  Serial.begin(9600); // Starts the serial communication
  
/*----------------------------------------------------------------------------*/
//Occupancy control
//----------------------------------------------------------------------------//
  pinMode(trigPin1, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin1, INPUT); // Sets the echoPin as an Input
  pinMode(trigPin2, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin2, INPUT); // Sets the echoPin as an Input
  digitalWrite(vcc, HIGH);

/*----------------------------------------------------------------------------*/
//Access control
//----------------------------------------------------------------------------//

////RFID////
  SPI.begin();        // Init SPI bus
  mfrc522.PCD_Init(); // Init MFRC522 card

  // Prepare the key (used both as key A and as key B)
  // using FFFFFFFFFFFFh which is the default 
  for (byte i = 0; i < 6; i++) {
      key.keyByte[i] = 0xFF;
  }
}

void loop() {

/*----------------------------------------------------------------------------*/
//Occupancy control
//----------------------------------------------------------------------------//
  // Clears the trigPin
  digitalWrite(trigPin1, LOW);
  delay(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin1, HIGH);
  delay(10);
  digitalWrite(trigPin1, LOW);
  
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration1 = pulseIn(echoPin1, HIGH);
  delay(10);

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

  int diff = distance2 - distance1;

  if (diff > 2){
    Serial.println('A');
    Serial.println(1);
    delay(500);
  }
  else if (diff < -2){
    Serial.println('A');
    Serial.println(-1);
    delay(500);
  }

/*----------------------------------------------------------------------------*/
//Access control
//----------------------------------------------------------------------------//

////RFID////
  if ( mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()){
    MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
        // Store NUID into nuidPICC array
        for (byte i = 0; i < 4; i++) {
            nuidPICC[i] = mfrc522.uid.uidByte[i];
        }
        Serial.println('B');
        printDec(mfrc522.uid.uidByte, mfrc522.uid.size);
    }
  
    // Halt PICC
    mfrc522.PICC_HaltA();
    // Stop encryption on PCD
    mfrc522.PCD_StopCrypto1();

 ////KeyPad////
 /*
  * Press '*' to enter a password.
  * Press '#' to Enter
  */
  char key = myKeypad.getKey();
  if (key == '*' && pw == 0){
    pw = 1;
  }

  else if (key == '#' && pw ==1){
    for(int i=1; i<4;i++){
      Serial.println('C');
      Serial.println(password);
      delay(400);
    }
    password = "";
    pw = 0;
  }

  else if (key != NULL && pw ==1 ){
    password = password + key;
  }  
  delay(250);
}

/**
 * Helper routine 
 */
void printDec(byte *buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
      Serial.print(buffer[i] < 0x10 ? " 0" : " ");
      Serial.print(buffer[i], DEC);
  }
  Serial.println("");
}