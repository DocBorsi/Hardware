import serial
import time

# Set up serial communication with Arduino
arduino_serial = serial.Serial('/dev/ttyACM0', 9600, timeout=1)  # Adjust port if necessary
time.sleep(2)  # Wait for the serial connection to initialize

try:
    while True:
        # Read the data from Arduino
        if arduino_serial.in_waiting > 0:
            weight = arduino_serial.readline().decode('utf-8').strip()
            print(f"Weight: {weight} grams")

except KeyboardInterrupt:
    print("Serial communication stopped")

finally:
    arduino_serial.close()  # Close the serial connection
