from machine import Machine

machine = Machine(port='/dev/ttyUSB0')

laser_state = machine.get_laser_state()

if not laser_state:
    distance = machine.get_distance()
    if distance < 20:
        machine.open_servo_1()
    else:
        machine.close_servo_1()
else:
    pass

if machine.detect_object_from_inductive():
    machine.turn_on_led()
else:
    machine.turn_off_led()
