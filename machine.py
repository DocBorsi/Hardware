import RPi.GPIO as GPIO
from escpos import *
import serial
import time
from signal import signal, SIGTERM, SIGHUP
from rpi_lcd import LCD

class Machine:
    def __init__(self, port) -> None:
        self.arduino = serial.Serial(port, 9600, timeout = 1)
        self.printer = printer.Usb(idVendor=0x0416, idProduct=0x5011, interface=0, in_ep=0x81, out_ep=0x03)
        self.lcd = LCD()
        self.arduino.flush()
        self.available_commands = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

        self.ultrasonic_trig_pin1 = 23  
        self.ultrasonic_echo_pin1 = 24
        self.ultrasonic_trig_pin2 = 25
        self.ultrasonic_echo_pin2 = 8
        self.ultrasonic_trig_pin3 = 12
        self.ultrasonic_echo_pin3 = 16
        self.ultrasonic_trig_pin4 = 20
        self.ultrasonic_echo_pin4 = 21
        self.ultrasonic_trig_pin_bin1 = 9
        self.ultrasonic_echo_pin_bin1 = 11
        self.ultrasonic_trig_pin_bin2 = 14
        self.ultrasonic_echo_pin_bin2 = 15

        self.push_button = 22
        self.led_red1 = 13
        self.led_green1 = 10
        self.led_blue1 = 7
        self.led_red = 5
        self.led_green = 6
        self.led_blue = 26
        self.inductive_sensor_pin = 17
        self.IR_SENSOR_PIN = 27
    
        #GPIO.setmode()
        GPIO.setmode(GPIO.BCM) 
        GPIO.setwarnings(False)
        GPIO.setup(self.ultrasonic_trig_pin1, GPIO.OUT)
        GPIO.setup(self.ultrasonic_echo_pin1, GPIO.IN)
        GPIO.setup(self.ultrasonic_trig_pin2, GPIO.OUT)
        GPIO.setup(self.ultrasonic_echo_pin2, GPIO.IN)
        GPIO.setup(self.ultrasonic_trig_pin3, GPIO.OUT)
        GPIO.setup(self.ultrasonic_echo_pin3, GPIO.IN)
        GPIO.setup(self.ultrasonic_trig_pin4, GPIO.OUT)
        GPIO.setup(self.ultrasonic_echo_pin4, GPIO.IN)
        GPIO.setup(self.ultrasonic_trig_pin_bin1, GPIO.OUT)
        GPIO.setup(self.ultrasonic_echo_pin_bin1, GPIO.IN)
        GPIO.setup(self.ultrasonic_trig_pin_bin2, GPIO.OUT)
        GPIO.setup(self.ultrasonic_echo_pin_bin2, GPIO.IN)

    
        GPIO.setup(self.push_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.led_red1, GPIO.OUT)
        GPIO.setup(self.led_green1, GPIO.OUT)
        GPIO.setup(self.led_blue1, GPIO.OUT)
        GPIO.setup(self.led_red, GPIO.OUT)
        GPIO.setup(self.led_green, GPIO.OUT)
        GPIO.setup(self.led_blue, GPIO.OUT)
        GPIO.setup(self.IR_SENSOR_PIN, GPIO.IN)
        GPIO.setup(self.inductive_sensor_pin, GPIO.IN)

        signal(SIGTERM, self.safe_exit)
        signal(SIGHUP, self.safe_exit)
        
    def safe_exit(self, signum, frame):
        self.lcd.clear()
        GPIO.cleanup()
        exit(1)

    def update_lcd_line(self, text: str, line: int):
        """
        Update a specific line on the LCD display.

        Parameters:
        text (str): The text to display.
        line (int): The line number (1 or 2).
        """
        if line in [1, 2]:
            self.lcd.text(text, line)
        else:
            raise ValueError("LCD only supports line 1 and 2.")

    def clear_lcd(self):
        """Clear the LCD display."""
        self.lcd.clear()

    # Add other methods (e.g., for interacting with Arduino, printer, GPIOs) here.

    def close(self):
        """Clean up resources when exiting."""
        self.lcd.clear()
        GPIO.cleanup()


    def send_command(self, command: int):
        '''
        Send command to Arduino
        can be used to explicitly invoke Arduino operation without calling specific functions\n

        Parameters:
        command(int): Command to send
        '''
        if(command in self.available_commands):
            while True:
                self.arduino.write(bytes(str(command)+'\n','utf-8'))
                time.sleep(0.5)
                response = self.get_arduino_response()
                if (response  == 'ok'):
                    break
        else:
            raise Exception('Unknown command')
        
    def get_arduino_response(self) -> str:
        '''
        Get arduino serial response

        Returns:
        response(str): Arduino response
        '''
        try:
            response = self.arduino.readline().decode('utf-8').rstrip()
        except UnicodeDecodeError:
            response = self.arduino.readline().decode('utf-8').rstrip()
        return response

    def close_servo_1(self):
        '''
        Close servo 1
        '''
        self.send_command(0)

    def open_servo_1(self):
        '''
        Open servo 1
        '''
        self.send_command(1)

    def close_servo1(self):
        '''
        Close servo 1
        '''
        self.send_command(2)

    def open_servo_2_4(self):
        '''
        Open servo 2 and 4
        '''
        self.send_command(3)

    def open_servo_2_3heavy(self):
        '''
        Open servo 2 and 3
        '''
        self.send_command(4)

    def open_servo_2(self):
        '''
        Open servo 2
        '''
        self.send_command(5)

    def open_servo_2_3(self):
        '''
        Open servo 2
        '''
        self.send_command(6)

    def open_servo_4_5(self):
        '''
        Open servo 2
        '''
        self.send_command(7)

    def open_servo_3(self):
        '''
        Open servo 2
        '''
        self.send_command(8)

    def get_weight(self):
        '''
        Get weight from load sensor
        '''
        self.send_command(9)
        time.sleep(3)
        response = self.get_arduino_response()
        try:
            return float(response)
        except:
            return None
        
    def close_servo_2_4(self):
        '''
        Open servo 2 and 4
        '''
        self.send_command(10)

    def close_servo_2_3(self):
        '''
        Open servo 2 and 3
        '''
        self.send_command(11)

    def close_servo2(self):
        '''
        Open servo 2
        '''
        self.send_command(12)

    def close_servo_4_5(self):
        '''
        Open servo 2
        '''
        self.send_command(13)

    def close_servo_3(self):
        '''
        Open servo 2
        '''
        self.send_command(14)

    def dispense_coin (self, amount:int):
        for i in range(amount):
            self.send_command(15)
    
    def bin_is_full(self):
        self.send_command(16)

    def get_distance_tube(self):
        '''
        Get distance from ultrasonic sensor
        '''
        GPIO.output(self.ultrasonic_trig_pin1, True)
        time.sleep(0.00001)
        GPIO.output(self.ultrasonic_trig_pin1, False)
        pulse_start = time.time()
        while GPIO.input(self.ultrasonic_echo_pin1) == 0:
            pulse_start = time.time()
        pulse_end = time.time()
        while GPIO.input(self.ultrasonic_echo_pin1) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        return distance

    def get_distance_small(self):
        '''
        Get distance from ultrasonic sensor
        '''
        GPIO.output(self.ultrasonic_trig_pin4, True)
        time.sleep(0.00001)
        GPIO.output(self.ultrasonic_trig_pin4, False)
        pulse_start = time.time()
        while GPIO.input(self.ultrasonic_echo_pin4) == 0:
            pulse_start = time.time()
        pulse_end = time.time()
        while GPIO.input(self.ultrasonic_echo_pin4) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        return distance
    
    def get_distance_medium(self):
        '''
        Get distance from ultrasonic sensor
        '''
        GPIO.output(self.ultrasonic_trig_pin3, True)
        time.sleep(0.00001)
        GPIO.output(self.ultrasonic_trig_pin3, False)
        pulse_start = time.time()
        while GPIO.input(self.ultrasonic_echo_pin3) == 0:
            pulse_start = time.time()
        pulse_end = time.time()
        while GPIO.input(self.ultrasonic_echo_pin3) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        return distance
      
    def get_distance_large(self):
        '''
        Get distance from ultrasonic sensor
        '''
        GPIO.output(self.ultrasonic_trig_pin2, True)
        time.sleep(0.00001)
        GPIO.output(self.ultrasonic_trig_pin2, False)
        pulse_start = time.time()
        while GPIO.input(self.ultrasonic_echo_pin2) == 0:
            pulse_start = time.time()
        pulse_end = time.time()
        while GPIO.input(self.ultrasonic_echo_pin2) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        return distance
        
    def get_distance_bin1(self):
        '''
        Get distance from ultrasonic sensor
        '''
        GPIO.output(self.ultrasonic_trig_pin_bin1, True)
        time.sleep(0.00001)
        GPIO.output(self.ultrasonic_trig_pin_bin1, False)
        pulse_start = time.time()
        while GPIO.input(self.ultrasonic_echo_pin_bin1) == 0:
            pulse_start = time.time()
        pulse_end = time.time()
        while GPIO.input(self.ultrasonic_echo_pin_bin1) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        return distance
    
    def get_distance_bin2(self):
        '''
        Get distance from ultrasonic sensor
        '''
        GPIO.output(self.ultrasonic_trig_pin_bin2, True)
        time.sleep(0.00001)
        GPIO.output(self.ultrasonic_trig_pin_bin2, False)
        pulse_start = time.time()
        while GPIO.input(self.ultrasonic_echo_pin_bin2) == 0:
            pulse_start = time.time()
        pulse_end = time.time()
        while GPIO.input(self.ultrasonic_echo_pin_bin2) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        return distance

    def get_irbreakbeam_state(self):
        '''
        Get irbreak beam state from laser sensor
        '''
        if GPIO.input(self.IR_SENSOR_PIN) == GPIO.HIGH:
            return 1
        return 0
    
    def get_inductive_state(self):
        '''
        Get inductive sensor value

        Returns 0 or 1
        '''
        if GPIO.input(self.inductive_sensor_pin) == GPIO.LOW:
            return 1
        return 0

    def turn_on_red1(self):
        '''
        Turn on LED light
        '''
        GPIO.output(self.led_red1, GPIO.HIGH)

    def turn_off_red1(self):
        '''
        Turn off LED light
        '''
        GPIO.output(self.led_red1, GPIO.LOW)

    def turn_on_blue1(self):
        '''
        Turn on LED light
        '''
        GPIO.output(self.led_blue1, GPIO.HIGH)

    def turn_off_blue1(self):
        '''
        Turn off LED light
        '''
        GPIO.output(self.led_blue1, GPIO.LOW)

    def turn_on_green1(self):
        '''
        Turn on LED light
        '''
        GPIO.output(self.led_green1, GPIO.HIGH)

    def turn_off_green1(self):
        '''
        Turn off LED light
        '''
        GPIO.output(self.led_green1, GPIO.LOW)

    def turn_on_red(self):
        '''
        Turn on LED light
        '''
        GPIO.output(self.led_red, GPIO.HIGH)

    def turn_off_red(self):
        '''
        Turn off LED light
        '''
        GPIO.output(self.led_red, GPIO.LOW)

    def turn_on_blue(self):
        '''
        Turn on LED light
        '''
        GPIO.output(self.led_blue, GPIO.HIGH)

    def turn_off_blue(self):
        '''
        Turn off LED light
        '''
        GPIO.output(self.led_blue, GPIO.LOW)

    def turn_on_green(self):
        '''
        Turn on LED light
        '''
        GPIO.output(self.led_green, GPIO.HIGH)

    def turn_off_green(self):
        '''
        Turn off LED light
        '''
        GPIO.output(self.led_green, GPIO.LOW)


    def get_button_state(self):
        '''
        Get button state
        '''
        if GPIO.input(self.push_button) == GPIO.LOW:
            return True
        else:
            return False

    def print(self, msg):
        '''
        Print to thermal printer
        '''
        self.printer.text(msg)

    def cut_paper(self):
        '''
        Cut thermal paper
        '''
        self.printer.cut()

    def dispense_coins(self, amount: int):
        '''
        Dispense x amount coins
        '''
        for i in range(amount):
            self.send_command(15)
            time.sleep(0.7)
    

