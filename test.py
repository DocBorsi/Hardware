from machine import Machine
# import requests

machine = Machine (port='/dev/ttyACM0')

#machine.close_servo_1()
#machine.open_servo_1()
#machine.get_distance_tube1()
#machine.open_servo_2()
# machine.turn_on_led()
# value = machine.detect_object_from_inductive()
# print(value)

#params = {
#    "category": "plastic",
#    "size": "large",
#    "key": "boteweb"
#}
#response = requests.get(f"http://127.0.0.1:8000/ticket/create/?", params=params)
#ticket_data = response.json()
#push = Machine.button_State()
#if push is True:
#machine.turn_on_led()
