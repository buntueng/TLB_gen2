from machine import Pin, PWM, UART,reset
import time 

device_id = '2'
master_command = ""
execute_flag = False

# 1 = 65535
# 1/2 = 32767
# 1/4 = 16383

DC_freq = 1000
DC_PWM = 65535

box1_limit_select_tube = Pin(10,Pin.IN,Pin.PULL_UP)
box1_limit_release_tube = Pin(11,Pin.IN,Pin.PULL_UP)

box2_limit_select_tube = Pin(12,Pin.IN,Pin.PULL_UP)
box2_limit_release_tube = Pin(13,Pin.IN,Pin.PULL_UP)

box3_limit_select_tube = Pin(14,Pin.IN,Pin.PULL_UP)
box3_limit_release_tube = Pin(15,Pin.IN,Pin.PULL_UP)

box4_limit_select_tube = Pin(16,Pin.IN,Pin.PULL_UP)
box4_limit_release_tube = Pin(17,Pin.IN,Pin.PULL_UP)

# box5_limit_select_tube = Pin(00,Pin.IN,Pin.PULL_UP)
# box5_limit_release_tube = Pin(00,Pin.IN,Pin.PULL_UP)

# box6_limit_select_tube = Pin(00,Pin.IN,Pin.PULL_UP)
# box6_limit_release_tube = Pin(00,Pin.IN,Pin.PULL_UP)

motor_DC_1 = PWM(Pin(6))
motor_DC_2 = PWM(Pin(7))
motor_DC_3 = PWM(Pin(8))
motor_DC_4 = PWM(Pin(9))

motor_DC_1.freq(DC_freq)
motor_DC_2.freq(DC_freq)
motor_DC_3.freq(DC_freq)
motor_DC_4.freq(DC_freq)

device_link = UART(0, baudrate=9600, bits=8, parity=None, stop=1,tx=Pin(0), rx=Pin(1),timeout=1000)
release_tube_command = UART(1, baudrate=9600, bits=8, parity=None, stop=1,tx=Pin(4), rx=Pin(5),timeout=1000)
device_link.read()              # clear data in serial port buffer
release_tube_command.read()     # clear data in serial port buffer

def resp_485(message):
    resp_message = device_id + message
    device_link.write(bytes( ord(ch) for ch in resp_message))

def run_motor1_DC():
    motor_DC_1.duty_u16(DC_PWM)

def stop_motor1_DC():
    motor_DC_1.duty_u16(0)

def run_motor2_DC():
    motor_DC_2.duty_u16(DC_PWM)

def stop_motor2_DC():
    motor_DC_2.duty_u16(0)

def run_motor3_DC():
    motor_DC_3.duty_u16(DC_PWM)

def stop_motor3_DC():
    motor_DC_3.duty_u16(0)

def run_motor4_DC():
    motor_DC_4.duty_u16(DC_PWM)

def stop_motor4_DC():
    motor_DC_4.duty_u16(0)

def silo1_run():
    message = '21\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))

def stop_silo1():
    message = '2s1\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))

def silo2_run():
    message = '22\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))

def stop_silo2():
    message = '2s2\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))

def silo3_run():
    message = '23\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))
 
def stop_silo3():
    message = '2s3\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))

def silo4_run():
    message = '24\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))

def stop_silo4():
    message = '2s4\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))

def silo5_run():
    message = '25\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))

def stop_silo5():
    message = '2s5\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))

def silo6_run():
    message = '26\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))

def stop_silo6():
    message = '2s6\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))

def stop_silo():
    message = '20\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))

def stop_all_DC_motor():
    motor_DC_1.duty_u16(0)
    motor_DC_2.duty_u16(0)
    motor_DC_3.duty_u16(0)
    motor_DC_4.duty_u16(0)

def stop_all_silo():
    message = '20\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))

stop_all_silo()
stop_all_DC_motor()


box1_running_flage = False
box2_running_flage = False
box3_running_flage = False
box4_running_flage = False
box5_running_flage = False
box6_running_flage = False

box1_timer = 0
box2_timer = 0
box3_timer = 0
box4_timer = 0
box5_timer = 0
box6_timer = 0

box1_state = 0
box2_state = 0
box3_state = 0
box4_state = 0
box5_state = 0
box6_state = 0

wait_select_tube_motor = 1150
wait_tube = 500

while True:
    if(device_link.any()):
        char_cmd = device_link.read(1)
        char_cmd = char_cmd.decode()
        if char_cmd == '\n':
            execute_flag = True
        else:
            master_command = master_command + char_cmd 

    if execute_flag == True:
        if len(master_command) > 0:
            if master_command[0] == device_id:
                if master_command[1] == '1':
                    # print(master_command)
                    box1_state = 100
                    message = "M1 OK\n"
                    resp_485(message=message)

                elif master_command[1] == '2':
                    # print(master_command)
                    box2_state = 100
                    message = "M2 OK\n"
                    resp_485(message=message)

                elif master_command[1] == '3':
                    # print(master_command)
                    box3_state = 100
                    message = "M3 OK\n"
                    resp_485(message=message)

                elif master_command[1] == '4':
                    # print(master_command)
                    box4_state = 100
                    message = "M4 OK\n"
                    resp_485(message=message)

                elif master_command[1] == '0':
                    stop_all_DC_motor()
                    stop_all_silo()
                    message = "STOP\n"
                    resp_485(message=message)


        execute_flag = False
        master_command = ""
# ========================================================= BOX 1 =====================================================
    
    if box1_state == 0:
        if box1_limit_release_tube.value() == 0:
            time.sleep(0.5)
            if box1_limit_release_tube.value() == 0:
                box1_state = 1
                box1_timer = time.ticks_ms()
           
    elif box1_state == 1:
        if time.ticks_ms() - box1_timer >= 50:
            if box1_limit_release_tube.value() == 0:
                run_motor1_DC()
                box1_state = 2

    elif box1_state == 2:
        if box1_limit_select_tube.value() == 0:
            pass
        else:
            box1_state = 3

    elif box1_state == 3:
        if box1_limit_select_tube.value() == 1:
            box1_state = 4
            box1_timer = time.ticks_ms()

    elif box1_state == 4:
        if time.ticks_ms() - box1_timer >= wait_select_tube_motor + 100:
            stop_motor1_DC()
            box1_timer = time.ticks_ms()
            box1_state = 5

    elif box1_state == 5:
        if box1_limit_release_tube.value() == 1:
            pass
        else:
            if time.ticks_ms() - box1_timer >= wait_tube:
                silo1_run()
                box1_state = 6
    
    elif box1_state == 6:
        if box1_limit_release_tube.value() == 1:
            box1_timer = time.ticks_ms()
            box1_state = 7

    elif box1_state == 7:
        if time.ticks_ms() - box1_timer >= 50:
            stop_silo1()
            box1_state = 8

    elif box1_state == 100:
        if box1_limit_release_tube.value() == 1:
            silo1_run()
            box1_state = 101
        else :
            box1_state = 0

    elif box1_state == 101:
        if box1_limit_release_tube.value() == 0:
            box1_timer = time.ticks_ms()
            box1_state = 102

    elif box1_state == 102:
        if time.ticks_ms() - box1_timer >= 300:
            stop_silo1()
            box1_timer = time.ticks_ms()
            # print("101")
            box1_state = 0
            
# ========================================================= BOX 2 =====================================================
    
    if box2_state == 0:
        if box2_limit_release_tube.value() == 0:
            time.sleep(0.5)
            if box2_limit_release_tube.value() == 0:
                box2_state = 1
                box2_timer = time.ticks_ms()
           
    elif box2_state == 1:
        if time.ticks_ms() - box2_timer >= 50:
            if box2_limit_release_tube.value() == 0:
                run_motor2_DC()
                box2_state = 2

    elif box2_state == 2:
        if box2_limit_select_tube.value() == 0:
            pass
        else:
            box2_state = 3

    elif box2_state == 3:
        if box2_limit_select_tube.value() == 1:
            box2_state = 4
            box2_timer = time.ticks_ms()

    elif box2_state == 4:
        if time.ticks_ms() - box2_timer >= wait_select_tube_motor + 70:
            stop_motor2_DC()
            box2_timer = time.ticks_ms()
            box2_state = 5

    elif box2_state == 5:
        if box2_limit_release_tube.value() == 1:
            pass
        else:
            if time.ticks_ms() - box2_timer >= wait_tube:
                silo2_run()
                box2_state = 6
    
    elif box2_state == 6:
        if box2_limit_release_tube.value() == 1:
            box2_timer = time.ticks_ms()
            box2_state = 7

    elif box2_state == 7:
        if time.ticks_ms() - box2_timer >= 50:
            stop_silo2()
            box2_state = 8

    elif box2_state == 100:
        if box2_limit_release_tube.value() == 1:
            silo2_run()
            box2_state = 101
        else :
            box2_state = 0

    elif box2_state == 101:
        if box2_limit_release_tube.value() == 0:
            box2_timer = time.ticks_ms()
            box2_state = 102

    elif box2_state == 102:
        if time.ticks_ms() - box2_timer >= 300:
            stop_silo2()
            box2_timer = time.ticks_ms()
            # print("101")
            box2_state = 0
            
# ========================================================= BOX 3 =====================================================
    
    if box3_state == 0:
        if box3_limit_release_tube.value() == 0:
            time.sleep(0.5)
            if box3_limit_release_tube.value() == 0:
                box3_state = 1
                box3_timer = time.ticks_ms()
           
    elif box3_state == 1:
        if time.ticks_ms() - box3_timer >= 50:
            if box3_limit_release_tube.value() == 0:
                run_motor3_DC()
                box3_state = 2

    elif box3_state == 2:
        if box3_limit_select_tube.value() == 0:
            pass
        else:
            box3_state = 3

    elif box3_state == 3:
        if box3_limit_select_tube.value() == 1:
            box3_state = 4
            box3_timer = time.ticks_ms()

    elif box3_state == 4:
        if time.ticks_ms() - box3_timer >= wait_select_tube_motor-100:
            stop_motor3_DC()
            box3_timer = time.ticks_ms()
            box3_state = 5

    elif box3_state == 5:
        if box3_limit_release_tube.value() == 1:
            pass
        else:
            if time.ticks_ms() - box3_timer >= wait_tube:
                silo3_run()
                box3_state = 6
    
    elif box3_state == 6:
        if box3_limit_release_tube.value() == 1:
            box3_timer = time.ticks_ms()
            box3_state = 7

    elif box3_state == 7:
        if time.ticks_ms() - box3_timer >= 50:
            stop_silo3()
            box3_state = 8

    elif box3_state == 100:
        if box3_limit_release_tube.value() == 1:
            silo3_run()
            box3_state = 101
        else :
            box3_state = 0

    elif box3_state == 101:
        if box3_limit_release_tube.value() == 0:
            box3_timer = time.ticks_ms()
            box3_state = 102

    elif box3_state == 102:
        if time.ticks_ms() - box3_timer >= 300:
            stop_silo3()
            box3_timer = time.ticks_ms()
            # print("101")
            box3_state = 0
            
# ========================================================= BOX 4 =====================================================
    
    if box4_state == 0:
        if box4_limit_release_tube.value() == 0:
            time.sleep(0.5)
            if box4_limit_release_tube.value() == 0:
                box4_state = 1
                box4_timer = time.ticks_ms()
           
    elif box4_state == 1:
        if time.ticks_ms() - box4_timer >= 50:
            if box4_limit_release_tube.value() == 0:
                run_motor4_DC()
                box4_state = 2

    elif box4_state == 2:
        if box4_limit_select_tube.value() == 0:
            pass
        else:
            box4_state = 3

    elif box4_state == 3:
        if box4_limit_select_tube.value() == 1:
            box4_state = 4
            box4_timer = time.ticks_ms()

    elif box4_state == 4:
        if time.ticks_ms() - box4_timer >= wait_select_tube_motor + 150:
            stop_motor4_DC()
            box4_timer = time.ticks_ms()
            box4_state = 5

    elif box4_state == 5:
        if box4_limit_release_tube.value() == 1:
            pass
        else:
            if time.ticks_ms() - box4_timer >= wait_tube:
                silo4_run()
                box4_state = 6
    
    elif box4_state == 6:
        if box4_limit_release_tube.value() == 1:
            box4_timer = time.ticks_ms()
            box4_state = 7

    elif box4_state == 7:
        if time.ticks_ms() - box4_timer >= 20:
            stop_silo4()
            box4_state = 8

    elif box4_state == 100:
        if box4_limit_release_tube.value() == 1:
            silo4_run()
            box4_state = 101
        else :
            box4_state = 0

    elif box4_state == 101:
        if box4_limit_release_tube.value() == 0:
            box4_timer = time.ticks_ms()
            box4_state = 102

    elif box4_state == 102:
        if time.ticks_ms() - box4_timer >= 300:
            stop_silo4()
            box4_timer = time.ticks_ms()
            # print("101")
            box4_state = 0
            