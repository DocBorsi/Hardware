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
    if machine.get_distance_small() < 9:
        if machine.get_distance_medium() < 9:
            if machine.get_distance_large() < 9:
                return "large"
            return "medium"
        return "small"
    return None
 
total_points = 0
category = ""
size = ""
started = False
finished = False
servo_opened = False
 
last_debounce = time.time() - 3
 
while True:
    current = time.time()
    if not started and (current - last_debounce) > 3:
        button_pressed = machine.get_button_state()
        print(f'Start button pressed: {button_pressed}')
        if button_pressed:
            started = True
            last_debounce = time.time()
            continue
 
    if finished:
        if total_points == 0:
            print('No points')
            finished = False
            started = False
            servo_opened = False
            continue
        
        machine.close_servo_1()
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
        servo_opened = False
 
    if started:
        if (current - last_debounce) > 3:
            button_pressed = machine.get_button_state()
            print(f'Stop button pressed: {button_pressed}')
            if button_pressed:
                last_debounce = current
                print('Button is pressed again, finishing')
                finished = True
                continue
 
        if not servo_opened:
            machine.open_servo_1()
            print('Servo 1 opened')
            servo_opened = True
 
        # Waiting for distance to be less than 20
        time.sleep(2)
        distance = machine.get_distance_tube()
        print (f'Distance:{distance}')
        if distance < 9:
            print (f'Distance:{distance}')
            machine.close_servo1()
            print('Servo 1 closed')
            is_inductive = machine.get_inductive_state()
            print(f'Inductive state: {is_inductive}')
 
            # If inductive (can, metal, etc)
            if is_inductive:
                weight = 0
                retry = 10
                print('Getting weight...')
                while retry > 0:
                    weight = machine.get_weight()
                    if weight is not None:
                        break
                    retry -= 1
                    time.sleep(3)
                else:
                    print('Error getting weight!')
                    machine.open_servo_2_3heavy()
                    # Add closing
                    time.sleep(5)
                    machine.close_servo_2_3()
                    started = False
                    servo_opened = False
                    time.sleep(3)
                    continue
                print(f'Weight: {weight}')
 
                if weight >= 0.30 and weight <= 25.0:
                    print('Weight passed, accept...')
                    machine.open_servo_2_4() # Accept
                    machine.turn_on_led()
                    # Add closing
                    time.sleep(5)
                    machine.close_servo_2_4()
                    category = "can"
                    point = get_points(category, size)
                    total_points += point
                    category = ''
                    size = ''
                    servo_opened = False
                    time.sleep(3)
                    continue
 
                print('Weight did not pass, rejecting...')
                machine.open_servo_2_3heavy()
                # Add closing
                time.sleep(5)
                machine.close_servo_2_3()
                started = False
                time.sleep(3)
                continue
 
            # If not inductive (e.g. plastics)
            if not is_inductive:
                weight = 0
                retry = 10
                print('Getting weight...')
                while retry > 0:
                    weight = machine.get_weight()
                    if weight is not None:
                        break
                    retry -= 1
 
                else:
                    print('Error getting weight!')
                    machine.open_servo_2_3heavy()
                    # Add closing#
                    time.sleep(5)
                    machine.close_servo_2_3()
                    started = False
                    servo_opened = False
                    time.sleep(3)
                    continue 
                print(f'Weight: {weight}')
 
                if weight >= 1.00 and weight <= 25.0:
                    print('Weight passed, accept...')
                    machine.open_servo_2() # Accept
                    machine.turn_on_led()
                    # Add closing
                    time.sleep(5)
                    machine.close_servo2()
                    print('Getting Size')
                    size = get_size()
                    print(f"Size: {size}")

                    if not size:
                        print('Size did not pass')
                        started = False
                        continue
 
                    is_opaque = machine.get_irbreakbeam_state()
                    print(f'Opaque: {is_opaque}')
                    if is_opaque:
                        print(f'Not opaque, accepting...')
                        machine.open_servo_4_5()
                        machine.turn_on_led()
                        time.sleep(5)
                        machine.close_servo_4_5()
                        category = "plastic"
                        point = get_points(category, size)
                        total_points += point
                        category = ''
                        size = ''
                        servo_opened = False
                        time.sleep(3)
                        continue
 
                    print(f'Opaque, rejecting...')
                    machine.open_servo_3()
                    time.sleep(5)
                    machine.close_servo_3()
                    started = False
                    servo_opened = False
                    time.sleep(3)
                    continue
 
                print('Weight did not pass, rejecting...')
                machine.open_servo_2_3()
                # Add closing
                time.sleep(5)
                machine.close_servo_2_3()
                started = False
                servo_opened = False
                time.sleep(3)
                continue