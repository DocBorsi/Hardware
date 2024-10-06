import RPi.GPIO as GPIO
import time
import serial

# Setup button pin and serial communication
button_pin = 5  # GPIO pin where the button is connected
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Serial communication setup (update the port if necessary)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Give the serial connection time to initialize

try:
    while True:
        if GPIO.input(button_pin) == GPIO.HIGH:  # Button is pressed
            print("Button pressed, sending command to Arduino!")
            ser.write(b'MOVE_SERVO\n')  # Send command to Arduino
            time.sleep(1)  # Debounce delay
        time.sleep(0.1)  # Check every 100ms
except KeyboardInterrupt:
    pass
finally:
    ser.close()  # Close serial connection
    GPIO.cleanup()
