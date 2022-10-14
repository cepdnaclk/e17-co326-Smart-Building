float meterReading = 0;
float adjustedValue = 0;
float gradient = 5.0;
float offset = 2690;

int lastvalues[10]= {0,0,0,0,0,0,0,0,0,0};
int tempnew = 0;
int templast = 0;

int maxVal = 0;
int minVal = 0;
int difference = 0;

const int analogIn = A0;

void setup(){
  Serial.begin(115200);  
}

void loop(){
  //Start of kWpMeter Sensor reading Function
  
  meterReading = analogRead(analogIn);
  Serial.print("Sensor Vlaue = ");
  adjustedValue = meterReading*gradient - offset;
  
  for (byte i = 1; i <= 10; i = i + 1) {
    //a function to move values one down the array; 
    tempnew = lastvalues[10-i];
    lastvalues[10-i] = templast;
    templast = tempnew;
  }
  lastvalues[9] = adjustedValue;

  Serial.println(adjustedValue);

  for (byte i = 0; i < 10; i = i + 1) {
    //takes the max and min values in the array
    maxVal = max(lastvalues[i],maxVal);
    minVal = min(lastvalues[i],minVal);

    //a function to print the array values;
    Serial.print(i);
    Serial.print(" = ");
    Serial.print(lastvalues[i]);
    Serial.print(" ");
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
  maxVal = 0;
  minVal = 0;

  Serial.println();

  //take readings every two seconds 
  delay(500);

  //End of kWpMeter Sensor reading Function
}
