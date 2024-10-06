from machine import Machine
import requests


machine = Machine(port='/dev/ttyACM0')

def create_ticket(category, size):
    params = {
        "category": category,
        "size": size,
        "key": "boteweb"
    }
    response = requests.get(f"http://127.0.0.1:8000/ticket/create/?", params=params)
    ticket_data = response.json()
    return ticket_data

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
        button_pressed = machine.get_button_state()
        if button_pressed:
            started = True
    
    if finished:
        data = create_ticket(category, size)
        print(f"New ticket: {data.get('code')} - {data.get('point')}")
        category = ""
        size = ""
        finished = False
        started = False
    
    if started:
        machine.open_servo_1()
        # Waiting for distance to be less than 20
        distance = machine.get_distance_tube()
        if distance < 20:
            machine.close_servo_2()
            is_inductive = machine.get_inductive_state()
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
