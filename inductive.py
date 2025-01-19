# Inductive Sensor

import RPi.GPIO as GPIO
import time
import serial

# Use BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Define the GPIO pins
SENSOR_PIN = 4
# LED_PIN = 27  # Choose a GPIO pin for the LED

# Set up the GPIO pins
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Enable pull-up resistor
# GPIO.setup(LED_PIN, GPIO.OUT)

# Set up serial communication (make sure the port matches the Arduino's port)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=0)  # Change '/dev/ttyUSB0' as needed
ser.flush()

try:
    while True:
        # Read the sensor value
        if GPIO.input(SENSOR_PIN) == GPIO.LOW:  # Inverted logic for NPN sensor
            print("Object Detected")
            # GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED ON (active high)
            ser.write(b'1')  # Send '1' to Arduino
        else:
            print("No Object Detected")
            # GPIO.output(LED_PIN, GPIO.LOW)   # Turn LED OFF (active high)
            ser.write(b'0')  # Send '0' to Arduino
        
        # Delay to reduce CPU usage
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Exiting program")

finally:
    # Clean up GPIO settings before exiting
    GPIO.cleanup()
