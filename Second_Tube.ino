#include <Servo.h>

Servo servo1;  // Servo that opens when a plastic bottle is detected
Servo servo2;  // Servo that opens when a non-plastic object is detected

const int laserPin = 13;           // Pin connected to the laser receiver
const int ultrasonicTrigPin = 11;  // Pin connected to the ultrasonic sensor trig
const int ultrasonicEchoPin = 10;  // Pin connected to the ultrasonic sensor echo

long duration;
int distance;

void setup() {
  servo1.attach(4);   // Servo 1 attached to pin 6
  servo2.attach(6);   // Servo 2 attached to pin 4
  pinMode(laserPin, INPUT);
  pinMode(ultrasonicTrigPin, OUTPUT);
  pinMode(ultrasonicEchoPin, INPUT);
  servo1.write(0);  // Initial position for servo 1
  servo2.write(0);  // Initial position for servo 2
  Serial.begin(9600);  // Back to the original baud rate
  Serial.println("System initialized.");
}

void loop() {
  int laserState = digitalRead(laserPin);
  Serial.print("Laser State: ");
  Serial.println(laserState);

  // Send a pulse to the ultrasonic sensor
  digitalWrite(ultrasonicTrigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(ultrasonicTrigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(ultrasonicTrigPin, LOW);

  // Read the echo pin to get the distance
  duration = pulseIn(ultrasonicEchoPin, HIGH, 30000);  // Added timeout of 30ms
  if (duration == 0) {
    Serial.println("Ultrasonic sensor timeout");
    distance = 400;  // Set a large distance if timeout occurs
  } else {
    distance = duration * 0.034 / 2;  // Convert duration to distance in cm
  }
  Serial.print("Distance: ");
  Serial.println(distance);

  if (laserState == LOW) {  // Laser connection is not broken
    if (distance < 20) {  // Object detected within 20 cm
      servo1.write(180);  // Open the first servo
      Serial.println("Plastic bottle detected and accepted.");
    } else {
      servo1.write(0);  // Keep the first servo closed
      Serial.println("No object detected.");
    }
  } else {  // Laser connection is broken
    if (distance < 20) {  // Object detected within 20 cm
      servo2.write(180);  // Open the second servo
      Serial.println("Non-plastic object detected and rejected.");
    } else {
      servo2.write(0);  // Keep the second servo closed
      Serial.println("No object detected.");
    }
  }

  delay(500);  // Reduced delay to 500ms for faster responsiveness
}

