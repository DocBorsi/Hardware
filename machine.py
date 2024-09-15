import RPi.GPIO as GPIO
import serial
import time

class Machine:
    def __init__(self, port) -> None:
        self.arduino = serial.Serial(port, 9600, timeout = 1)
        self.arduino.flush()
        self.available_commands = [0, 1, 2, 3, 4, 5] 

        self.led_pin = 27
        self.inductive_sensor_pin = 17

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)
        GPIO.setup(self.led_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
        Close servo 2
        '''
        self.send_command(2)

    def open_servo_2(self):
        '''
        Open servo 2
        '''
        self.send_command(3)

    def get_distance(self):
        '''
        Get distance from ultrasonic sensor
        '''
        self.send_command(4)
        response = self.get_arduino_response()
        while not response:
            response = self.get_arduino_response()
        return int(response)

    def get_laser_state(self):
        '''
        Get laser state from laser sensor
        '''
        self.send_command(5)
        response = self.get_arduino_response()
        while not response:
            response = self.get_arduino_response()
        return int(response)
    
    def get_weight(self):
        '''
        Get weight from load sensor
        '''
        self.send_command(6)
        response = self.get_arduino_response()
        while not response:
            response = self.get_arduino_response()
        return float(response)
    
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

    def detect_object_from_inductive(self):
        '''
        Get inductive sensor value

        Returns 0 or 1
        '''
        if GPIO.input(self.inductive_sensor_pin) == GPIO.LOW:
            return 1
        return 0
