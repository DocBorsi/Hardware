from machine import Machine
#import requests


machine = Machine(port='/dev/ttyACM0')

# buttonState = machine.button_State()
# inductiveState = machine.detect_object_from_inductive()
# weightState = machine.get_weight()
# irbreakbeamState = machine.get_irbreakbeam_state()
# while True:
#     buttonState = machine.button_State()
#     if not buttonState:
#         distance_tube1 = machine.get_distance_tube1()
#         if distance_tube1 < 20:
#             if not inductiveState: # For can
#                 if weightState is None:
#                     machine.close_servo_2()
#                 else:
#                     if 5.00 <= weightState <= 50.0:
#                         machine.open_servo_2_4() # For accept
#                     elif weightState > 50.0:
#                         machine.open_servo_2_3() # For reject
#             elif inductiveState: # !can
#                 if weightState is None:
#                     machine.close_servo_2()
#                 else:
#                     if 5.00 <= weightState <= 50.0:
#                         machine.open_servo_2()
#                         # Wait for small, then medium, large
#                         distance_tubesmall = machine.get_distance_small()
#                         distance_tubemedium = machine.get_distance_medium()
#                         distance_tubelarge = machine.get_distance_large()
#                         if distance_tubesmall < 20:
#                             if not irbreakbeamState:
#                                 machine.open_servo_4_5() # Accept
#                             else:
#                                 machine.open_servo_3() # Reject
#                         else:  
#                             irbreakbeamState()
#                     elif weightState > 50.0:
#                         machine.open_servo_2_3() # reject
#                     else:
#                         machine.close_servo_2() # close
#         else:
#             pass
#     else:
#         pass


# Wait for button to be pressed
# If button pressed, check if type is plastic or can, wait for distance
# If can, wait to stabilize, check weight
#   If 5 < weight < 50, then accept
#   else reject
# If plastic, wait to stabilize, check weight
#   If 5 < weight < 50, then check size
#   Check ir beam state:
#       If not, accept
#       else reject
#   Else reject
'''
def create_ticket(category, size):
    params = {
        "category": category,
        "size": size,
        "key": "boteweb"
    }
    response = requests.get(f"http://127.0.0.1:8000/ticket/create/?", params=params)
    ticket_data = response.json()
    return ticket_data
'''
def get_size():
    if machine.get_distance_small():
        if machine.get_distance_medium():
            if machine.get_distance_large():
                return "large"
            return "medium"
        return "small"
    return None

category = ""
size = ""
started = False
finished = False

while True:
    if not started:
        button_pressed = machine.button_State()
        if button_pressed:
            started = True
    '''
    if finished:
        data = create_ticket(category, size)
        print(f"New ticket: {data.get('code')} - {data.get('point')}")
        category = ""
        size = ""
        finished = False
        started = False
    '''
    if started:
        machine.open_servo_1()
        # Waiting for distance to be less than 20
        distance = machine.get_distance_tube1()
        if distance < 20:
            machine.close_servo_2()
            is_inductive = machine.detect_object_from_inductive()
            # If inductive (can, metal, etc)
            if is_inductive:
                weight = -1
                while True:
                    weight = machine.get_weight()
                    if weight is not None:
                        break
                if weight == -1:
                    raise Exception("Error getting weight")
                
                if weight >= 5.00 and weight <= 50.0:
                    machine.open_servo_2_4() # Accept
                    machine.turn_on_led()
                    category = "can"
                    finished = True
                    continue
                
                machine.open_servo_2_3()
                started = False
                continue

            # If not inductive (e.g. plastics)
            if not is_inductive:
                weight = -1
                while True:
                    weight = machine.get_weight()
                    if weight is not None:
                        break
                if weight == -1:
                    raise Exception("Error getting weight")
                
                size = get_size()
                if not size:
                    machine.open_servo_2_3()
                    started = False
                    continue
                
                print(f"Size: {size}")

                is_opaque = machine.get_irbreakbeam_state()
                if not is_opaque:
                    machine.open_servo_2_4()
                    machine.turn_on_led()
                    category = "plastic"
                    finished = True
                    continue
                machine.open_servo_2_3()
                started = False
                continue
