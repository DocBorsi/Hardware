#include <Servo.h>
#include <HX711.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

LiquidCrystal_I2C lcd(0x27, 20, 4);
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
Servo servohopper;

HX711 scale;
const int dataPin = 13;
const int clockPin = 12;
float w1, w2, previous = 0;

int current_command = -1;

void setup() {
  Serial.begin(9600);

  servo1.attach(11);
  servo2.attach(10);
  servo3.attach(4);
  servo4.attach(3);
  servo5.attach(5);
  servohopper.attach(9);
  servo1.write(170);
  servo2.write(90);
  servo3.write(5);
  servo4.write(1);
  servo5.write(100);
  servohopper.write(0);

  scale.begin(dataPin, clockPin);
  scale.set_scale(2955.f);
  scale.tare();
  
  lcd.init();
  lcd.backlight();
}

void loop() {
  if (current_command == -1) { 
    receiveCommand(); 
  } 
  
  else if (current_command == 0) { 
    closeServo1();
    lcd.clear();
    lcd.setCursor(3, 0);  
    lcd.print("BOTECANnected");
    current_command = -1; 
  } 
  
  else if (current_command == 1) { 
    openServo1();
    lcd.clear();
    lcd.setCursor(3, 0);  
    lcd.print("BOTECANnected");
    lcd.setCursor(0, 1);
    lcd.print("Insert Item");
    current_command = -1; 
  } 
  
  else if (current_command == 2) { 
    closeServo1();
    lcd.clear();
    lcd.setCursor(3, 0);  
    lcd.print("BOTECANnected");
    lcd.setCursor(0, 1);
    lcd.print("Item Detected");
    current_command = -1; 
  } 
  
  else if (current_command == 3) { 
    openServo2();
    openServo4();
    lcd.clear();
    lcd.setCursor(3, 0);  
    lcd.print("BOTECANnected");
    lcd.setCursor(0, 1);
    lcd.print("Light Can");
    lcd.setCursor(0, 2);
    lcd.print("Accepted");
    current_command = -1; 
  }
  
  else if (current_command == 4) { 
    openServo2();
    openServo3();
    lcd.clear();
    lcd.setCursor(3, 0);  
    lcd.print("BOTECANnected");
    lcd.setCursor(0, 1);
    lcd.print("Heavy Can");
    lcd.setCursor(0, 2);
    lcd.print("Rejected");
    current_command = -1; 
  } 
  
  else if (current_command == 5) { 
    openServo2();
    current_command = -1; 
  } 
  
  else if (current_command == 6) { 
    openServo2();
    openServo3();
    lcd.clear();
    lcd.setCursor(3, 0);  
    lcd.print("BOTECANnected");
    lcd.setCursor(0, 1);
    lcd.print("Unknown Heavy Object");
    lcd.setCursor(0, 2);
    lcd.print("Rejected");
    current_command = -1; 
  }
  
  else if (current_command == 7) { 
    openServo5();
    delay(1500);
    openServo4();
    lcd.clear();
    lcd.setCursor(3, 0);  
    lcd.print("BOTECANnected");
    lcd.setCursor(0, 1);
    lcd.print("Plastic-Bottle");
    lcd.setCursor(0, 2);
    lcd.print("Accepted");
    current_command = -1; 
  } 
  
  else if (current_command == 8) { 
    openServo3();
    lcd.clear();
    lcd.setCursor(3, 0);  
    lcd.print("BOTECANnected");
    lcd.setCursor(0, 1);
    lcd.print("Non-Bottle Object");
    lcd.setCursor(0, 2);
    lcd.print("Rejected");
    current_command = -1; 
  }
  
  else if (current_command == 9) {
    getWeight();
    current_command = -1;
  }
  
  else if (current_command == 10) {
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
    delay(1500);
    closeServo5();
    current_command = -1; 
  } 
  
  else if (current_command == 14) { 
    closeServo3();
    current_command = -1; 
  }

  else if (current_command == 15) {
    dispense();
    delay(500);
    notdispense();
    current_command = -1;
  }

  delay(100); 
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
  servo4.write(1);
}

void closeServo5() {
  servo5.write(100);
}

void dispense(){
  servohopper.write(85);
}

void notdispense(){
  servohopper.write(0);
}

void openServo1() {
  servo1.write(70);
}

void openServo2() {
  servo2.write(180);
}

void openServo3() {
  servo3.write(110);
}

void openServo4() {
  servo4.write(55);
}

void openServo5() {
  servo5.write(0);
}

void getWeight(){
  w1 = scale.get_units(10);
  delay(100);
  w2 = scale.get_units();
  while ((abs(w1-w2) > 10) && (w1 < 1)) {
    w1 = w2;
    w2 = scale.get_units();
    delay(100);
  }
  float gram = abs(w1);
  sendResponse(String(gram));
}
