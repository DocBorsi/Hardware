#include <Servo.h>

Servo servo1;  // Servo for plastic bottle
Servo servo2;  // Servo for non-plastic object

const int servo1Pin = 13;
const int servo2Pin = 12;

void setup() {
  servo1.attach(servo1Pin);
  servo2.attach(servo2Pin);
  Serial.begin(9600);
  servo1.write(0);  // Initial position for servo 1
  servo2.write(0);  // Initial position for servo 2
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();
    
    switch (command) {
      case 'A':  // Open first servo
        servo1.write(180);
        Serial.println("Servo 1 Opened");
        break;
      case 'B':  // Close first servo
        servo1.write(0);
        Serial.println("Servo 1 Closed");
        break;
      case 'C':  // Open second servo
        servo2.write(180);
        Serial.println("Servo 2 Opened");
        break;
      case 'D':  // Close second servo
        servo2.write(0);
        Serial.println("Servo 2 Closed");
        break;
      default:
        Serial.println("Unknown command");
        break;
    }
  }
}
