from machine import Pin, UART, reset ###po
import time
import rp2

device_id = '1'
pc_command = ""
resp_message = ""
execute_flag = False
resp_flag = False
start_flag = False
wait_device_resp = False
wait_slave2pc = False
running_state = 0
tube_drop_status = False
sticker_detect_status = False
device_resp_message = ""

main_state_timer = 0
printer_retry = 0
silo_retry = 0
check_printer_state_counter = 0

present_silo = '0'
run_main_state = False
main_state = 0

move_origin = True
move_origin_state = 0
move_origin_timer = 0

fast_sliding_motor = True

# time.sleep(10)
#======================================= config pin ====================================
relay_rolling_pin = Pin(21,Pin.OUT)
relay_sliding_pin = Pin(20,Pin.OUT)
rolling_motor_dir_pin = Pin(19,Pin.OUT)
sliding_motor_dir_pin = Pin(17,Pin.OUT)
prox1_pin = Pin(10,Pin.IN)
prox2_pin = Pin(11,Pin.IN)
prox3_pin = Pin(12,Pin.IN)
prox4_pin = Pin(13,Pin.IN)
prox5_pin = Pin(8,Pin.IN)##
prox6_pin = Pin(9,Pin.IN)##

roller_limit_pin = Pin(14,Pin.IN)
# front_and_back_limit_pin = True
printer_limit_pin = Pin(22,Pin.IN)

tube_drop_pin = Pin(6,Pin.IN)
sticker_detect_pin = Pin(7,Pin.IN)

lock1_solenoid_pin = Pin(27,Pin.OUT)
drop1_solenoid_pin = Pin(28,Pin.OUT)
select1_solenoid_pin = Pin(26,Pin.OUT)
# rolling_solenoid_pin = Pin(26,Pin.OUT)


pc_link = UART(0, baudrate=115200, bits=8, parity=None, stop=1,tx=Pin(0), rx=Pin(1),timeout=1000)
device_link = UART(1, baudrate=9600, bits=8, parity=None, stop=1,tx=Pin(4), rx=Pin(5),timeout=1000)

pc_link.read()              # clear data in serial port buffer
device_link.read()

#========== sub functions ==========
def read_prox():
    sw_status = (prox6_pin.value() << 5)+(prox5_pin.value() << 4)+(prox4_pin.value() << 3) + (prox3_pin.value()<<2) + (prox2_pin.value()<<1) + prox1_pin.value()
    return_sw_status = 0
    if sw_status == 63:
        return_sw_status = 7   #########################เริ่มแก้pox
    elif sw_status == 62:
        return_sw_status = 1
    elif sw_status == 61:
        return_sw_status = 2
    elif sw_status == 59:
        return_sw_status = 3
    elif sw_status == 55:
        return_sw_status = 4
    elif sw_status == 47:
        return_sw_status = 5
    elif sw_status == 31:
        return_sw_status = 6
    else:
        return_sw_status = 0
    return return_sw_status

def On_rolling():
    relay_rolling_pin.value(1)

def Off_rolling():
    relay_rolling_pin.value(0)

def On_sliding():
    relay_sliding_pin.value(1)

def Off_sliding():
    relay_sliding_pin.value(0)

def set_sliding_forward():
    sliding_motor_dir_pin.value(1)

def set_sliding_backward():
    sliding_motor_dir_pin.value(0)

def save_params():
    pass

def run_printer_controller():
    message = '3s1\n'
    device_link.write( bytes( ord(ch) for ch in message))

def clear_printer_controller():
    message = '3s0\n'
    device_link.write( bytes( ord(ch) for ch in message))
def come_back_origin():
    message = '1o\n'
    device_link.write( bytes( ord(ch) for ch in message))

def initial_io():
    rolling_motor_dir_pin.value(1)
    sliding_motor_dir_pin.value(1)
    # turn off all solenoid
    lock1_solenoid_pin.value(0)
    drop1_solenoid_pin.value(0)
    select1_solenoid_pin.value(0)
    sliding_motor_dir_pin.value(0)

def run_silo(silo_number):
    message = '2'+ str(silo_number)+'\n'
    device_link.write(bytes( ord(ch) for ch in message))

def stop_silo():
    message = '20\n'
    device_link.write( bytes( ord(ch) for ch in message))

def check_printer_state():
    message = '3c\n'
    device_link.write( bytes( ord(ch) for ch in message))

def on_solenoid1():
    lock1_solenoid_pin.value(1)

def off_solenoid1():
    lock1_solenoid_pin.value(0)

def on_solenoid2():
    select1_solenoid_pin.value(1)

def off_solenoid2():
    select1_solenoid_pin.value(0)

def on_solenoid3():
    drop1_solenoid_pin.value(1)

def off_solenoid3():
    drop1_solenoid_pin.value(0)
# ----------------------------------------------------------------





def pc_response(resp_message):
    resp_message = resp_message + "\n" ###resp=""+"n"
    pc_link.write( bytes( ord(ch) for ch in resp_message) )

def check_running_state():
    message = ""
    if main_state == 0:
        message = "idle"
    elif main_state > 0 and main_state < 33:
        message = "running"
    elif main_state >= 33 and main_state < 41:
        message = "back"
    elif main_state == 45:
        message = "complete"
    elif main_state == 21:
        message = "jam"
    elif main_state == 200:
        message = "printer module not response"
    elif main_state == 201:
        message = "sliding not origin"
    elif main_state == 202:
        message = "prox sensor error"
    elif main_state == 203:
        message = "limit switch"
    elif main_state == 204:
        message = "silo module not response"
    elif main_state == 205:
        message = "tube jam"
    elif main_state == 206:
        message = "printer module not response"
    elif main_state == 207:
        message = "try condition error"
    elif main_state == 208:
        message = "running_error"
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

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def run_sliding_motor_step2():
    wrap_target()
    set(pins, 1)   [31]
    nop()
    set(pins, 0)   [31]
    nop()
    wrap()

##เริ่ม
sliding_motor = rp2.StateMachine(0, run_sliding_motor, freq=2500000, set_base=Pin(16))      # GPIO16 => pulse, GPIO17 => direction //2600000
rolling_motor = rp2.StateMachine(1, run_roller_motor, freq=1200000, set_base=Pin(18))      # GPIO18 => pulse, GPIO19 => direction
rolling_motor.active(0)
sliding_motor.active(0)
rolling_motor_dir_pin.value(1) ##ประกาศตำแหน่งที่3
initial_io()
# move sliding motor to origin
set_sliding_backward()
clear_printer_controller()
time.sleep(0.2)
resp_flag = False
device_resp_message = ""
move_origin = True
move_origin_state = 0

# clear tube on initial
clear_tube_flag = False
clear_tube_timer = 0
clear_tube_state = 0

while True:
    # get proximeter sensors
    box_location = read_prox()
    limit_status = roller_limit_pin.value()
    # check tube drop status
    #print(tube_drop_pin.value(), +sticker_detect_pin.value())
    # print(main_state)
    # time.sleep(0.1)
    # time.sleep(0.2)
    if tube_drop_pin.value() == 0: ##หลอดตกขาที่ 6 มีค่าเป็น0
        tube_drop_status = True  ###กำหนดส่งflagว่าหลอดตก

    if sticker_detect_pin.value() == 1:
        sticker_detect_status = True
        
    if sticker_detect_pin.value() == 0:
        sticker_detect_status = False

    if wait_slave2pc and resp_flag: ###กำหนด wait และ resp เป็น false
        resp_flag = False
        wait_slave2pc = False
        pc_resp_message = device_resp_message + "\n" ##กำหนด pc-resp= ""+"n"
        pc_response(pc_resp_message) 
        device_resp_message = ""  

    # ===== move sliding motor to origin ========
    if move_origin:
        if move_origin_state == 0:
            if start_flag==True:
                move_origin_state = 100
                move_origin = False
                Off_sliding()
                sliding_motor.active(0)
            else:
                On_sliding()
                move_origin_state = 200
                set_sliding_backward()
                move_origin_timer = time.ticks_ms()

        elif move_origin_state == 1:
            if start_flag==True:
                move_origin_state = 100
                #move_origin = False
                Off_sliding()
                sliding_motor.active(0)
                clear_tube_flag = True
                clear_tube_state = 0
                move_origin_state = 3
            else:
                if time.ticks_ms() - move_origin_timer >= 3000:
                    move_origin_state = 102
                    move_origin = False
                    Off_sliding()
                    sliding_motor.active(0)
                else:
                    if box_location == 1:
                        move_origin_state = 2
                        #move_origin = False
                        # Off_sliding()
                        # sliding_motor.active(0)
                    elif box_location == 0:
                        move_origin_state = 101
                        move_origin = False
                        Off_sliding()
                        sliding_motor.active(0)
                    else:
                        pass
        elif move_origin_state == 2:                    # sliding motor is origin
            move_origin_timer = time.ticks_ms()
            set_sliding_backward()
            sliding_motor.active(1)
            On_sliding()
            move_origin_state = 222
            # Off_sliding()

            # ========= set clear tube state and flag
            # clear_tube_flag = True
            # clear_tube_state = 0
            # move_origin_state = 3
        elif move_origin_state == 222:
            if time.ticks_ms() - move_origin_timer >= 10:
                Off_sliding()
                sliding_motor.active(0)
                clear_tube_flag = True
                clear_tube_state = 0
                move_origin_state = 3
        elif move_origin_state == 3:
            move_origin = False
        elif move_origin_state == 100:                  # sliding motor hits limit switch
            Off_sliding()
            pass
        elif move_origin_state == 101:                  # prox sensor error
            Off_sliding()
            pass
        elif move_origin_state == 102:                  # sliding motor can not run
            Off_sliding()
            pass
        elif move_origin_state == 200:
            if time.ticks_ms()- move_origin_timer >= 50:
                sliding_motor.active(1)
                move_origin_state = 1
                move_origin_timer = time.ticks_ms()
    #========================================= clear tube
    if clear_tube_flag:
        if clear_tube_state == 0:
            clear_tube_timer = time.ticks_ms()
            clear_tube_state = 10
        elif clear_tube_state == 1:
            if time.ticks_ms() - clear_tube_timer >= 100:
                On_sliding()
                sliding_motor.active(1)
                clear_tube_state = 2
        elif clear_tube_state == 2:
            if roller_limit_pin.value() == 1:
                sliding_motor.active(0)
                clear_tube_timer = time.ticks_ms()
                clear_tube_state = 22
                set_sliding_backward()
        elif clear_tube_state == 22:
            if time.ticks_ms() - clear_tube_timer >= 10:   
                sliding_motor.active(1)  
                clear_tube_timer = time.ticks_ms() 
                clear_tube_state = 23   
        elif clear_tube_state == 23:
            if time.ticks_ms() - clear_tube_timer >= 120:
                on_solenoid3()
                sliding_motor.active(0)
                clear_tube_timer = time.ticks_ms()
                clear_tube_state = 3
        elif clear_tube_state == 3:
            if time.ticks_ms() - clear_tube_timer >= 300:
                clear_tube_state = 4
                on_solenoid1()
                # off_solenoid3()
                clear_tube_timer = time.ticks_ms()
        elif clear_tube_state == 4:
            if time.ticks_ms() - clear_tube_timer >= 300:
                clear_tube_state = 5
                off_solenoid1()
                off_solenoid3()
                clear_tube_timer = time.ticks_ms()
        elif clear_tube_state == 5:
            if time.ticks_ms() - clear_tube_timer >= 500:
                clear_tube_state = 6
                off_solenoid1()
                off_solenoid3()
                clear_tube_timer = time.ticks_ms()
        elif clear_tube_state == 6:
            sliding_motor.active(1)
            clear_tube_state = 7
        elif clear_tube_state == 7:
            if box_location == 1:
                clear_tube_timer = time.ticks_ms()
                # sliding_motor.active(0)
                # Off_sliding()
                # set_sliding_backward()
                clear_tube_state = 777
                # clear_tube_flag = False
        elif clear_tube_state == 777:
            if time.ticks_ms() - clear_tube_timer >= 20:
                sliding_motor.active(0)
                Off_sliding()
                set_sliding_backward()
                clear_tube_state = 8
                clear_tube_flag = False

        elif clear_tube_state == 10:
            if time.ticks_ms() - clear_tube_timer >= 200:
                set_sliding_forward()
                clear_tube_state = 11
                clear_tube_timer = time.ticks_ms()
        elif clear_tube_state == 11:
            if time.ticks_ms() - clear_tube_timer >= 200:
                clear_tube_state = 1
                clear_tube_timer = time.ticks_ms()

    # =========== command from pc ============
    if(pc_link.any()):
        try:
            char_cmd = pc_link.read(1)
            char_cmd = char_cmd.decode()
            if char_cmd == '\n':
                execute_flag = True
            else:
                pc_command = pc_command + char_cmd
        except:
            execute_flag = False
            pc_command = ""
    # =========== response from slaves ============
    if(device_link.any()):
        try:
            device_resp = ""
            device_resp = device_link.read(1)
            device_resp = device_resp.decode()
            if device_resp == '\n':
                resp_flag = True
            else:
                device_resp_message = device_resp_message + device_resp
        except:
            device_resp_message = ""
            resp_flag = False
     ####################################################### all order   
    if execute_flag==True:
        # check command
        if len(pc_command) > 0:
            if pc_command[0] == device_id:              # command to master
                if len(pc_command) == 2:                ##focus colum2
                    if pc_command[1] == 'e':                # return [temperature,humidity,pressure]
                        message = "0,0,0,"
                        pc_response(resp_message=message)
                    elif pc_command[1] == 'r':              #1r
                        message = "reset"
                        pc_response(resp_message=message)
                        time.sleep(0.1)
                        reset() 
                    elif pc_command[1] == 'c':               #1c
                        message = check_running_state()
                        #message = str(main_state)
                        pc_response(resp_message=message)
                    elif pc_command[1] == 'l':               #1l
                        message = str(box_location)
                        pc_response(resp_message=message)
                    elif pc_command[1] == 'p':               #1p
                        message = str(limit_status)
                        pc_response(resp_message=message)
                    elif pc_command[1] == 't':               #1t
                        message = str(tube_drop_status) + "\t" + str(sticker_detect_status)
                        pc_response(resp_message=message)
                        tube_drop_status = False
                        sticker_detect_status = False
                    elif pc_command[1] == 'o':               #1o                           # move sliding motor to origin
                        On_sliding()
                        move_origin = True
                        move_origin_state = 0
                        message = "Go origin"
                        pc_response(resp_message=message)
                    elif pc_command[1] == 'x':
                        message = "x command"                #1x
                        pc_response(message)           
                elif len(pc_command) == 3:                   #focus colum3
                    if pc_command[1] == 'd':
                        message = ""
                        if pc_command[2] == '1':             #1d1
                            set_sliding_forward()
                            On_sliding()
                            sliding_motor.active(1)
                            time.sleep(0.5)
                            sliding_motor.active(0)
                            time.sleep(0.5)
                            Off_sliding()
                            message = "move sliding forward"
                        elif pc_command[2] == '2':           #1d2
                            set_sliding_backward()
                            On_sliding()
                            sliding_motor.active(1)
                            time.sleep(0.5)
                            sliding_motor.active(0)
                            time.sleep(0.5)
                            Off_sliding()
                            message = "move sliding backward"
                        elif pc_command[2] == '3':           #1d3
                            On_sliding()
                            rolling_motor_dir_pin.value(0)
                            rolling_motor.active(1)
                            time.sleep_ms(100)
                            rolling_motor.active(0)
                            time.sleep_ms(10)
                            rolling_motor_dir_pin.value(1)
                            rolling_motor.active(1)
                            time.sleep(1)
                            rolling_motor.active(0)
                            Off_sliding()
                            message = "run rolling motor"
                        elif pc_command[2] == '4':           #1d4
                            on_solenoid1()
                            time.sleep(0.2)
                            off_solenoid1()
                            message = "on_solinoid_Locktube"    
                        elif pc_command[2] =='5':            #1d5
                            on_solenoid2()
                            time.sleep(0.2)
                            off_solenoid2()
                            message = "on_solinoid_select_tube"
                        elif pc_command[2] =='6':           #1d6
                            on_solenoid3()
                            time.sleep(0.2)
                            off_solenoid3()
                            message = "on_solinoid_drop_Tube"

                        elif pc_command[2]=='7':            #1d7
                            On_sliding()
                            On_rolling()
                            time.sleep(0.2)
                            message = "On sliding"
                        elif pc_command[2]=='8':             #1d8
                            Off_sliding()
                            Off_rolling()
                            time.sleep(0.2)
                            message ="Off sliding"
                        pc_response(resp_message=message)
                    elif pc_command[1] == 'g':
                        present_silo = int(pc_command[2])
                        if present_silo >0 and present_silo <=6:       ############################################ต้องมาแก้px ตรงนี้
                            run_main_state = True
                            main_state = 0
                            On_sliding()
                            message = "run machine"           #1g(1-6)
                        else:
                            run_main_state = False
                            sliding_motor.active(0)
                            main_state = 0
                            Off_sliding()
                            message = "stop machine"
                        pc_response(resp_message=message)
            else:
                if pc_command[0] <= '9':
                    # other send commad to slaves
                    device_message = pc_command + "\n"
                    device_link.write(bytes( ord(ch) for ch in device_message))
                    wait_slave2pc = True                                        # wait slaves response to pc
            execute_flag = False
            pc_command = ""

    
    ###------------------------------------------------------------run main -----------------------------------------------------------------------------
    if run_main_state:
        previous_state=main_state                         
        #======== check prox sensor ======
        if box_location == 0:
            main_state = 202
            Off_sliding()
            sliding_motor.active(0)         # stop sliding motor
            # sliding_motor.active(0)
            off_solenoid1()
            off_solenoid2()
            off_solenoid3()
        #======== check limit_switch=======
        if start_flag==True:
            main_state = 203
            Off_sliding()
            sliding_motor.active(0)         # stop sliding motor
            # sliding_motor1.active(0)
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
                if time.ticks_ms() - main_state_timer >= 100:                # wait 20 ms
                    main_state = 2
                if printer_retry >= 5:
                    main_state = 200
            elif main_state == 2:
                if resp_flag:
                    if len(device_resp_message) >= 2:
                        if device_resp_message[0:3] == '3OK':              ##///////////////////////////////////////
                            main_state =3
                    resp_flag = False
                    device_resp_message = ""
                else:
                    main_state = 1
                    main_state_timer = time.ticks_ms()
                    printer_retry = printer_retry + 1
            #-------------------------------------------------------------------------------------------------
            elif main_state == 3:
                if box_location == 1:    ####ถ้ากล่อง1
                    main_state = 4
                    sliding_motor.active(1)
                else:
                    main_state = 201                
            elif main_state == 4:
                if present_silo == 1:           
                    main_state = 11
                    sliding_motor.active(0)
                else:
                    if box_location == 7:
                        main_state = 5
            #--------------------------------------------------------------------------------------------------------
            elif main_state == 5:
                if box_location == 2:  ###กล่อง2
                    main_state = 6
            elif main_state == 6:
                if present_silo == 2:
                    main_state = 11
                    sliding_motor.active(0)
                else:
                    if box_location == 7:
                        main_state = 7
            #-----------------------------------------------------------------------------------------------------------
            elif main_state == 7:
                if box_location == 3:  ##box3
                    main_state = 8
            elif main_state == 8:
                if present_silo == 3:
                    main_state =11
                    sliding_motor.active(0)
                else:
                    if box_location == 7:
                        main_state = 711
            #--------------------------------------------------------------------------------------------------------------
            elif main_state == 711:
                if box_location == 4:  ##box4
                    main_state = 811
            elif main_state == 811:
                if present_silo == 4:
                    main_state =11
                    sliding_motor.active(0)
                else:
                    if box_location == 7:
                        main_state = 712
            #----------------------------------------------------------------------------------------------------------------
            elif main_state == 712:
                if box_location == 5:  ##box5
                    main_state = 812
            elif main_state == 812:
                if present_silo == 5:
                    main_state =11
                    sliding_motor.active(0)
                else:
                    if box_location == 7:
                        main_state = 9
            
            #-----------------------------------------------------------------------------------------------------------------
            elif main_state == 9:
                if box_location == 6: ##box6
                    main_state = 10
            elif main_state == 10:
                if present_silo == 6:
                    main_state = 11
                    sliding_motor.active(0)
            #-----------------------------------------------------------------------------------------------------------------
            elif main_state == 11:
                main_state_timer = time.ticks_ms()
                resp_flag = False
                device_resp_message = ""
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
                    if len(device_resp_message) >= 3:
                        if device_resp_message[0:3] == '2Bo':
                            main_state = 14
                            main_state_timer = time.ticks_ms()
                    tube_drop_status = False
                    resp_flag = False
                    device_resp_message = ""
                else:
                    if silo_retry >= 50:
                        main_state = 204
                    else:
                        silo_retry = silo_retry + 1
                        main_state = 12
                        main_state_timer = time.ticks_ms()
            elif main_state == 14:
                if time.ticks_ms() - main_state_timer >= 7000:
                    stop_silo()
                    main_state = 205
                else:
                    if tube_drop_status:
                        #stop_silo()
                        main_state_timer = time.ticks_ms()
                        main_state = 70
                        tube_drop_status = False            
            elif main_state == 15:
                if time.ticks_ms() - main_state_timer >= 300:
                    on_solenoid1()
                    main_state_timer = time.ticks_ms()
                    sticker_detect_status = False
                    main_state = 16
                else:
                    if resp_flag:
                        resp_flag = False
                        device_resp_message = ""
            elif main_state == 16:
                if time.ticks_ms() - main_state_timer >= 500:
                    off_solenoid1()
                    main_state_timer = time.ticks_ms()
                    main_state = 17

            elif main_state == 17:
                if time.ticks_ms() - main_state_timer >= 1000:    
                    if sticker_detect_status == True:
                        on_solenoid2()
                        main_state_timer = time.ticks_ms()
                        main_state = 18
                    else:
                        on_solenoid2()
                        main_state_timer = time.ticks_ms()
                        main_state = 181
            elif main_state == 18:
                if time.ticks_ms()-main_state_timer >=10000: #500
                    off_solenoid2()
                    off_solenoid1()
                    main_state = 19
                if time.ticks_ms()-main_state_timer >=2000: #500    
                    if sticker_detect_status == True:
                        off_solenoid2()
                        off_solenoid1()
                        main_state = 19

            elif main_state == 181:
                if time.ticks_ms() - main_state_timer >= 4000: #20
                    off_solenoid2()
                    off_solenoid1()
                    main_state = 19
                if time.ticks_ms()-main_state_timer >=2000: #500 
                    if sticker_detect_status == True:
                        off_solenoid2()
                        off_solenoid1()
                        main_state = 19
                # elif sticker_detect_status == True:
                #     off_solenoid2()
                #     off_solenoid1()
                #     main_state = 19
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
                elif present_silo ==5:
                    main_state = 27
                elif present_silo == 6:
                    main_state = 29
            elif main_state == 20:
                                                 
                if box_location == 7:
                    main_state = 21
            elif main_state == 21:
                if box_location == 2:
                    main_state = 22
            elif main_state == 22:
                if box_location == 7:
                    main_state = 23
            elif main_state == 23:
                if box_location == 3:
                    main_state = 24
            elif main_state == 24:
                if box_location == 7:
                    main_state = 25
            elif main_state == 25:                  # stop at box 4
                if box_location == 4:
                    main_state = 26
            elif main_state == 26:
                if box_location == 7:
                    main_state = 27
            elif main_state ==27:
                if box_location ==5:
                    main_state = 28
            elif main_state == 28:
                if box_location == 7:
                    main_state =29
            elif main_state == 29:
                if box_location == 6:
                    main_state = 30
            elif main_state == 30:
                # --------------roller up--------------------
                On_rolling()
                sliding_motor.active(0)
                rolling_motor.active(0)
                resp_flag = False
                device_resp_message = ""
                check_printer_state()
                check_printer_state_counter = 0
                main_state_timer = time.ticks_ms()
                main_state = 31
            elif main_state == 31:
                if time.ticks_ms() - main_state_timer >= 400:#200
                    main_state = 32
            elif main_state == 32:
                if resp_flag:
                    if len(device_resp_message) >= 2:
                        # if device_resp_message[0:2] == '3C':       # machine complete
                        #     main_state = 33
                        #     main_state_timer = time.ticks_ms()
                        #     set_sliding_forward()
                        # else:
                        #     main_state = 50
                        #     main_state_timer = time.ticks_ms()
                        # ----device_resp_message == '3C'
                        main_state = 33
                        main_state_timer = time.ticks_ms()
                    device_resp_message = ""
                    resp_flag = False
                else:
                    if check_printer_state_counter >= 60:
                        main_state = 206
                        Off_rolling()
                        rolling_motor.active(0)
                    else:
                        check_printer_state_counter = check_printer_state_counter + 1
                        main_state_timer = time.ticks_ms()
                        main_state = 31
            elif main_state == 33:
                if time.ticks_ms() - main_state_timer >= 20:
                    # run sliding motor in second speed
                    main_state_timer = time.ticks_ms()
                    sliding_motor.active(1)
                    main_state = 34
            elif main_state == 34:#30:                              # reach the sticker roller
                if roller_limit_pin.value() == 1:
                    rolling_motor.active(1)
                    sliding_motor.active(0)
                    rolling_motor_dir_pin.value(1)
                    set_sliding_backward()
                    clear_printer_controller()
                    main_state_timer = time.ticks_ms()
                    main_state = 300
            # -----------------------------start loop roller---------------------
            elif main_state == 300:
                if time.ticks_ms() - main_state_timer >= 300:
                    sliding_motor.active(1)
                    main_state = 301
                else: 
                    rolling_motor.active(1)
                    rolling_motor_dir_pin.value(1)
            # -----satrt--------------------------------------------------
            elif main_state == 301:
                if time.ticks_ms() - main_state_timer >= 20:
                    rolling_motor_dir_pin.value(0) #edit
                    main_state_timer = time.ticks_ms()
                    main_state = 302
            elif main_state == 302:
                if time.ticks_ms() - main_state_timer >= 200:
                    sliding_motor.active(0)
                    rolling_motor.active(0)
                    rolling_motor_dir_pin.value(1) #edit
                    on_solenoid1()
                    set_sliding_forward()
                    main_state_timer = time.ticks_ms()
                    main_state = 303
            elif main_state == 303:
                if time.ticks_ms() - main_state_timer >= 50:
                    off_solenoid1()
                    rolling_motor.active(1)
                    sliding_motor.active(1)
                    rolling_motor_dir_pin.value(1) #edit
                    main_state_timer = time.ticks_ms()
                    main_state = 304
            elif main_state == 304:
                if roller_limit_pin.value() == 1:
                    sliding_motor.active(0)
                    rolling_motor_dir_pin.value(1)
                    set_sliding_backward()    
                    main_state_timer = time.ticks_ms()
                    main_state = 305
            elif main_state == 305:
                if time.ticks_ms() - main_state_timer >= 200:
                    main_state_timer = time.ticks_ms()
                    main_state = 35       
            elif main_state == 35:
                if time.ticks_ms()-main_state_timer >= 550:
                    sliding_motor.active(1)
                    rolling_motor.active(0)
                    #on_solenoid1()
                    #on_solenoid3()
                    Off_rolling()
                    main_state_timer = time.ticks_ms()
                    main_state = 36
                if time.ticks_ms() - main_state_timer >= 450:
                    # on_solenoid1()
                    on_solenoid3()
            elif main_state == 36:#32:
                if time.ticks_ms() - main_state_timer >= 50:
                    on_solenoid1()
                    # on_solenoid3()
                    sliding_motor.active(0)
                    main_state_timer = time.ticks_ms()
                    main_state = 60
            elif main_state == 37:#33:
                if time.ticks_ms() - main_state_timer >= 400:
                    # off_solenoid1()
                    off_solenoid3()
                    sliding_motor.active(1)
                    set_sliding_forward()
                    main_state = 371
                    main_state_timer = time.ticks_ms()
            # ---------------------------------------------------------------------------
            elif main_state == 371:
                if time.ticks_ms() - main_state_timer >= 20:
                    sliding_motor.active(0)
                    set_sliding_backward()
                    main_state = 372
                    main_state_timer = time.ticks_ms()
            elif main_state == 372:
                if time.ticks_ms() - main_state_timer >= 20:
                    sliding_motor.active(1)
                    main_state = 38
                    main_state_timer = time.ticks_ms()
            # --------------------------------------------------------------------------------------
            elif main_state == 38:
                if time.ticks_ms() - main_state_timer >= 200:
                    off_solenoid1()
                    off_solenoid3()
                if box_location == 6 or time.ticks_ms() - main_state_timer >= 800:
                    if box_location == 6:
                        main_state = 39#35
                    else:
                        main_state_timer = time.ticks_ms()
                        sliding_motor.active(0)
                        set_sliding_forward()
                        main_state = 32#29
            elif main_state == 39:#35:
                if box_location == 7:
                    main_state = 40#36
            elif main_state == 40:#36:
                if box_location == 5:
                    # off_solenoid1()
                    main_state = 41#37
            elif main_state == 41:#37:
                if box_location == 5:
                    main_state = 42#38
            elif main_state == 42:#38:
                if box_location == 2:
                    main_state = 43#39
            elif main_state == 43:#39:
                if box_location == 7:
                    main_state = 44#40
            elif main_state == 44:#40:
                if box_location == 1:
                    main_state_timer = time.ticks_ms()
                #     sliding_motor.active(0)
                #     set_sliding_forward()
                    main_state = 444
                # resp_flag = False
                # device_resp_message = ""
            elif main_state == 444:
                if time.ticks_ms()-main_state_timer >= 20:
                    sliding_motor.active(0)
                    set_sliding_forward()
                    main_state = 45#41
                resp_flag = False
                device_resp_message = ""
            elif main_state == 45:#41:
                Off_sliding()
                pass
            
            elif main_state == 60:
                if time.ticks_ms() - main_state_timer >= 300:
                    main_state_timer = time.ticks_ms()
                    sliding_motor.active(1)
                    main_state =61
            elif main_state == 61:
                if time.ticks_ms() - main_state_timer >= 50:
                    sliding_motor.active(0)
                    main_state_timer = time.ticks_ms()
                    main_state = 62
            elif main_state == 62:
                if time.ticks_ms() - main_state_timer >= 50:
                    main_state_timer = time.ticks_ms()
                    sliding_motor.active(1)
                    main_state =63
            elif main_state == 63:
                if time.ticks_ms() - main_state_timer >= 50:
                    sliding_motor.active(0)
                    main_state_timer = time.ticks_ms()
                    main_state = 37            

            elif main_state == 50:
                if time.ticks_ms() - main_state_timer >= 200:#200
                    resp_flag = False
                    device_resp_message = ""
                    check_printer_state()
                    main_state_timer = time.ticks_ms()
                    main_state = 51
            elif main_state == 51:
                if time.ticks_ms() - main_state_timer >= 5:
                    main_state = 28

            #===================== stop silo =============================        
            elif main_state == 70:
                if time.ticks_ms() - main_state_timer >= 50: #100
                    stop_silo()
                    # on_solenoid1()
                    main_state_timer = time.ticks_ms()
                    main_state = 71      
            elif main_state == 71:
                if time.ticks_ms() - main_state_timer >=1000: #100
                    sliding_motor.active(0)
                    main_state_timer = time.ticks_ms()
                    main_state = 15 
            

        except:
            Off_sliding()
            main_state = 207
        # ============= error states =========
        #main_state == 200:             # printer module not response
        #main_state == 201:             # sliding box position is not origin
        #main_state == 202:             # prox sensor error
        #main_state == 203:             # sliding motor run to front limit switch
        #main_state == 204:             # silo module not response
        #main_state == 205:             # blood tube is jamming
        #main_state == 206:             # printer module not response
        #main_state == 207:              # there is an error from try condition
        #main_state == 208:             # can not go to roller

        if previous_state !=main_state:
            #pc_response(str(main_state))
            pass
                                    





