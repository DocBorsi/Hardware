import serial
import time

# Set up the serial connection (check the correct port)
arduino_port = '/dev/ttyUSB0'  # Replace with your Arduino's port
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

time.sleep(0.5)  # Allow time for the connection to establish

def get_weight():
    ser.write(b'r')  # Send command to Arduino to read weight
    time.sleep(0.5)  # Wait for Arduino to respond
    while ser.in_waiting == 0:  # Wait for response
        pass
    weight = ser.readline().decode('utf-8').strip()  # Read weight
    return weight

try:
    while True:
        weight = get_weight()
        print(weight)  # Print the weight received from Arduino
        time.sleep(0.5)  # Delay between readings
except KeyboardInterrupt:
    print("Program stopped.")
finally:
    ser.close()  # Close the serial connection
