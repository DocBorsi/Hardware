#include <Servo.h>
#include <HX711_ADC.h>
#include <LiquidCrystal_I2C.h> // You missed the ".h" in the include

LiquidCrystal_I2C lcd(0x27, 20, 4); // LCD I2C address 0x27, 20x4 LCD
Servo servo1; // entrance 
Servo servo2; // load sensor servo
Servo servo3; // reject servo
Servo servo4; // exit
Servo servo5; // segregate

HX711_ADC scale(13, 12);
//float w1, w2, previous = 0;
float previousWeight = 0.0;
int stableCounter = 0;
int stabilityThreshold = 10;


int current_command = -1; 

void setup() {
  Serial.begin(9600); 

  servo1.attach(11);
  servo2.attach(10);
  servo3.attach(9);
  servo4.attach(8);
  servo5.attach(7); 
  servo1.write(0); 
  servo2.write(0); 
  servo3.write(0);
  servo4.write(0);
  servo5.write(0);

  scale.begin();
  scale.start (2000);
  scale.setCalFactor(2500.0);
  scale.tare(); 
  
  lcd.begin();
  lcd.backlight();
  lcd.clear();
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
/*
  else if (current_command == 9) { 
    double weight = getWeight();
    sendResponse(String(weight));
    displayScreen("Weight: " + String(weight) + " g");
    current_command = -1; 
  } */
  
  else if (current_command == 9) {
    getWeight();
    current_command = -1;
  }
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
  servo1.write(0); 
  servo2.write(0); 
  servo3.write(0);
  servo4.write(0);
  servo5.write(0);
}

void openServo1() {
  servo1.write(180);
  servo2.write(0); 
  servo3.write(0);
  servo4.write(0);
  servo5.write(0);
}

void openServo2() {
  servo1.write(0);
  servo2.write(180); 
  servo3.write(0);
  servo4.write(0);
  servo5.write(0);
}

void openServo3() {
  servo1.write(0);
  servo2.write(0); 
  servo3.write(180);
  servo4.write(0);
  servo5.write(0);
}

void openServo4() {
  servo1.write(0);
  servo2.write(0); 
  servo3.write(0);
  servo4.write(180);
  servo5.write(0);
}

void openServo5() {
  servo1.write(0);
  servo2.write(180); 
  servo3.write(0);
  servo4.write(0);
  servo5.write(180);
}

void displayScreen(String message) {
  lcd.clear();  
  lcd.setCursor(0, 0);  
  lcd.print(message);
  lcd.setCursor (0,1);
  lcd.print (message);
}
/*
double getWeight() {
  scale.update();
  w1 = scale.get_units(10);
  delay(100);
  w2 = scale.get_units();
  while (abs(w1 - w2) > 10) {
    w1 = w2;
    w2 = scale.get_units();
    delay(100);
  }
  double kilogram = w1 / 1000;
  return kilogram;
}*/

void getWeight(){
  scale.update();
  float weight = scale.getData();
    if (abs(weight - previousWeight) < 1.0) { // Change in weight is less than 1 gram
    stableCounter++; // Increase stable reading count
  } else {
    stableCounter = 0; // Reset counter if the weight changes significantly
  }
  previousWeight = weight;

  if (stableCounter >= stabilityThreshold) {
        Serial.println(weight);  // Send weight to Raspberry Pi
      } else {
        Serial.println("Waiting");  // Send status message to Raspberry Pi
      }
      delay(100);
    }
