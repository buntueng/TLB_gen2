from machine import Pin, UART, reset
import time
import rp2

device_id = '3'
master_command = ""
execute_flag = False
running_state = 0

debugging = True

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
run_motor_flag = False
motor_state = 0
motor_timer = 0
# ========= assigned direction pin ===========
motor1_dir_pin = Pin(16,Pin.OUT)
motor2_dir_pin = Pin(19,Pin.OUT)
motor3_dir_pin = Pin(21,Pin.OUT)
motor4_dir_pin = Pin(27,Pin.OUT)

device_link = UART(0, baudrate=115200, bits=8, parity=None, stop=1,tx=Pin(0), rx=Pin(1),timeout=1000)
device_link.read()              # clear data in serial port buffer

motor1_controller = rp2.StateMachine(0, run_motor1, freq=2000, set_base=Pin(17))      # GPIO16 => pulse, GPIO17 => direction
motor2_controller = rp2.StateMachine(1, run_motor2, freq=2000, set_base=Pin(18))      # GPIO18 => pulse, GPIO19 => direction
motor3_controller = rp2.StateMachine(2, run_motor3, freq=2000, set_base=Pin(20))      # GPIO18 => pulse, GPIO21 => direction
motor4_controller = rp2.StateMachine(3, run_motor4, freq=2000, set_base=Pin(26))      # GPIO18 => pulse, GPIO27 => direction
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
    motor3_controller.active(0)
    motor4_controller.active(0)

def initial_io():
    motor1_dir_pin.value(0)
    motor2_dir_pin.value(0)
    motor3_dir_pin.value(0)
    motor4_dir_pin.value(0)

def resp_485(message):
    resp_message = device_id + message
    device_link.write(bytes( ord(ch) for ch in resp_message))


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
        if debugging:
            message = "receive CMD:" + master_command
            print(message)
        # check command
        if len(master_command) > 0:
            if master_command[0] == device_id:
                if master_command[1] == 'r':
                    message = "node" + device_id + " reset\n"
                    resp_485(message=message)
                    time.sleep(0.1)
                    reset()

                elif master_command[1] == 's':
                    run_motor_flag = True
                    message = "OK\n"
                    resp_485(message=message)   

                elif master_command[1] == 'c':
                    message = "Complete\n"
                    resp_485(message=message)

                elif master_command[1] == 't':         # turnoff all motors
                    off_motor()
                    run_motor_flag = False
                    current_silo = 0
                    message = "OK\n"
                    resp_485(message=message)

            execute_flag = False
            master_command = ""
    




