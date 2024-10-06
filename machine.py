import RPi.GPIO as GPIO
import serial
import time

class Machine:
    def __init__(self, port) -> None:
        self.arduino = serial.Serial(port, 9600, timeout = 1)
        self.arduino.flush()
        self.available_commands = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

        self.ultrasonic_trig_pin1 = 23
        self.ultrasonic_echo_pin1 = 12
        self.ultrasonic_trig_pin2 = 16
        self.ultrasonic_echo_pin2 = 24
        self.ultrasonic_trig_pin3 = 25
        self.ultrasonic_echo_pin3 = 20
        self.ultrasonic_trig_pin4 = 21
        self.ultrasonic_echo_pin4 = 8

        self.push_button = 5
        self.led_pin = 6
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
    
        GPIO.setup(self.push_button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.setup(self.led_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.IR_SENSOR_PIN, GPIO.IN)
        GPIO.setup(self.inductive_sensor_pin, GPIO.IN)
        

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

    def close_servo_2(self):
        '''
        Close servo 1
        '''
        self.send_command(2)

    def open_servo_2_4(self):
        '''
        Open servo 2 and 4
        '''
        self.send_command(3)

    def open_servo_2_3(self):
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

        self.get_arduino_response()
        weight_data = self.arduino.readline().decode('utf-8').strip()  # Read the weight data
        
        if weight_data == "Waiting":
            return None  # Weight is not stable yet
        else:
            try:
                return float(weight_data)  # Convert weight to a float
            except ValueError:
                return None  # Return None if invalid data is received


    def get_distance_tube1(self):
        '''
        Get distance from ultrasonic sensor
        '''
        # GPIO.output(self.ultrasonic_trig_pin1, GPIO.LOW)
        # time.sleep(0.000002)
        # GPIO.output(self.ultrasonic_trig_pin1, GPIO.HIGH)
        # time.sleep(0.00001)
        # GPIO.output(self.ultrasonic_trig_pin1, GPIO.LOW)
        GPIO.output(self.ultrasonic_trig_pin1, True)
        time.sleep(0.00001)
        GPIO.output(self.ultrasonic_trig_pin1, False)
        while GPIO.input(self.ultrasonic_echo_pin1) == 0:
            pulse_start = time.time()
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
        # GPIO.output(self.ultrasonic_trig_pin2, GPIO.LOW)
        # time.sleep(0.000002)
        # GPIO.output(self.ultrasonic_trig_pin2, GPIO.HIGH)
        # time.sleep(0.00001)
        # GPIO.output(self.ultrasonic_trig_pin2, GPIO.LOW)
        GPIO.output(self.ultrasonic_trig_pin2, True)
        time.sleep(0.00001)
        GPIO.output(self.ultrasonic_trig_pin2, False)
        while GPIO.input(self.ultrasonic_echo_pin2) == 0:
            pulse_start = time.time()
        while GPIO.input(self.ultrasonic_echo_pin2) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        return distance
    
    def get_distance_medium(self):
        '''
        Get distance from ultrasonic sensor
        '''
        # GPIO.output(self.ultrasonic_trig_pin3, GPIO.LOW)
        # time.sleep(0.000002)
        # GPIO.output(self.ultrasonic_trig_pin3, GPIO.HIGH)
        # time.sleep(0.00001)
        # GPIO.output(self.ultrasonic_trig_pin3, GPIO.LOW)
        GPIO.output(self.ultrasonic_trig_pin3, True)
        time.sleep(0.00001)
        GPIO.output(self.ultrasonic_trig_pin3, False)
        while GPIO.input(self.ultrasonic_echo_pin3) == 0:
            pulse_start = time.time()
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
        # GPIO.output(self.ultrasonic_trig_pin4, GPIO.LOW)
        # time.sleep(0.000002)
        # GPIO.output(self.ultrasonic_trig_pin4, GPIO.HIGH)
        # time.sleep(0.00001)
        # GPIO.output(self.ultrasonic_trig_pin4, GPIO.LOW)
        GPIO.output(self.ultrasonic_trig_pin4, True)
        time.sleep(0.00001)
        GPIO.output(self.ultrasonic_trig_pin4, False)
        while GPIO.input(self.ultrasonic_echo_pin4) == 0:
            pulse_start = time.time()
        while GPIO.input(self.ultrasonic_echo_pin4) == 1:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        return distance
        
    def get_irbreakbeam_state(self):
        '''
        Get irbreak beam state from laser sensor
        '''
        if GPIO.input(self.IR_SENSOR_PIN) == GPIO.LOW:
            return 1
        return 0
    
    def detect_object_from_inductive(self):
        '''
        Get inductive sensor value

        Returns 0 or 1
        '''
        if GPIO.input(self.inductive_sensor_pin) == GPIO.HIGH:
            return 1
        return 0
    
    def turn_on_led(self):
        '''
        Turn on LED light
        '''
        GPIO.output(self.led_pin, GPIO.HIGH)

    def turn_off_led(self):
        '''
        Turn off LED light
        '''
        GPIO.output(self.led_pin, GPIO.LOW)


    def button_State(self):
        # Check if the push button is pressed (assuming HIGH means pressed)
        if GPIO.input(self.push_button) == GPIO.HIGH:
            return True  # Button pressed
        else:
            return False  # Button not pressed
