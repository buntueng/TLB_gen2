from machine import Pin, UART, reset
import time
import rp2

device_id = '2'
master_command = ""
execute_flag = False

#======================================================================================================
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def run_silo1_motor():
    wrap_target()
    set(pins, 1)   [31]
    nop()
    set(pins, 0)   [31]
    nop()
    wrap()

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def run_silo2_motor():
    wrap_target()
    set(pins, 1)   [31]
    nop()
    set(pins, 0)   [31]
    nop()
    wrap()

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def run_silo3_motor():
    wrap_target()
    set(pins, 1)   [31]
    nop()
    set(pins, 0)   [31]
    nop()
    wrap()

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def run_silo4_motor():
    wrap_target()
    set(pins, 1)   [31]
    nop()
    set(pins, 0)   [31]
    nop()
    wrap()

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def run_silo5_motor():
    wrap_target()
    set(pins, 1)   [31]
    nop()
    set(pins, 0)   [31]
    nop()
    wrap()

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def run_silo6_motor():
    wrap_target()
    set(pins, 1)   [31]
    nop()
    set(pins, 0)   [31]
    nop()
    wrap()
#======================================================================================================

run_motor_box1_flag = False
run_motor_box2_flag = False
run_motor_box3_flag = False
run_motor_box4_flag = False
run_motor_box5_flag = False
run_motor_box6_flag = False

motor_box1_state = 0
motor_box2_state = 0
motor_box3_state = 0
motor_box4_state = 0
motor_box5_state = 0
motor_box6_state = 0

motor_1_timer = 0
motor_2_timer = 0
motor_3_timer = 0
motor_4_timer = 0
motor_5_timer = 0
motor_6_timer = 0
# ========= assigned direction pin ===========
silo1_dir_pin = Pin(26,Pin.OUT) #5
silo2_dir_pin = Pin(20,Pin.OUT) #11
silo3_dir_pin = Pin(17,Pin.OUT) #15
silo4_dir_pin = Pin(15,Pin.OUT) #17
silo5_dir_pin = Pin(11,Pin.OUT) #20
silo6_dir_pin = Pin(5,Pin.OUT)  #26
#========== Enable pin ======================
silo1_ENB_pin = Pin(28,Pin.OUT) #7
silo2_ENB_pin = Pin(22,Pin.OUT) #13
silo3_ENB_pin = Pin(19,Pin.OUT) #16
silo4_ENB_pin = Pin(16,Pin.OUT) #19
silo5_ENB_pin = Pin(13,Pin.OUT) #22
silo6_ENB_pin = Pin(7,Pin.OUT)  #28
#=============== LIMIT TUBE PIN ================
box1_limit_select_tube_pin = Pin(3,Pin.IN,Pin.PULL_UP)
box1_limit_release_tube_pin = Pin(4,Pin.IN,Pin.PULL_UP)

#===============================================

device_link = UART(1, baudrate=9600, bits=8, parity=None, stop=1,tx=Pin(8), rx=Pin(9),timeout=1000)
device_link.read()              # clear data in serial port buffer

silo_freq = 80000

silo1_motor = rp2.StateMachine(0, run_silo1_motor, freq=silo_freq, set_base=Pin(27)) #6       # GPIO16 => pulse, GPIO17 => direction
silo2_motor = rp2.StateMachine(1, run_silo2_motor, freq=silo_freq, set_base=Pin(21)) #12      # GPIO18 => pulse, GPIO19 => direction
silo3_motor = rp2.StateMachine(2, run_silo3_motor, freq=silo_freq, set_base=Pin(18)) #14      # GPIO18 => pulse, GPIO21 => direction
silo4_motor = rp2.StateMachine(3, run_silo4_motor, freq=silo_freq, set_base=Pin(14)) #18      # GPIO18 => pulse, GPIO27 => direction
silo5_motor = rp2.StateMachine(4, run_silo5_motor, freq=silo_freq, set_base=Pin(12)) #21
silo6_motor = rp2.StateMachine(5, run_silo4_motor, freq=silo_freq, set_base=Pin(6))  #27
#========== sub functions ==========
def on_motor(motor_number):
    if motor_number == 1:
        silo1_motor.active(1)
        silo2_motor.active(0)
        silo3_motor.active(0)
        silo4_motor.active(0)
        silo5_motor.active(0)
        silo6_motor.active(0)
        silo1_ENB_pin.value(0)
        silo2_ENB_pin.value(1)
        silo3_ENB_pin.value(1)
        silo4_ENB_pin.value(1)
        silo5_ENB_pin.value(1)
        silo6_ENB_pin.value(1)
    elif motor_number == 2:
        silo1_motor.active(0)
        silo2_motor.active(1)
        silo3_motor.active(0)
        silo4_motor.active(0)
        silo5_motor.active(0)
        silo6_motor.active(0)
        silo1_ENB_pin.value(1)
        silo2_ENB_pin.value(0)
        silo3_ENB_pin.value(1)
        silo4_ENB_pin.value(1)
        silo5_ENB_pin.value(1)
        silo6_ENB_pin.value(1)
    elif motor_number == 3:
        silo1_motor.active(0)
        silo2_motor.active(0)
        silo3_motor.active(1)
        silo4_motor.active(0)
        silo5_motor.active(0)
        silo6_motor.active(0)
        silo1_ENB_pin.value(1)
        silo2_ENB_pin.value(1)
        silo3_ENB_pin.value(0)
        silo5_ENB_pin.value(1)
        silo6_ENB_pin.value(1) 
    elif motor_number == 4:
        silo1_motor.active(0)
        silo2_motor.active(0)
        silo3_motor.active(0)
        silo4_motor.active(1)
        silo5_motor.active(0)
        silo6_motor.active(0)
        silo1_ENB_pin.value(1)
        silo2_ENB_pin.value(1)
        silo3_ENB_pin.value(1)
        silo4_ENB_pin.value(0)
        silo5_ENB_pin.value(1)
        silo6_ENB_pin.value(1)
    elif motor_number == 5:
        silo1_motor.active(0)
        silo2_motor.active(0)
        silo3_motor.active(0)
        silo4_motor.active(0)
        silo5_motor.active(1)
        silo6_motor.active(0)
        silo1_ENB_pin.value(1)
        silo2_ENB_pin.value(1)
        silo3_ENB_pin.value(1)
        silo4_ENB_pin.value(1)
        silo5_ENB_pin.value(0)
        silo6_ENB_pin.value(1)
    elif motor_number == 6:
        silo1_motor.active(0)
        silo2_motor.active(0)
        silo3_motor.active(0)
        silo4_motor.active(0)
        silo5_motor.active(0)
        silo6_motor.active(1)
        silo1_ENB_pin.value(1)
        silo2_ENB_pin.value(1)
        silo3_ENB_pin.value(1)
        silo4_ENB_pin.value(1)
        silo5_ENB_pin.value(1)
        silo6_ENB_pin.value(0)
    elif motor_number == 0:
        pass
    
# def set_dir(motor_number,direction):
#     if motor_number == 1:
#         silo1_dir_pin.value(direction)
#     elif motor_number == 2:
#         silo2_dir_pin.value(direction)
#     elif motor_number == 3:
#         silo3_dir_pin.value(direction)
#     elif motor_number == 4:
#         silo4_dir_pin.value(direction)
#     elif motor_number == 5:
#         silo5_dir_pin.value(direction)
#     elif motor_number == 6:
#         silo6_dir_pin.value(direction)
#     elif motor_number == 0:
#         pass

def set_enb(motor_number,enb):
    if motor_number == 1:
        silo1_ENB_pin.value(enb)
    elif motor_number == 2:
        silo2_ENB_pin.value(enb)    
    elif motor_number == 2:
        silo3_ENB_pin.value(enb) 
    elif motor_number == 2:
        silo4_ENB_pin.value(enb)
    elif motor_number == 2:
        silo5_ENB_pin.value(enb)
    elif motor_number == 2:
        silo6_ENB_pin.value(enb)
    elif motor_number == 0:
        pass
def off_enb():
    silo1_ENB_pin.value(1)
    silo2_ENB_pin.value(1)
    silo3_ENB_pin.value(1)
    silo4_ENB_pin.value(1)
    silo5_ENB_pin.value(1)
    silo6_ENB_pin.value(1)

def off_motor():
    silo1_motor.active(0)
    silo2_motor.active(0)
    silo3_motor.active(0)
    silo4_motor.active(0)
    silo5_motor.active(0)
    silo6_motor.active(0)

def initial_io():
    silo1_dir_pin.value(0)
    silo2_dir_pin.value(0)
    silo3_dir_pin.value(0)
    silo4_dir_pin.value(0)
    silo5_dir_pin.value(0)
    silo6_dir_pin.value(0)
    #======= ENB =========
    silo1_ENB_pin.value(1)
    silo2_ENB_pin.value(1)
    silo3_ENB_pin.value(1)
    silo4_ENB_pin.value(1)
    silo5_ENB_pin.value(1)
    silo6_ENB_pin.value(1)

def resp_485(message):
    resp_message = device_id + message
    device_link.write(bytes( ord(ch) for ch in resp_message))

off_motor()
initial_io()

while True:
    # =========== command from pc ============
    if(device_link.any()):
        char_cmd = device_link.read(1)
        char_cmd = char_cmd.decode()
        if char_cmd == '\n':
            execute_flag = True
        else:
            master_command = master_command + char_cmd

    if execute_flag==True:
        if len(master_command) > 0:
            if master_command[0] == device_id:
                if master_command[1] == 'r':
                    message = "node " + device_id + " reset\n"
                    resp_485(message=message)
                    time.sleep(0.1)
                    reset()
                elif master_command[1] == '1':
                    run_motor_box1_flag = True
                    silo1_ENB_pin.value(0)
                    message = "Box1\n"
                    resp_485(message=message)   

                elif master_command[1] == '2':
                    run_motor_box2_flag = True
                    silo2_ENB_pin.value(0)
                    message = "Box2\n"
                    resp_485(message=message)

                elif master_command[1] == '3':
                    run_motor_box3_flag = True
                    silo3_ENB_pin.value(0)
                    message = "Box3\n"
                    resp_485(message=message)

                elif master_command[1] == '4':
                    run_motor_box4_flag = True
                    silo4_ENB_pin.value(0)
                    message = "Box4\n"
                    resp_485(message=message)

                elif master_command[1] == '5':
                    run_motor_box5_flag = True
                    silo5_ENB_pin.value(0)
                    message = "Box5\n"
                    resp_485(message=message)

                elif master_command[1] == '6':
                    run_motor_box6_flag = True
                    silo6_ENB_pin.value(0)
                    message = "Box6\n"
                    resp_485(message=message)

                elif master_command[1] == '0':         # turnoff all motors
                    off_motor()
                    off_enb()
                    run_motor_flag = False
                    message = "OK\n"
                    resp_485(message=message)
                    
                elif master_command[1] == 's':
                    if master_command[2] == '1':
                        run_motor_box1_flag = False
                        motor_box1_state = 0
                        silo1_dir_pin.value(0)
                        silo1_motor.active(0)
                        print("stop motor")

                    elif master_command[2] == '2':
                         run_motor_box2_flag = False
                         motor_box2_state = 0
                         silo2_dir_pin.value(0)
                         silo2_motor.active(0)
                         print("stop motor")

                    elif master_command[2] == '3':
                         run_motor_box3_flag = False
                         motor_box3_state = 0
                         silo3_dir_pin.value(0)
                         silo3_motor.active(0)
                         print("stop motor")

                    elif master_command[2] == '4':
                         run_motor_box4_flag = False
                         motor_box4_state = 0
                         silo4_dir_pin.value(0)
                         silo4_motor.active(0)
                         print("stop motor")

                    elif master_command[2] == '5':
                         run_motor_box5_flag = False
                         motor_box5_state = 0
                         silo5_dir_pin.value(0)
                         silo5_motor.active(0)
                         print("stop motor")

                    elif master_command[2] == '6':
                         run_motor_box6_flag = False
                         motor_box6_state = 0
                         silo6_dir_pin.value(0)
                         silo6_motor.active(0)
                         print("stop motor")
                    
            execute_flag = False
            master_command = ""

    # =========== run motor ==============

    if run_motor_box1_flag:    
        if motor_box1_state == 0:
            silo1_dir_pin.value(0)
            silo1_motor.active(1)

    if run_motor_box2_flag:
        if motor_box2_state == 0:
            silo2_dir_pin.value(0)
            silo2_motor.active(1)
    
    if run_motor_box3_flag:
        if motor_box3_state == 0:
            silo3_dir_pin.value(0)
            silo3_motor.active(1)

    if run_motor_box4_flag:
        if motor_box4_state == 0:
            silo4_dir_pin.value(0)
            silo4_motor.active(1)

    if run_motor_box5_flag:
        if motor_box5_state == 0:
            silo5_dir_pin.value(0)
            silo5_motor.active(1)

    if run_motor_box6_flag:
        if motor_box6_state == 0:
            silo6_dir_pin.value(0)
            silo6_motor.active(1)

