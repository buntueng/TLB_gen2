from machine import Pin, UART, reset
import time
import rp2

device_id = '2'
master_command = ""
execute_flag = False
running_state = 0

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

current_silo = 0
run_motor_flag = False
motor_state = 0
motor_timer = 0
# ========= assigned direction pin ===========
silo1_dir_pin = Pin(5,Pin.OUT)
silo2_dir_pin = Pin(11,Pin.OUT)
silo3_dir_pin = Pin(15,Pin.OUT)
silo4_dir_pin = Pin(17,Pin.OUT)
silo5_dir_pin = Pin(20,Pin.OUT)
silo6_dir_pin = Pin(26,Pin.OUT)
#========== Enable pin ======================
silo1_ENB_pin = Pin(7,Pin.OUT)
silo2_ENB_pin = Pin(13,Pin.OUT)
silo3_ENB_pin = Pin(16,Pin.OUT)
silo4_ENB_pin = Pin(19,Pin.OUT)
silo5_ENB_pin = Pin(22,Pin.OUT)
silo6_ENB_pin = Pin(28,Pin.OUT)
#=============== LIMIT TUBE PIN ================
box1_limit_select_tube_pin = Pin(3,Pin.IN,Pin.PULL_UP)
box1_limit_release_tube_pin = Pin(4,Pin.IN,Pin.PULL_UP)

#===============================================

device_link = UART(1, baudrate=9600, bits=8, parity=None, stop=1,tx=Pin(8), rx=Pin(9),timeout=1000)
device_link.read()              # clear data in serial port buffer

silo1_motor = rp2.StateMachine(0, run_silo1_motor, freq=23000, set_base=Pin(6))      # GPIO16 => pulse, GPIO17 => direction
silo2_motor = rp2.StateMachine(1, run_silo2_motor, freq=23000, set_base=Pin(12))      # GPIO18 => pulse, GPIO19 => direction
silo3_motor = rp2.StateMachine(2, run_silo3_motor, freq=23000, set_base=Pin(14))####      # GPIO18 => pulse, GPIO21 => direction
silo4_motor = rp2.StateMachine(3, run_silo4_motor, freq=23000, set_base=Pin(18))###      # GPIO18 => pulse, GPIO27 => direction
silo5_motor = rp2.StateMachine(4, run_silo5_motor, freq=23000, set_base=Pin(21))
silo6_motor = rp2.StateMachine(5, run_silo4_motor, freq=23000, set_base=Pin(27))
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
    
def set_dir(motor_number,direction):
    if motor_number == 1:
        silo1_dir_pin.value(direction)
    elif motor_number == 2:
        silo2_dir_pin.value(direction)
    elif motor_number == 3:
        silo3_dir_pin.value(direction)
    elif motor_number == 4:
        silo4_dir_pin.value(direction)
    elif motor_number == 5:
        silo5_dir_pin.value(direction)
    elif motor_number == 6:
        silo6_dir_pin.value(direction)
    elif motor_number == 0:
        pass

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
    # get proximeter sensors
    # print(box1_limit_select_tube_pin.value(),box1_limit_release_tube_pin.value())
    # time.sleep(0.2)
    # =========== command from pc ============
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
                    message = "node " + device_id + " reset\n"
                    resp_485(message=message)
                    time.sleep(0.1)
                    reset()

                elif master_command[1] == '1':
                    current_silo = 1
                    set_dir(current_silo,0)
                    run_motor_flag = True
                    message = "Box1\n"
                    print("BoX1")
                    resp_485(message=message)   

                elif master_command[1] == '2':
                    current_silo = 2
                    set_dir(current_silo,0)
                    run_motor_flag = True
                    message = "Box2\n"
                    print("BoX2")
                    resp_485(message=message)
                
                elif master_command[1] == '3':
                    current_silo = 3
                    set_dir(current_silo,0)
                    run_motor_flag = True
                    message = "Box3\n"
                    print("BoX3")
                    resp_485(message=message)

                elif master_command[1] == '4':
                    current_silo = 4
                    set_dir(current_silo,0)
                    run_motor_flag = True
                    message = "Box4\n"
                    print("BoX4")
                    resp_485(message=message)

                elif master_command[1] == '5':
                    current_silo = 5
                    set_dir(current_silo,0)
                    run_motor_flag = True
                    message = "Box5\n"
                    print("BoX5")
                    resp_485(message=message)

                elif master_command[1] == '6':
                    current_silo = 6
                    set_dir(current_silo,0)
                    run_motor_flag = True
                    message = "Box6\n"
                    print("BoX6")
                    resp_485(message=message)

                elif master_command[1] == '0':         # turnoff all motors
                    off_motor()
                    off_enb()
                    run_motor_flag = False
                    current_silo = 0
                    set_dir(current_silo,0)
                    set_enb(current_silo,1)
                    message = "OK\n"
                    resp_485(message=message)
            execute_flag = False
            master_command = ""
    # =========== run motor ==============
    if run_motor_flag:
        if motor_state == 0:
            set_dir(current_silo,0)
            set_enb(current_silo,0)
            motor_state =1
            motor_timer = time.ticks_ms()
        elif motor_state == 1:
            set_dir(current_silo,0)
            if time.ticks_ms()-motor_timer >= 50:
                motor_state = 2
                on_motor(current_silo)
                motor_timer = time.ticks_ms()
        elif motor_state == 2:
            if time.ticks_ms()-motor_timer >= 1000:
                off_motor()
                motor_state = 3
                motor_timer = time.ticks_ms()
        elif motor_state == 3:
            if time.ticks_ms()-motor_timer >= 50:
                set_dir(current_silo,1)
                motor_state = 4
                motor_timer = time.ticks_ms()
        elif motor_state == 4:
            if time.ticks_ms()-motor_timer >= 50:
                on_motor(current_silo)
                motor_state = 5
                motor_timer = time.ticks_ms()
        elif motor_state == 5:
            if time.ticks_ms()-motor_timer >= 100:
                off_motor()
                motor_state = 0
                set_dir(current_silo,0)
                motor_timer = time.ticks_ms()




