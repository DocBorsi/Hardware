import RPi.GPIO as GPIO
import time

# GPIO Pin Definitions
IR_SENSOR_PIN = 17  # GPIO pin where the IR sensor is connected
LED_PIN = 27        # GPIO pin where the LED is connected

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(IR_SENSOR_PIN, GPIO.IN)  # Set up IR sensor pin as input
GPIO.setup(LED_PIN, GPIO.OUT)       # Set up LED pin as output

# Function to turn on/off LED based on sensor state
def check_sensor():
    if GPIO.input(IR_SENSOR_PIN) == GPIO.LOW:  # If the beam is interrupted
        GPIO.output(LED_PIN, GPIO.LOW)  # Turn on LED
        print("not plastic bottle")
    else:
        GPIO.output(LED_PIN, GPIO.HIGH)   # Turn off LED
        print("plastic bottle")

try:
    while True:
        check_sensor()
        time.sleep(0.1)  # Small delay to avoid CPU overuse
except KeyboardInterrupt:
    print("Exiting program")
finally:
    GPIO.cleanup()  # Reset GPIO pins when exiting
