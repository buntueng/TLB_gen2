from machine import Pin, UART, I2C, reset
import time
import bme280
import rp2

device_id = '1'
pc_command = ""
resp_message = ""
execute_flag = False
resp_flag = False
wait_device_resp = False
wait_slave2pc = False
running_state = 0
tube_drop_status = False
sticker_detect_status = False

main_state_timer = 0
printer_retry = 0
silo_retry = 0
check_printer_state_counter = 0

present_silo = '0'
run_main_state = False
main_state = 0

rolling_motor_dir_pin = Pin(17,Pin.OUT)
sliding_motor_dir_pin = Pin(19,Pin.OUT)
prox1_pin = Pin(10,Pin.IN)
prox2_pin = Pin(11,Pin.IN)
prox3_pin = Pin(12,Pin.IN)
prox4_pin = Pin(13,Pin.IN)

roller_limit_pin = Pin(14,Pin.IN)
front_and_back_limit_pin = Pin(15,Pin.IN,Pin.PULL_UP)
printer_limit_pin = Pin(22,Pin.IN)

tube_drop_pin = Pin(6,Pin.IN)
sticker_detect_pin = Pin(7,Pin.IN)

lock_solenoid_pin = Pin(26,Pin.OUT)
drop_solenoid_pin = Pin(27,Pin.OUT)
rolling_solenoid_pin = Pin(28,Pin.OUT)


#dht_sensor = dht.DHT11(Pin(6)) 
bmp_link=I2C(1,sda=Pin(2), scl=Pin(3), freq=400000)    #initializing the I2C to bmp
pc_link = UART(0, baudrate=115200, bits=8, parity=None, stop=1,tx=Pin(0), rx=Pin(1),timeout=1000)
device_link = UART(1, baudrate=115200, bits=8, parity=None, stop=1,tx=Pin(4), rx=Pin(5),timeout=1000)
bmp280_sensor= bme280.BME280(i2c=bmp_link)

pc_link.read()              # clear data in serial port buffer
device_link.read()

#========== sub functions ==========
def read_prox():
    sw_status = (prox4_pin.value() << 3) + (prox3_pin.value()<<2) + (prox2_pin.value()<<1) + prox1_pin.value()
    return_sw_status = 0
    if sw_status == 15:
        return_sw_status = 5
    elif sw_status == 14:
        return_sw_status = 4
    elif sw_status == 13:
        return_sw_status = 3
    elif sw_status == 11:
        return_sw_status = 2
    elif sw_status == 7:
        return_sw_status = 1
    else:
        return_sw_status = 0
    return return_sw_status

def set_sliding_forward():
    sliding_motor_dir_pin.value(1)

def set_sliding_backward():
    sliding_motor_dir_pin.value(0)

def save_params():
    pass

def run_printer_controller():
    message = '3s\n'
    device_link.write( bytes( ord(ch) for ch in message))

def initial_io():
    rolling_motor_dir_pin.value(0)
    sliding_motor_dir_pin.value(0)
    # turn off all solenoid
    lock_solenoid_pin.value(0)
    drop_solenoid_pin.value(0)
    rolling_solenoid_pin.value(0)

def run_silo(silo_number):
    message = '2s'+str(silo_number)+'\n'
    device_link.write( bytes( ord(ch) for ch in message))

def stop_silo():
    message = '2s0\n'
    device_link.write( bytes( ord(ch) for ch in message))

def check_printer_state():
    message = '3c\n'
    device_link.write( bytes( ord(ch) for ch in message))

def on_solenoid1():
    lock_solenoid_pin.value(1)

def off_solenoid1():
    lock_solenoid_pin.value(0)

def on_solenoid2():
    rolling_solenoid_pin.value(1)

def off_solenoid2():
    rolling_solenoid_pin.value(0)

def on_solenoid3():
    drop_solenoid_pin.value(1)

def off_solenoid3():
    drop_solenoid_pin.value(0)


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
    set(pins, 0)   [31]
    nop()
    wrap()

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def run_sliding_motor():
    wrap_target()
    set(pins, 1)   [31]
    nop()
    set(pins, 0)   [31]
    nop()
    wrap()

rolling_motor = rp2.StateMachine(0, run_roller_motor, freq=200000, set_base=Pin(16))      # GPIO16 => pulse, GPIO17 => direction
sliding_motor = rp2.StateMachine(1, run_sliding_motor, freq=200000, set_base=Pin(18))      # GPIO18 => pulse, GPIO19 => direction
rolling_motor.active(0)
sliding_motor.active(0)
initial_io()

while True:
    # get proximeter sensors
    box_location = read_prox()
    # check tube drop status
    if tube_drop_pin.value() == 0:
        tube_drop_status = True
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
        # device_resp = device_resp.decode()
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
                    present_silo = int(pc_command[2])
                    if present_silo >0 and present_silo <=4:
                        run_main_state = True
                        main_state = 0
                        message = "run machine\n"
                    else:
                        run_main_state = False
                        sliding_motor.active(0)
                        main_state = 0
                        message = "stop machine\n"
                    pc_response(resp_message=message)
                
                elif pc_command[1] == 'c':
                    message = check_running_state()
                    message = str(main_state)
                    pc_response(resp_message=message)
            else:
                # other send commad to slaves
                device_message = pc_command + "\n"
                device_link.write(bytes( ord(ch) for ch in device_message))
                wait_slave2pc = True                                         # wait slaves response to pc
            execute_flag = False
            pc_command = ""

    if wait_slave2pc:
        if resp_flag:
            resp_flag = False
            pc_resp_message = resp_message + "\n"
            resp_message = ""
            wait_slave2pc = False
            pc_response(pc_resp_message)
    
    if run_main_state:
        #======== check prox sensor ======
        if box_location == 0:
            main_state = 202
            sliding_motor.active(0)         # stop sliding motor
            off_solenoid1()
            off_solenoid2()
            off_solenoid3()
        #======== check limit_switch=======
        if front_and_back_limit_pin.value() == 0:
            main_state = 203
            sliding_motor.active(0)         # stop sliding motor
            off_solenoid1()
            off_solenoid2()
            off_solenoid3()
        # ======= check sticker detect =====
        if sticker_detect_pin.value() == 0:
            sticker_detect_status = True
        try:
            if main_state == 0:
                set_sliding_forward()
                main_state_timer = time.ticks_ms()
                printer_retry = 0
                run_printer_controller()
                main_state = 1
            elif main_state == 1:
                if time.ticks_ms() - main_state_timer >= 20:                # wait 20 ms
                    main_state = 2
                if printer_retry >= 5:
                    main_state = 200
            elif main_state == 2:
                if resp_flag:
                    print(resp_message)
                    if resp_message[0:2] == '3OK':
                        main_state =3
                    resp_flag = False
                    resp_message = ""
                else:
                    main_state = 1
                    main_state_timer = time.ticks_ms()
                    printer_retry = printer_retry + 1
            elif main_state == 3:
                if box_location == 1:
                    main_state = 4
                    sliding_motor.active(1)
                else:
                    main_state = 201                
            elif main_state == 4:
                if present_silo == 1:
                    main_state = 11
                    sliding_motor.active(0)
                else:
                    if box_location == 5:
                        main_state = 5
            elif main_state == 5:
                if box_location == 2:
                    main_state = 6
            elif main_state == 6:
                if present_silo == 2:
                    main_state = 11
                    sliding_motor.active(0)
                else:
                    if box_location == 5:
                        main_state = 7
            elif main_state == 7:
                if box_location == 3:
                    main_state = 8
            elif main_state == 8:
                if present_silo == 3:
                    main_state =11
                    sliding_motor.active(0)
                else:
                    if box_location == 5:
                        main_state = 9
            elif main_state == 9:
                if box_location == 4:
                    main_state = 10
            elif main_state == 10:
                if present_silo == 4:
                    main_state = 11
                    sliding_motor.active(0)
            elif main_state == 11:
                main_state_timer = time.ticks_ms()
                silo_retry = 0
                run_silo(present_silo)
                main_state = 12
                sliding_motor.active(0)
                tube_drop_status = False
            elif main_state == 12:
                if time.ticks_ms()-main_state_timer>= 20:
                    main_state = 13
            elif main_state == 13:
                if resp_flag:
                    if resp_message[0:2] == '3OK':
                        main_state = 14
                        main_state_timer = time.ticks_ms()
                    resp_flag = False
                    resp_message = ""
                else:
                    if silo_retry >= 5:
                        main_state = 204
                    else:
                        silo_retry = silo_retry + 1
                        main_state = 12
                        main_state_timer = time.ticks_ms()
            elif main_state == 14:
                if time.ticks_ms() - main_state_timer >= 5000:
                    stop_silo()
                    main_state = 205
                else:
                    if tube_drop_status:
                        main_state_timer = time.ticks_ms()
                        main_state = 15
                        tube_drop_status = False
            elif main_state == 15:
                if time.ticks_ms() - main_state_timer >= 200:
                    on_solenoid1()
                    main_state_timer = time.ticks_ms()
                    sticker_detect_status = False
                    main_state = 16
            elif main_state == 16:
                if time.ticks_ms() - main_state_timer >= 200:
                    off_solenoid1()
                    main_state = 17
            elif main_state == 17:
                if sticker_detect_status:
                    on_solenoid2()
                    main_state_timer = time.ticks_ms()
                    main_state = 18
                else:
                    main_state = 19
            elif main_state == 18:
                if time.ticks_ms()-main_state_timer >=500:
                    off_solenoid2()
                    main_state = 19
            elif main_state == 19:
                sliding_motor.active(1)
                if present_silo == 1:
                    main_state = 20
                elif present_silo == 2:
                    main_state = 21
                elif present_silo == 3:
                    main_state = 23
                elif present_silo == 4:
                    main_state = 25
            elif main_state == 20:
                if box_location == 5:
                    main_state = 21
            elif main_state == 21:
                if box_location == 2:
                    main_state = 22
            elif main_state == 22:
                if box_location == 5:
                    main_state = 23
            elif main_state == 23:
                if box_location == 3:
                    main_state = 24
            elif main_state == 24:
                if box_location == 5:
                    main_state = 25
            elif main_state == 25:
                if box_location == 4:
                    main_state = 26
            elif main_state == 26:
                sliding_motor.active(0)
                rolling_motor.active(1)
                check_printer_state()
                check_printer_state_counter = 0
                main_state_timer = time.ticks_ms()
                main_state = 27
            elif main_state == 27:
                if time.ticks_ms() - main_state_timer >= 20:
                    main_state = 28
            elif main_state == 28:
                if resp_flag:
                    if resp_message[0:1] == '3C':
                        main_state = 29
                    resp_message = ""
                    resp_flag = False
                else:
                    if check_printer_state_counter >= 5:
                        main_state = 206
                    else:
                        check_printer_state_counter = check_printer_state_counter + 1
                        main_state_timer = time.ticks_ms()
                        main_state = 27
            elif main_state == 29:
                # run sliding motor in second speed
                sliding_motor.active(1)
                main_state = 30
            elif main_state == 30:
                if roller_limit_pin.value() == 0:
                    sliding_motor.active(0)
                    set_sliding_backward()
                    main_state_timer = time.ticks_ms()
                    main_state = 31
            elif main_state == 31:
                if time.ticks_ms()-main_state_timer >= 800:
                    sliding_motor.active(1)
                    main_state_timer = time.ticks_ms()
                    main_state = 32
            elif main_state == 32:
                if time.ticks_ms() - main_state_timer >= 100:
                    on_solenoid1()
                    on_solenoid3()
                    main_state_timer = time.ticks_ms()
                    main_state = 33
            elif main_state == 33:
                if time.ticks_ms() - main_state_timer >= 100:
                    off_solenoid1()
                    off_solenoid3()
                    main_state = 34
            elif main_state == 34:
                if box_location == 4:
                    main_state = 35
            elif main_state == 35:
                if box_location == 5:
                    main_state = 36
            elif main_state == 36:
                if box_location == 3:
                    main_state = 37
            elif main_state == 37:
                if box_location == 5:
                    main_state = 38
            elif main_state == 38:
                if box_location == 2:
                    main_state = 39
            elif main_state == 39:
                if box_location == 5:
                    main_state = 40
            elif main_state == 40:
                if box_location == 1:
                    sliding_motor.active(0)
                    set_sliding_forward()
                    main_state = 41
            elif main_state == 41:
                pass
        except:
            main_state = 207
        # ============= error states =========
        #main_state == 200:             # printer module not response
        #main_state == 201:             # sliding box position is not origin
        #main_state == 202:             # prox sensor error
        #main_state == 203:             # sliding motor run to front limit switch
        #main_state == 204:             # silo module not response
        #main_state == 205:             # blood tube is jamming
        #main_state == 206:             # printer module not response
        #main_state == 207              # there is an error from try condition




