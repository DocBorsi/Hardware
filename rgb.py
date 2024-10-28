import RPi.GPIO as GPIO
import time

# Pin setup
RED_PIN = 17
GREEN_PIN = 27
BLUE_PIN = 22

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

# Create PWM instances with 100Hz frequency
red_pwm = GPIO.PWM(RED_PIN, 100)
green_pwm = GPIO.PWM(GREEN_PIN, 100)
blue_pwm = GPIO.PWM(BLUE_PIN, 100)

# Start PWM with 0 duty cycle (off)
red_pwm.start(0)
green_pwm.start(0)
blue_pwm.start(0)

def set_color(red, green, blue):
    """
    Set the color of the RGB LED.
    Parameters:
    red (int): Duty cycle for red (0-100)
    green (int): Duty cycle for green (0-100)
    blue (int): Duty cycle for blue (0-100)
    """
    red_pwm.ChangeDutyCycle(red)
    green_pwm.ChangeDutyCycle(green)
    blue_pwm.ChangeDutyCycle(blue)

try:
    while True:
        # Example: Cycle through colors
        set_color(100, 0, 0)  # Red
        time.sleep(1)
        set_color(0, 100, 0)  # Green
        time.sleep(1)
        set_color(0, 0, 100)  # Blue
        time.sleep(1)
        set_color(100, 100, 0)  # Yellow
        time.sleep(1)
        set_color(0, 100, 100)  # Cyan
        time.sleep(1)
        set_color(100, 0, 100)  # Magenta
        time.sleep(1)
        set_color(100, 100, 100)  # White
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    # Stop PWM and clean up GPIO
    red_pwm.stop()
    green_pwm.stop()
    blue_pwm.stop()
    GPIO.cleanup()
