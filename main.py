from machine import Machine
import requests
import time


machine = Machine(port='/dev/ttyACM0')

def get_points(category, size):
    point_map = {
        "can": 5,
        "small": 3,
        "medium": 7,
        "large": 10
    }
    if category == "can":
        points = point_map.get("can", 0)
    elif category == "plastic":
        points = point_map.get(size)
    else:
        points = 0
    return points

def create_ticket(points):
    params = {
        "points": points
    }
    response = requests.get(f"http://127.0.0.1:8000/point/create/?", params=params)
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

total_points = 0
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
        if total_points == 0:
            print('No points')
            finished = False
            started = False
            continue
        
        data = create_ticket(total_points)
        print(f"New ticket: {data.get('code')} - {data.get('point')}")
        machine.print("********************************")
        machine.print(f"New ticket: {data.get('code')} - {data.get('point')}")
        machine.print("********************************")
        machine.cut_paper()
        category = ""
        size = ""
        total_points = 0
        finished = False
        started = False
    
    if started:
        button_pressed = machine.get_button_state()
        if button_pressed:
            finished = True
            continue

        machine.open_servo_1()
        # Waiting for distance to be less than 20
        distance = machine.get_distance_tube()
        if distance < 20:
            machine.close_servo_2()
            is_inductive = machine.get_inductive_state()
            # If inductive (can, metal, etc)
            if is_inductive:
                weight = 0
                retry = 10
                while retry > 0:
                    weight = machine.get_weight()
                    if weight is not None:
                        break
                    retry -= 1
                else:
                    print('Error getting weight!')
                    machine.open_servo_2_3heavy()
                    # Add closing
                    started = False
                    continue 
                
                if weight >= 5.00 and weight <= 50.0:
                    machine.open_servo_2_4() # Accept
                    machine.turn_on_led()
                    # Add closing
                    category = "can"
                    point = get_points(category, size)
                    total_points += point
                    category = ''
                    size = ''
                    continue
                
                machine.open_servo_2_3heavy()
                # Add closing
                started = False
                continue

            # If not inductive (e.g. plastics)
            if not is_inductive:
                weight = 0
                retry = 10
                while retry > 0:
                    weight = machine.get_weight()
                    if weight is not None:
                        break
                    retry -= 1
                else:
                    print('Error getting weight!')
                    machine.open_servo_2_3heavy()
                    # Add closing
                    started = False
                    continue 
                
                size = get_size()
                if not size:
                    started = False
                    continue
                
                print(f"Size: {size}")

                is_opaque = machine.get_irbreakbeam_state()
                if not is_opaque:
                    machine.open_servo_4_5()
                    machine.turn_on_led()
                    category = "plastic"
                    point = get_points(category, size)
                    total_points += point
                    category = ''
                    size = ''
                    continue
                machine.open_servo_3()
                started = False
                continue
