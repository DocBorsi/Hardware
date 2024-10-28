// #define relayPin 13
#define sensorPin A2  // Changed sensor pin to analog pin A0

void setup() {
  Serial.begin(9600);              // Initialize serial communication
  pinMode(sensorPin, INPUT);
  // pinMode(relayPin, OUTPUT);        // Set the relay pin as an output
  // digitalWrite(relayPin, LOW);      // Ensure the relay is initially off
}

void loop() {
  int sensorValue = digitalRead(sensorPin); // Read the analog sensor value

  // Print out the sensor value for debugging
  Serial.print("Sensor Value: ");
  Serial.println(sensorValue);
  delay(500);
}

  // // Check if the value indicates coin detection (you may need to adjust the threshold)
  // if (sensorValue < 750) {  // Example threshold for detection
  //   Serial.println("Coin detected");
  // } else {
  //   Serial.println("No coin detected");
  // }

  // delay(500); // Add a delay for readability



  // if (Serial.available()) {
  //   char input = Serial.read(); // Read the character input

  //   if (input == '1') { // Compare with character '1'
  //     digitalWrite(relayPin, LOW);
  //     Serial.println("not dispensing");
  //   }
  //   else if (input == '2') { // Compare with character '2'
  //     digitalWrite(relayPin, HIGH);
  //     Serial.println("dispensing");
  //   }
  // }

