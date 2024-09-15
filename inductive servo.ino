#include <Servo.h>

Servo myServo;  // Create a servo object
int pos = 0;    // Variable to store the servo position

void setup() {
  Serial.begin(9600);  // Start serial communication
  myServo.attach(13);   // Attach the servo to pin 9
  myServo.write(0);    // Set initial position of the servo to 0 degrees
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();  // Read the incoming byte

    if (command == '1') {
      // Move the servo to 180 degrees when object is detected
      myServo.write(180);
      delay(2000);  // Wait for 1 second
    } else if (command == '0') {
      // Move the servo back to 0 degrees if no object is detected
      myServo.write(0);
      delay(2000);  // Wait for 1 second
    }
  }
}
