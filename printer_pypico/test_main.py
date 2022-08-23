from machine import Pin, UART, reset
import time
import rp2

device_id = '3'
master_command = ""
execute_flag = False
running_state = 0
main_state = 0
debugging_flag = False

printer_state = 0
printer_state_timer = 0

origin_flag = False
origin_state_timer = 0
origin_state = 0
#======================================================================================================
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def run_motor1():
    wrap_target()
    set(pins, 1)   [31]
    nop()
    set(pins, 0)   [31]
    nop()
    wrap()

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def run_motor2():
    wrap_target()
    set(pins, 1)   [31]
    nop()
    set(pins, 0)   [31]
    nop()
    wrap()

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def run_motor3():
    wrap_target()
    set(pins, 1)   [31]
    nop()
    set(pins, 0)   [31]
    nop()
    wrap()

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def run_motor4():
    wrap_target()
    set(pins, 1)   [31]
    nop()
    set(pins, 0)   [31]
    nop()
    wrap()

#======================================================================================================

current_silo = 0
run_printer_flag = False
motor_state = 0
motor_timer = 0
# ========= assigned direction pin ===========
duo_switch = Pin(27,Pin.IN,Pin.PULL_UP)
slap_switch = Pin(20,Pin.IN,Pin.PULL_UP)
motor1_dir_pin = Pin(12,Pin.OUT)                    # paper roller motor
motor2_dir_pin = Pin(14,Pin.OUT)                    # slap motor
# motor3_dir_pin = Pin(21,Pin.OUT)
# motor4_dir_pin = Pin(27,Pin.OUT)
slap_target_pulse = 1000
# ========== debug parameters =====
debug_roller_motor_forward = False
debug_roller_motor_backward = False
debug_slap_motor_forward = False
debug_slap_motor_backward = False

device_link = UART(0, baudrate=115200, bits=8, parity=None, stop=1,tx=Pin(0), rx=Pin(1),timeout=1000)
device_link.read()              # clear data in serial port buffer

motor1_controller = rp2.StateMachine(0, run_motor1, freq=20000, set_base=Pin(13))      # GPIO13 => pulse, GPIO12 => direction
motor2_controller = rp2.StateMachine(1, run_motor2, freq=20000, set_base=Pin(15))      # GPIO15 => pulse, GPIO14 => direction
# motor1_controller.irq(m1_pulse_handler)
# motor2_controller.irq(m2_pulse_handler)
# motor3_controller = rp2.StateMachine(2, run_motor3, freq=2000, set_base=Pin(20))      # GPIO18 => pulse, GPIO21 => direction
# motor4_controller = rp2.StateMachine(3, run_motor4, freq=2000, set_base=Pin(26))      # GPIO18 => pulse, GPIO27 => direction
#========== sub functions ==========
def on_motor(motor_number):
    if motor_number == 1:
        motor1_controller.active(1)
        motor2_controller.active(0)
        motor3_controller.active(0)
        motor4_controller.active(0)
    elif motor_number == 2:
        motor1_controller.active(0)
        motor2_controller.active(1)
        motor3_controller.active(0)
        motor4_controller.active(0)
    elif motor_number == 3:
        motor1_controller.active(0)
        motor2_controller.active(0)
        motor3_controller.active(1)
        motor4_controller.active(0)
    elif motor_number == 4:
        motor1_controller.active(0)
        motor2_controller.active(0)
        motor3_controller.active(0)
        motor4_controller.active(1)
    elif motor_number == 0:
        pass
    
def set_dir(motor_number,direction):
    if motor_number == 1:
        motor1_dir_pin.value(direction)
    elif motor_number == 2:
        motor2_dir_pin.value(direction)
    elif motor_number == 3:
        motor3_dir_pin.value(direction)
    elif motor_number == 4:
        motor4_dir_pin.value(direction)
    elif motor_number == 0:
        pass

def off_motor():
    motor1_controller.active(0)
    motor2_controller.active(0)
    # motor3_controller.active(0)
    # motor4_controller.active(0)

def initial_io():
    motor1_dir_pin.value(0)
    motor2_dir_pin.value(0)
    # motor3_dir_pin.value(0)
    # motor4_dir_pin.value(0)

def resp_485(message):
    resp_message = device_id + message + "\n"
    device_link.write(bytes( ord(ch) for ch in resp_message))

def set_roller_motor_forward():     # tight paper
    motor1_dir_pin.value(0)

def set_roller_motor_backward():     # release paper
    motor1_dir_pin.value(1)

def set_slap_motor_up():
    motor2_dir_pin.value(1)

def set_slap_motor_down():
    motor2_dir_pin.value(0)


off_motor()
initial_io()

while True:
    # =========== command from master ============
    if(device_link.any()):
        char_cmd = device_link.read(1)
        char_cmd = char_cmd.decode()
        if char_cmd == '\n':
            execute_flag = True
        else:
            master_command = master_command + char_cmd

    if execute_flag==True:
        # check command
        if len(master_command) > 0:
            if master_command[0] == device_id:
                if master_command[1] == 'r':
                    message = "node" + device_id + " reset"
                    resp_485(message=message)
                    if debugging_flag:
                        db_message = device_id + "node is in reset state"
                        print(db_message)
                    time.sleep(0.1)
                    reset()

                elif master_command[1] == 's':
                    if len(master_command)>=3:
                        if master_command[2] == '1':
                            run_printer_flag = True
                            printer_state = 0
                        elif master_command[2] == '0':
                            origin_flag = True
                            origin_state = 0
                        message = "OK"
                        resp_485(message=message)

                elif master_command[1] == 'c':
                    message = "Complete"
                    resp_485(message=message)
                    if debugging_flag:
                        db_message = device_id + "dummy state"
                        print(db_message)

                elif master_command[1] == 't':         # turnoff all motors
                    off_motor()
                    run_motor_flag = False
                    current_silo = 0
                    message = "OK"
                    resp_485(message=message)
                    if debugging_flag:
                        db_message = device_id + "turn off all motors"
                        print(db_message)
                elif master_command[1] == 'd':          # turn on debug
                    if len(master_command)>= 3:
                        debugging_flag = True
                        message = "Debug"
                        resp_485(message=message)
                        if debugging_flag:
                            db_message = device_id + "turn on debugging"
                            print(db_message)

                        # ==== debug_command ======
                        if master_command[2] == '1':
                            debug_roller_motor_forward = True
                        elif master_command[2] == '2':
                            debug_roller_motor_backward = True
                        elif master_command[2] == '3':
                            debug_slap_motor_forward = True
                        elif master_command[2] == '4':
                            debug_slap_motor_backward = True
                elif master_command[1] == 'u':          # turn off debug
                    debugging_flag = False
                    message = "Undebug"
                    resp_485(message=message)
                    if debugging_flag:
                        db_message = device_id + "turn off debugging"
                        print(db_message)

            execute_flag = False
            master_command = ""
    
    # ============ run printer state machine ========
    if printer_state == 0:
        if run_printer_flag == True:
            motor1_controller.active(0)
            motor2_controller.active(0)
            printer_state = 1
            printer_state_timer = time.ticks_ms()
            set_slap_motor_up()
            set_roller_motor_forward()
            run_printer_flag = False
    elif printer_state == 1:
        if (time.ticks_ms() - printer_state_timer) >= 100:
            printer_state = 2
            printer_state_timer = time.ticks_ms()
            motor2_controller.active(1)
    elif printer_state == 2:
        if time.ticks_ms()-printer_state_timer>= 150:
            printer_state = 3
            printer_state_timer = time.ticks_ms()
            motor1_controller.active(0)
            motor2_controller.active(0)
    elif printer_state == 3:
        if (time.ticks_ms() - printer_state_timer) >= 2000:
            printer_state = 4
            motor1_controller.active(1)
            printer_state_timer = time.ticks_ms()
    elif printer_state == 4:
        if time.ticks_ms() - printer_state_timer >= 5000:
            printer_state = 100
        else:
            if duo_switch.value() == 1:
                printer_state = 5
                printer_state_timer = time.ticks_ms()
                motor1_controller.active(0)
                motor2_controller.active(0)
                set_slap_motor_down()
    elif printer_state == 5:
        if time.ticks_ms() - printer_state_timer >= 100:
            printer_state = 6
            motor1_controller.active(0)
            motor2_controller.active(1)
            printer_state_timer = time.ticks_ms()
    elif printer_state == 6:
        if time.ticks_ms()-printer_state_timer>=100:
            printer_state = 7
            motor1_controller.active(0)
            motor2_controller.active(0)
    elif printer_state == 7:
        # motor1_controller.active(0)
        # motor2_controller.active(0)
        pass
    elif printer_state == 100:
        # motor1_controller.active(0)
        # motor2_controller.active(0)
        pass
    elif printer_state == 101:
        # motor1_controller.active(0)
        # motor2_controller.active(0)
        pass

    if debug_roller_motor_forward:
        set_roller_motor_forward()
        motor1_controller.active(1)
        time.sleep(1)
        motor1_controller.active(0)
        debug_roller_motor_forward = False
    
    if debug_roller_motor_backward:
        set_roller_motor_backward()
        motor1_controller.active(1)
        time.sleep(1)
        motor1_controller.active(0)
        debug_roller_motor_backward = False
    
    if debug_slap_motor_forward:
        set_slap_motor_up()
        motor2_controller.active(1)
        time.sleep(1)
        motor2_controller.active(0)
        debug_slap_motor_forward = False
    
    if debug_slap_motor_backward:
        set_slap_motor_down()
        motor2_controller.active(1)
        time.sleep(1)
        motor2_controller.active(0)
        debug_slap_motor_backward = False


    if origin_state == 0:
        if origin_flag == True:
            motor1_controller.active(0)
            motor2_controller.active(0)
            set_roller_motor_backward()
            set_slap_motor_down()
            origin_state_timer = time.ticks_ms()
            origin_state = False
            origin_state = 1
    elif origin_state == 1:
        if time.ticks_ms() - origin_state_timer >= 10:
            motor1_controller.active(1)
            motor2_controller.active(1)
            origin_state = 2
    elif origin_state == 2:
        if slap_switch.value() == 0:
            origin_state = 3
            motor2_controller.active(0)
            origin_state_timer = time.ticks_ms()
    elif origin_state == 3:
        if time.ticks_ms() - origin_state_timer >= 500:
            motor1_controller.active(0)
            origin_state = 4
    elif origin_state == 4:
        pass




