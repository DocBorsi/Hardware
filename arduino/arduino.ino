#include <Servo.h>
#include <HX711.h>
#include <LiquidCrystal_I2C.h> // You missed the ".h" in the include
#include <Wire.h>

LiquidCrystal_I2C lcd(0x27, 20, 4); // LCD I2C address 0x27, 20x4 LCD
Servo servo1; // entrance 
Servo servo2; // load sensor servo
Servo servo3; // reject servo
Servo servo4; // exit
Servo servo5; // segregate

HX711 scale;
const int dataPin=13;
const int clockPin=12;
float w1, w2, previous = 0;
//float previousWeight = 0.0;
//int stableCounter = 0;
//int reading = 10;
//float cb = 2550.0;

int current_command = -1; 

void setup() {
  Serial.begin(9600); 

  servo1.attach(11);
  servo2.attach(4);
  servo3.attach(3);
  servo4.attach(2);
  servo5.attach(1);   
  servo1.write(170); 
  servo2.write(90); 
  servo3.write(5);
  servo4.write(0);
  servo5.write(0);

  scale.begin(dataPin, clockPin);
//  scale.start (2000);
  scale.set_scale(2950.f);
  scale.tare();
  
  lcd.begin();
  lcd.backlight();

}

void loop() {
  if (current_command == -1) { 
    receiveCommand(); 
  } 
  
  else if (current_command == 0) { 
    closeServo1();
    displayScreen("BOTECANnected");
    current_command = -1; 
  } 
  // push button
  else if (current_command == 1) { 
    openServo1();
    displayScreen("Insert Item");
    current_command = -1; 
  } 
  // first ultrasonic detected an item
  else if (current_command == 2) { 
    closeServo1();
    displayScreen("Item Detected");
    current_command = -1; 
  } 
  // inductive sensor detects a can and it is lightweight
  else if (current_command == 3) { 
    openServo2();
    openServo4();
    displayScreen("Light Can Detected" + String('\t') + "Accepted");
    current_command = -1; 
  }
  // inductive detects a can but it is heavy
  else if (current_command == 4) { 
    openServo2();
    openServo3();
    displayScreen("Heavy Can Detected" + String('\t') + "Rejected");
    current_command = -1; 
  } 
  // inductive did not detect a can but it is lightweight
  else if (current_command == 5) { 
    openServo2();
    current_command = -1; 
  } 
  // inductive did not detect a can and also it is heavy
  else if (current_command == 6) { 
    openServo2();
    openServo3();
    displayScreen("Unknown Heavy Object" + String('\t') + "Rejected");
    current_command = -1; 
  }
  // IR break beam detects a plastic bottle
  else if (current_command == 7) { 
    openServo4();
    openServo5();
    displayScreen("Plastic Bottle Detected" + String('\t') + "Accepted");
    current_command = -1; 
  } 
  // IR break beam did not detect a plastic bottle
  else if (current_command == 8) { 
    openServo3();
    displayScreen("Non-Bottle Object" + String('\t') + "Rejected");
    current_command = -1; 
  }
  else if (current_command == 9) {
    getWeight();
    current_command = -1;
  }
  else if (current_command ==10) {
    closeServo2();
    closeServo4();
    current_command = -1; 
  }
  else if (current_command == 11) { 
    closeServo2();
    closeServo3();
    current_command = -1; 
  }
  else if (current_command == 12) { 
    closeServo2();
    current_command = -1; 
  }
  else if (current_command == 13) { 
    closeServo4();
    closeServo5();
    current_command = -1; 
  } 
  else if (current_command == 14) { 
    closeServo3();
    current_command = -1; 
  }
  delay(500); 
  }
  
void receiveCommand() {
  if (Serial.available()) {
    int sent = Serial.readStringUntil('\n').toInt();
    Serial.println("ok");
    current_command = sent;   
  }
}

void sendResponse(String data) {
  Serial.println(data);
}

void closeServo1() {
  servo1.write(170); 

}

void closeServo2() {
  
  servo2.write(90);

}

void closeServo3() {

  servo3.write(5);

}

void closeServo4() {

  servo4.write(0);

}

void closeServo5() {


  servo5.write(0);
}

void openServo1() {
  servo1.write(80);

}

void openServo2() {
  
  servo2.write(180);

}

void openServo3() {

  servo3.write(110);


}

void openServo4() {

  servo4.write(90);


}

void openServo5() {

  servo5.write(180);
}

void displayScreen(String message) {
  lcd.clear();  
  lcd.setCursor(0, 0);  // Set cursor to the first line
  lcd.print(message.substring(0, 20));  // Print the first 20 characters

  if (message.length() > 20) {
    lcd.setCursor(0, 1);  // Set cursor to the second line
    lcd.print(message.substring(20));   // Print the rest of the message
  }
}


//float getWeight(){
//    scale.update();
//    float weight = scale.getData();
//    if (abs(weight - previousWeight) < 1.0) { // Change in weight is less than 1 gram
//    stableCounter++; // Increase stable reading count
//  } else {
//    stableCounter = 0; // Reset counter if the weight changes significantly
//  }
//  previousWeight = weight;
//
//  if (stableCounter >= stabilityThreshold) {
//        Serial.println(weight);  // Send weight to Raspberry Pi
//      } else {
//        Serial.println("Waiting");  // Send status message to Raspberry P
//      }
//      delay(500);
//    
//}
void getWeight(){
  //scale.set_scale(2950.f);
//  if (scale.is_ready()){
//    float weight = scale.get_units(10);  // Average of 10 readings
//    
//    // Only send weight if it's within a reasonable range (stabilization)
//    if (abs(weight) > 0.01) {  // Avoid sending noise data
//      float gram = max (weight,0.0);
//      //Serial.println(gram);
//      sendResponse(String(gram));
//      lcd.setCursor(0,1);
//      lcd.print("Weight[g]:");
//      lcd.setCursor(0,2);
//      lcd.print(gram);
//      }
//  }
//    else {
//      //Serial.println("scale not ready");
//       sendResponse(String("Scale not ready"));
//    }
//  
//  delay(100);  // Delay 1 second between readings
//}
    w1 = scale.get_units(10);
    delay(100);
    w2 = scale.get_units();
    while ((abs(w1-w2)>10)&&(w1<1))
    {
      w1=w2;
      w2=scale.get_units();
      delay(100);
    }
    float gram = abs(w1);
//    lcd.setCursor(0,1);
//    lcd.print("Weight[g]:");
//    lcd.setCursor(0,2);
//    lcd.print(gram);    
    sendResponse(String(gram));
}
