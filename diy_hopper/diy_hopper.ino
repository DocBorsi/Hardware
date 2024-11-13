#include <Servo.h>

const int trigPin = 12;
const int echoPin = 9;
const int laser = 8;
const int sensor = 13;

const int redPin = 5;
const int greenPin = 6;
const int bluePin = 7;
const int buzzerPin = 4;

Servo myServo;
int pos = 0;
int thresholdDistance = 10;

void setup() {
  Serial.begin(9600);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(sensor, INPUT);
  pinMode(laser, OUTPUT);

  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);

  pinMode(buzzerPin, OUTPUT);
  myServo.attach(11);
  myServo.write(0);
  digitalWrite(laser, HIGH);
}

void loop() {
  int irState = digitalRead(sensor);

  // RGB LED and Buzzer control
  if (irState == HIGH) {
    digitalWrite(redPin, LOW);
    digitalWrite(greenPin, HIGH);
    digitalWrite(bluePin, LOW);
    digitalWrite(buzzerPin, LOW);
  } 
  else {
    digitalWrite(redPin, HIGH);
    digitalWrite(greenPin, LOW);
    digitalWrite(bluePin, LOW);

    // Buzzer with modified delay
    digitalWrite(buzzerPin, HIGH);
    delay(100);
    digitalWrite(buzzerPin, LOW);
    delay(100);
  }
  
  // Ultrasonic sensor
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  long duration = pulseIn(echoPin, HIGH);
  int distance = (duration > 0) ? duration * 0.034 / 2 : 0;

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.print(" cm, IR Sensor: ");
  Serial.println(irState == HIGH ? "Object Detected" : "No Object");

  // Servo control based on distance or IR sensor
  if (distance < thresholdDistance || irState == HIGH) {
    // Move the servo if within threshold or IR sensor detects an object
    for (pos = 0; pos <= 90; pos += 1) {
      myServo.write(pos);
      delay(5);
    }
    for (pos = 90; pos >= 0; pos -= 1) {
      myServo.write(pos);
      delay(5);
    }
  } else if (distance > thresholdDistance || irState == LOW)
    {
    // Stop the servo if distance is greater than threshold
    myServo.write(0);  // Keep the servo at 0 degrees when no object is detected
  }

  delay(100);
}
