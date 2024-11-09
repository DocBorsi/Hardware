
const int relayPin = 13;
const int sensorPin = A0;  // Coin sensor connected to analog pin A0
int dispense = 0; // Number of coins to dispense
int counter = 0;           // Coin counter

void setup() {
  Serial.begin(9600);            // Initialize serial communication
  pinMode(sensorPin, INPUT);     // Set sensor pin as input
  pinMode(relayPin, OUTPUT);     // Set relay pin as output
  digitalWrite(relayPin, LOW);   // Ensure relay is off initially

  Serial.println("Waiting for command...");
}

void loop() {
  // Check if there's data available in the serial buffer
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read the command from serial
    command.trim();  // Remove any trailing newlines or spaces

    // Check for command '0' to dispense 3 coins
    if (command == "0") {
      dispense = 5;      // Set number of coins to dispense
      counter = 0;       // Reset coin counter
      Serial.println("Dispensing 3 coins...");
    }
  }

  // Read the sensor value
  int value = analogRead(sensorPin);

  // If we are still dispensing coins
  if (counter < dispense) {
      digitalWrite(relayPin, HIGH);  // Turn on relay to start dispensing

      // Check if a coin is detected
      if (value > 1022) {
          Serial.print(value);za
          Serial.println("Coin detected");
          counter++;           // Increment coin counter
          delay(90);           // Debounce delay to prevent multiple counts
      }
  } else {
      // Stop dispensing when the required number of coins is reached
      digitalWrite(relayPin, LOW);   // Turn off relay
      dispense = 0;                  // Reset dispense command
  }
}


