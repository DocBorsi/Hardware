import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711

def cleanAndExit():
    print("Cleaning up...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Suppress warnings if the GPIO pins are already in use

hx = HX711(dout_pin=23, pd_sck_pin=24)

# Stabilization variables
previousWeight = 0.0
stableCounter = 0
stabilityThreshold = 10  # Number of consecutive stable readings required

try:
    # Start connection to HX711
    hx.reset()
    time.sleep(0.5)  # Load cell gets 500ms of time to stabilize

    # Set the scale (calibration factor)
    hx.set_scale(2550.0)  # This line sets the calibration factor for the load cell
    hx.tare()
    print("Tare done! Add weight now...")

    while True:
        try:
            # Retrieve data from the load cell
            weight = hx.get_weight(5)  # Get the weight, average over 5 readings
            print(f"Weight: {weight:.2f} g")

            # Check if the weight is stable
            if abs(weight - previousWeight) < 1.0:  # Change in weight is less than 1 gram
                stableCounter += 1  # Increase stable reading count
            else:
                stableCounter = 0  # Reset counter if the weight changes significantly

            previousWeight = weight  # Update the previous weight for the next loop

            if stableCounter >= stabilityThreshold:  # Check if the weight has been stable for enough readings
                if 5.0 <= weight <= 48.0:
                    print("Item Accepted")
                elif weight > 48.0:
                    print("Item Rejected")
                else:
                    print("Insert Item")
            else:
                print("Waiting for stable weight...")

            time.sleep(0.1)  # Small delay to prevent excessive updates

        except Exception as e:
            print(f"Error reading weight: {e}")
            time.sleep(1)  # Wait a bit before trying again

except (KeyboardInterrupt, SystemExit):
    cleanAndExit()