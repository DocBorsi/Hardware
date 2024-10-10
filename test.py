from machine import Machine
#import time
# import requests

machine = Machine (port='/dev/ttyACM0')
# v = machine.get_distance_tube()
# print(v)
# while True:
#     machine.send_command(9)
#     time.sleep(3)
#     response = machine.get_arduino_response()
#     print(response)
# machine.send_command(9)
# time.sleep(3)
# print(machine.get_arduino_response())
#machine.close_servo_1()
#machine.open_servo_1()
#machine.open_servo_2_3heavy()
#machine.open_servo_3()
#machine.open_servo_4_5()
# machine.print("TEST")
# print (w)
# while w != 'e':
#     machine.open_servo_2()
# # machine.turn_on_led()
# value = machine.detect_object_from_inductive()
# print(value)
value = machine.get_irbreakbeam_state()
print(value)
#weight = machine.get_weight()
# # # 
# if weight >= 1:
#     machine.open_servo_2()
# print(weight*10)


# time.sleep(5)
# while True:
#     value = machine.get_button_state()
#     print(value)

#params = {
#    "category": "plastic",
#    "size": "large",
#    "key": "boteweb"
#}
#response = requests.get(f"http://127.0.0.1:8000/ticket/create/?", params=params)
#ticket_data = response.json()
#push = Machine.button_State()


