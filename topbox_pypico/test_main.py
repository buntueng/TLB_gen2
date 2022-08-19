from machine import Pin, UART, reset
import time
import rp2

device_id = '2'
master_command = ""
execute_flag = False
running_state = 0

# ========= assigned direction pin ===========
silo1_dir_pin = Pin(16,Pin.OUTPUT)
silo2_dir_pin = Pin(18,Pin.OUTPUT)
silo3_dir_pin = Pin(20,Pin.OUTPUT)
silo4_dir_pin = Pin(26,Pin.OUTPUT)


device_link = UART(0, baudrate=115200, bits=8, parity=None, stop=1,tx=Pin(0), rx=Pin(1),timeout=1000)
device_link.read()              # clear data in serial port buffer

#========== sub functions ==========
def main_state():
    pass

def initial_io():
    silo1_dir_pin.value(0)
    silo2_dir_pin.value(0)
    silo3_dir_pin.value(0)
    silo4_dir_pin.value(0)

def resp_485(message):
    resp_message = device_id + message
    device_link.write(bytes( ord(ch) for ch in resp_message))

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def run_silo1_motor():
    wrap_target()
    set(pins, 1)   [31]
    nop()
    set(pins, 1)   [31]
    nop()
    wrap()

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def run_silo2_motor():
    wrap_target()
    set(pins, 1)   [31]
    nop()
    set(pins, 1)   [31]
    nop()
    wrap()

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def run_silo3_motor():
    wrap_target()
    set(pins, 1)   [31]
    nop()
    set(pins, 1)   [31]
    nop()
    wrap()

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def run_silo4_motor():
    wrap_target()
    set(pins, 1)   [31]
    nop()
    set(pins, 1)   [31]
    nop()
    wrap()

silo1_motor = rp2.StateMachine(0, run_silo1_motor, freq=2000, set_base=Pin(17))      # GPIO16 => pulse, GPIO17 => direction
silo2_motor = rp2.StateMachine(1, run_silo2_motor, freq=2000, set_base=Pin(19))      # GPIO18 => pulse, GPIO19 => direction
silo3_motor = rp2.StateMachine(2, run_silo3_motor, freq=2000, set_base=Pin(21))      # GPIO18 => pulse, GPIO21 => direction
silo4_motor = rp2.StateMachine(3, run_silo4_motor, freq=2000, set_base=Pin(27))      # GPIO18 => pulse, GPIO27 => direction
silo1_motor.active(0)
silo2_motor.active(0)
silo3_motor.active(0)
silo4_motor.active(0)
initial_io()

while True:
    # get proximeter sensors

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
        if len(pc_command) > 0:
            if pc_command[0] == device_id:
                if pc_command[1] == 'r':
                    message = "reset\n"
                    resp_485(message=message)
                    time.sleep(0.1)
                    reset()

                elif pc_command[1] == '1':
                    silo1_motor.active(1)
                    message = "OK\n"
                    resp_485(message=message)   

                elif pc_command[1] == '2':
                    silo2_motor.active(1)
                    message = "OK\n"
                    resp_485(message=message)
                
                elif pc_command[1] == '3':
                    silo3_motor.active(1)
                    message = "OK\n"
                    resp_485(message=message)

                elif pc_command[1] == '4':
                    silo4_motor.active(1)
                    message = "OK\n"
                    resp_485(message=message)

                elif pc_command[1] == '0':         # turnoff all motors
                    silo1_motor.active(0)
                    silo2_motor.active(0)
                    silo3_motor.active(0)
                    silo4_motor.active(0)
                    message = "OK\n"
                    resp_485(message=message)
            execute_flag = False
            pc_command = ""





