from machine import Machine
#import time
# import requests

machine = Machine (port='/dev/ttyACM0')
s = machine.get_distance_small()
print(s)
v = machine.get_distance_medium()
print(v)
l = machine.get_distance_large()
print(l)

#machine.get_distance_small()
# machine.open_servo_1()
# machine.open_servo_2()
# machine.open_servo_3()
# machine.open_servo_4_5()
# time.sleep(1)
# machine.close_servo_1()
# machine.close_servo2()
# machine.close_servo_3()
# machine.close_servo_4_5()

# if s <8:
#     print(s)
#     m = machine.get_distance_medium()
#     print(m)
#     l = machine.get_distance_large()
#     print(l)

# while True:
#     machine.send_command(9)
#     time.sleep(3)
#     response = machine.get_arduino_response()
#     print(response)
# machine.send_command(9)
# time.sleep(3)
# print(machine.get_arduino_response())
# machine.open_servo_2_4()
# time.sleep(1)
# machine.close_servo_2_4()
# machine.open_servo_2_3heavy()

# machine.print("TEST")
# print (w)
# while w != 'e':
#     machine.open_servo_2()
# # machine.turn_on_led()
# value = machine.get_inductive_state()
# print(value)
# value = machine.get_irbreakbeam_state()
# print(value)
#weight = machine.get_weight()
# # # 
# if weight >= 1:
#     machine.open_servo_2()
# print(weight*10)

# while True:
#     # Check if the button is pressed
#     button_pressed = machine.get_button_state()
#     if button_pressed:
#         # Open servo 1 when the button is pressed
#         machine.open_servo_1()
#         print("Servo 1 opened")
        
#         # Start monitoring with ultrasonic sensor
#         while True:
#             distance = machine.get_distance_tube()  # Get the distance from ultrasonic sensor
            
#             # Check if the distance is less than 8
#             if distance <8:
#                 # Close servo 1 if the distance is less than 8
#                 machine.close_servo_1()
#                 print("Servo 1 closed due to object detected within 8 cm")
#                 machine.open_servo_2_4()
#                 machine.open_servo_1()
#                 time.sleep(1)
#                 machine.close_servo_2_4()
#                 break  # Exit the loop to stop monitoring
#             button_pressed == False
#             # You can add a small sleep to avoid excessive CPU usage
#             time.sleep(0.1)  # Adjust this delay as needed

# # time.sleep(5)
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


