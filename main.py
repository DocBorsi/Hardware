from machine import Machine

machine = Machine(port='/dev/ttyUSB0')

buttonState = machine.button_State()
inductiveState = machine.detect_object_from_inductive()
weightState = machine.get_weight()
irbreakbeamState = machine.get_irbreakbeam_state()


if not buttonState:
    distance_tube1 = machine.get_distance_tube1()
    if distance_tube1 < 20:
        if not inductiveState:
            if weightState is None:
                machine.close_servo_2()
            else:
                if 5.00 <= weightState <= 50.0:
                    machine.open_servo_2_4()
                elif weightState > 50.0:
                    machine.open_servo_2_3()
        elif inductiveState:
            if weightState is None:
                machine.close_servo_2()
            else:
                if 5.00 <= weightState <= 50.0:
                    machine.open_servo_2()
                    distance_tubesmall = machine.get_distance_small()
                    distance_tubemedium = machine.get_distance_medium()
                    distance_tubelarge = machine.get_distance_large()
                    if distance_tubesmall < 20:
                        if not irbreakbeamState:
                            machine.open_servo_4_5()
                        else:
                            machine.open_servo_3()
                    else:  
                        irbreakbeamState()
                elif weightState > 50.0:
                    machine.open_servo_2_3()
                else:
                    machine.close_servo_2()
    else:
        pass
else:
    pass
