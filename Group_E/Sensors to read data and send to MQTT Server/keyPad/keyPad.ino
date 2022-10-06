#include <Keypad.h>
 
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
 
byte colPins[n_rows] = {D3, D2, D1, D0};
byte rowPins[n_cols] = {D7, D6, D5, D4};
 
Keypad myKeypad = Keypad( makeKeymap(keys), rowPins, colPins, n_rows, n_cols); 
 
void setup(){
  Serial.begin(9600);
}
 
void loop(){
  char key = myKeypad.getKey();
  
 
  if (key == '*' && pw == 0){
    Serial.println();
    Serial.print("Password: ");
    pw = 1;
  }

  else if (key == 'D' && pw ==1){
    Serial.println();
    Serial.println("sent.");
    pw = 0;
  }

  else if (key != NULL && pw ==1 ){
    Serial.print(key);
  }  

}