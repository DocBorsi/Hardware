#include <Servo.h>
#include <HX711.h>

Servo servo1; 
Servo servo2; 

const int ultrasonicTrigPin = 11; 
const int ultrasonicEchoPin = 10;
const int laserPin = 13;  

HX711 scale;
float w1, w2, previous = 0;
uint8_t dataPin = 13;
uint8_t clockPin = 12;

int current_command = -1; 

void setup() {
  Serial.begin(9600); 

  servo1.attach(4);
  servo2.attach(6); 
  servo1.write(0); 
  servo2.write(0); 

  pinMode(ultrasonicTrigPin, OUTPUT);
  pinMode(ultrasonicEchoPin, INPUT);

  scale.begin(dataPin, clockPin);
  scale.set_scale(451.57738095);
  scale.tare(); 
}

void loop() { 
  if(current_command == -1) { 
    receiveCommand(); 
  } 

  else if(current_command == 0) { 
    closeServo1();
    current_command = -1; 
  } 

  else if(current_command == 1) { 
    openServo1();
    current_command = -1; 
  } 

  else if(current_command == 2) { 
    closeServo2();
    current_command = -1; 
  } 

  else if(current_command == 3) { 
    openServo2();
    current_command = -1; 
  } 

  else if(current_command == 4) { 
    int distance = getDistance();
    sendResponse(String(distance));
    current_command = -1; 
  } 

  else if(current_command == 5) { 
    int laserState = getLaserState();
    sendResponse(String(laserState));
    current_command = -1; 
  } 

  else if(current_command == 6) { 
    double weight = getWeight();
    sendResponse(String(weight));
    current_command = -1; 
  } 
} 

void receiveCommand() {
  if(Serial.available()){
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
}

void openServo1() {
  servo1.write(180);
}

void closeServo2() {
  servo1.write(0);
}

void openServo2() {
  servo1.write(180);
}

int getDistance() {
  int distance = 0;
  long duration = pulseIn(ultrasonicEchoPin, HIGH, 30000);
  if (duration == 0) {
    distance = 400; 
  } else {
    distance = duration * 0.034 / 2;  
  }
  return distance;
}

int getLaserState() {
  int laserState = digitalRead(laserPin);
  return lasertState;
}

double getWeight(){
  w1 = scale.get_units(10);
  delay(100);
  w2 = scale.get_units();
  while (abs(w1-w2)>10)
  {
    w1 = w2;
    w2 = scale.get_units();
    delay (100);
  }
  double kilogram = w1/1000;
  return kilogram;
}
