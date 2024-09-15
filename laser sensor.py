
import serial
import RPi.GPIO as GPIO
import time

# Serial port configuration
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Adjust the port name as needed

# Setup GPIO servo1_pin = 4 servo2_pin = 6
laser_pin = 17
ultrasonic_trig_pin = 27
ultrasonic_echo_pin = 22

GPIO.setmode(GPIO.BCM) 
# GPIO.setup(servo1_pin, GPIO.OUT)
# GPIO.setup(servo2_pin, GPIO.OUT)
GPIO.setup(laser_pin, GPIO.IN)
GPIO.setup(ultrasonic_trig_pin, GPIO.OUT)
GPIO.setup(ultrasonic_echo_pin, GPIO.IN)

def get_distance():
    GPIO.output(ultrasonic_trig_pin, GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(ultrasonic_trig_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(ultrasonic_trig_pin, GPIO.LOW)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(ultrasonic_echo_pin) == GPIO.LOW:
        start_time = time.time()

    while GPIO.input(ultrasonic_echo_pin) == GPIO.HIGH:
        stop_time = time.time()

    duration = stop_time - start_time
    distance = duration * 34300 / 2

    return distance

try:
    while True:
        laser_state = GPIO.input(laser_pin)
        print(f"Laser State: {laser_state}")

        distance = get_distance()
        print(f"Distance: {distance:.2f} cm")

        if laser_state == GPIO.LOW:  # Laser connection is not broken
            if distance < 20:
                ser.write(b'A')  # Command to open the first servo
                print("Plastic bottle detected and accepted.")
            else:
                ser.write(b'B')  # Command to close the first servo
                print("No object detected.")
        else:  # Laser connection is broken
            if distance < 20:
                ser.write(b'C')  # Command to open the second servo
                print("Non-plastic object detected and rejected.")
            else:
                ser.write(b'D')  # Command to close the second servo
                print("No object detected.")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Program stopped")

finally:
    ser.close()
    GPIO.cleanup()
