import serial
import time

# Initialize serial connection to Arduino (adjust the port and baudrate as needed)
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)

def send_command(command):
    arduino.write((command + '\n').encode())  # Send command to Arduino
    time.sleep(0.1)  # Allow time for Arduino to process the command

    # Read the response from the Arduino
    response = arduino.readline().decode().strip()
    return response

def main():
    while True:
        # Send the "SHOW_WEIGHT" command to Arduino
        response = send_command("SHOW_WEIGHT")
        
        # Print the response from Arduino
        if response:
            print(f"Arduino Response: {response}")
        
        time.sleep(1)  # Wait for 1 second before sending the next command

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program interrupted")
    finally:
        arduino.close()  # Close the serial connection when done
