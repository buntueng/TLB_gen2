from machine import Pin, UART, I2C, reset
import time
import bme280
import dht
import rp2

device_id = '1'
pc_command = ""
resp_message = ""
execute_flag = False
resp_flag = False
wait_device_resp = False
wait_slave2pc = False
running_state = 0

present_silo = '0'
run_main_state = False
main_state = 0

rolling_motor_dir_pin = Pin(17,Pin.OUT)
sliding_motor_dir_pin = Pin(19,Pin.OUT)
prox1_pin = Pin(10,Pin.IN)
prox2_pin = Pin(11,Pin.IN)
prox3_pin = Pin(12,Pin.IN)
prox4_pin = Pin(13,Pin.IN)

front_limit_pin = Pin(14,Pin.IN)
back_limit_pin = Pin(15,Pin.IN)
printer_limit_pin = Pin(22,Pin.IN)

tube_drop_pin = Pin(6,Pin.IN)
sticker_detect_pin = Pin(7,Pin.IN)

lock_solenoid_pin = Pin(26,Pin.OUT)
drop_solenoid_pin = Pin(27,Pin.OUT)
rolling_solenoid_pin = Pin(28,Pin.OUT)


dht_sensor = dht.DHT11(Pin(6)) 
bmp_link=I2C(1,sda=Pin(2), scl=Pin(3), freq=400000)    #initializing the I2C to bmp
pc_link = UART(0, baudrate=115200, bits=8, parity=None, stop=1,tx=Pin(0), rx=Pin(1),timeout=1000)
device_link = UART(1, baudrate=115200, bits=8, parity=None, stop=1,tx=Pin(4), rx=Pin(5),timeout=1000)
bmp280_sensor= bme280.BME280(i2c=bmp_link)

pc_link.read()              # clear data in serial port buffer
device_link.read()

#========== sub functions ==========
def save_params():
    pass

def initial_io():
    rolling_motor_dir_pin.value(0)
    sliding_motor_dir_pin.value(0)
    # turn off all solenoid
    lock_solenoid_pin.value(0)
    drop_solenoid_pin.value(0)
    rolling_solenoid_pin.value(0)

def pc_response(resp_message):
    pc_link.write( bytes( ord(ch) for ch in resp_message) )

def check_running_state():
    message = ""
    if running_state == 0:
        message = "idle"
    elif running_state > 0 and running_state < 20:
        message = "running"
    elif running_state == 20:
        message = "complete"
    elif running_state == 21:
        message = "jam"
    return message + "\n"

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def run_roller_motor():
    wrap_target()
    set(pins, 1)   [31]
    nop()
    set(pins, 1)   [31]
    nop()
    wrap()

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def run_sliding_motor():
    wrap_target()
    set(pins, 1)   [31]
    nop()
    set(pins, 1)   [31]
    nop()
    wrap()

rolling_motor = rp2.StateMachine(0, run_roller_motor, freq=2000, set_base=Pin(16))      # GPIO16 => pulse, GPIO17 => direction
sliding_motor = rp2.StateMachine(1, run_sliding_motor, freq=2000, set_base=Pin(18))      # GPIO18 => pulse, GPIO19 => direction
rolling_motor.active(0)
sliding_motor.active(0)
initial_io()


while True:
    # get proximeter sensors

    # =========== command from pc ============
    if(pc_link.any()):
        char_cmd = pc_link.read(1)
        char_cmd = char_cmd.decode()
        if char_cmd == '\n':
            execute_flag = True
        else:
            pc_command = pc_command + char_cmd
    # =========== response from slaves ============
    if(device_link.any()):
        device_resp = device_link.read(1)
        device_resp = device_resp.decode()
        if device_resp == '\n':
            resp_flag = True
        else:
            resp_message = resp_message + device_resp


    if execute_flag==True:
        # check command
        if len(pc_command) > 0:
            if pc_command[0] == device_id:              # command to master
                if pc_command[1] == 'e':                # return [temperature,humidity,pressure]
                    message = ""
                    try:
                        dht_sensor.measure()
                        message = str(dht_sensor.temperature()) + "," + str(dht_sensor.humidity()) + "," + str(bmp280_sensor.values[1])+"\n"
                    except:
                        message = "0,0,0\n"
                    pc_response(resp_message=message)
                elif pc_command[1] == 'r':
                    message = "reset\n"
                    pc_response(resp_message=message)
                    time.sleep(0.1)
                    reset()
                elif pc_command[1] == 'g':
                    present_silo = pc_command[2]
                    run_main_state = True
                    main_state = 0
                    message = "run silo motor\n"
                    pc_response(resp_message=message)
                
                elif pc_command[1] == 'c':
                    message = check_running_state()
                    pc_response(resp_message=message)
            else:
                # other send commad to slaves
                device_message = pc_command.encode()
                device_link.write(bytes( ord(ch) for ch in device_message))
                wait_slave2pc = True                                         # wait slaves response to pc
            execute_flag = False
            pc_command = ""

    if wait_slave2pc:
        pc_resp_message = resp_message.encode()
        resp_message = ""
        wait_slave2pc = False
        pc_response(pc_resp_message)
    
    if run_main_state:
        if main_state == 0:
            main_state = 1
            
        elif main_state == 1:
            pass
        elif main_state == 2:
            pass
        elif main_state == 3:
            pass
        elif main_state == 4:
            pass
        elif main_state == 5:
            pass
        elif main_state == 6:
            pass
        elif main_state == 7:
            pass
        elif main_state == 8:
            pass
        elif main_state == 9:
            pass
        elif main_state == 10:
            pass
        elif main_state == 11:
            pass
        elif main_state == 12:
            pass



