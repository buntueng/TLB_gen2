from machine import Pin, UART, reset
import time

device_id = '2'
master_command = ""
execute_flag = False
running_state = 0



signal_1 = Pin(2,Pin.OUT)
signal_2 = Pin(3,Pin.OUT)
signal_3 = Pin(6,Pin.OUT)

limit_box1_release_tube = Pin(10,Pin.IN,Pin.PULL_UP)
limit_box1_select_tube = Pin(11,Pin.IN,Pin.PULL_UP)

release_tube_box1 = False
silo_box1_state = 0
silo1_time = 0


reset_4_relay = Pin(7,Pin.OUT)
reset_4_relay.value(1)

device_link = UART(1, baudrate=9600, bits=8, parity=None, stop=1,tx=Pin(8), rx=Pin(9),timeout=1000)
release_tube_command = UART(0, baudrate=9600, bits=8, parity=None, stop=1,tx=Pin(0), rx=Pin(1),timeout=1000)

device_link.read()              # clear data in serial port buffer
release_tube_command.read()     # clear data in serial port buffer

def resp_485(message):
    resp_message = device_id + message
    device_link.write(bytes( ord(ch) for ch in resp_message))

def silo1_run():
    message = '21\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))

def silo2_run():
    message = '22\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))

def silo3_run():
    message = '23\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))

def silo4_run():
    message = '24\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))

def silo5_run():
    message = '25\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))

def silo6_run():
    message = '26\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))
    print("silo")

def stop_silo():
    message = '20\n'
    release_tube_command.write( bytes( ord(ch) for ch in message))


def on_motor1():
    signal_1.value(0)
    signal_2.value(1)
    signal_3.value(1)

def on_motor2():
    signal_1.value(1)
    signal_2.value(0)
    signal_3.value(1)

def on_motor3():
    signal_1.value(1)
    signal_2.value(1)
    signal_3.value(0)

def on_motor4():
    signal_1.value(0)
    signal_2.value(0)
    signal_3.value(1)

def off_all_motor():
    signal_1.value(1)
    signal_2.value(1)
    signal_3.value(1)

def on_all():
    signal_1.value(0)
    signal_2.value(0)
    signal_3.value(0)

def reset_relay_motor():
    reset_4_relay.value(0)
    time.sleep(0.1)
    reset_4_relay.value(1)

off_all_motor()
reset_relay_motor()



while True:
    # print(limit_box1_release_tube.value())
    time.sleep(0.1)
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
                    release_tube_box1 = True
                    # print("m1")
                    silo6_run()
                    message = "M1 OK\n"
                    resp_485(message=message)
                if master_command[1] == '2':
                    stop_silo()
                    off_all_motor()
                    on_motor2()
                    # print("m2")
                    message = "M2 OK\n"
                    resp_485(message=message)
                if master_command[1] == '3':
                    stop_silo()
                    off_all_motor()
                    on_motor3()
                    # print("m3")
                    message = "M3 OK\n"
                    resp_485(message=message)
                if master_command[1] == '4':
                    stop_silo()
                    off_all_motor()
                    on_motor4()
                    # print("m4")
                    message = "M4 OK\n"
                    resp_485(message=message)
                if master_command[1] == '0':
                    off_all_motor()
                    stop_silo()
                    # print("off")
                    message = "OFF OK\n"
                    resp_485(message=message)
                if master_command[1] == 'r':
                    if master_command[2] == '1':
                        off_all_motor()
                        reset_relay_motor()
                        message = "RESET RELAY SUCCESS\n"
                        resp_485(message=message)
                    if master_command[2] == '2':
                        message = "RESET SUCCESS\n"
                        resp_485(message=message)
                        reset()

        execute_flag = False
        master_command = ""

    try:
        # if running_box1_state:
        if silo_box1_state == 0:
            print("1")
            if limit_box1_release_tube.value() == 1:
                silo_box1_state = 4
                # off_all_motor()
                print("2")
            if limit_box1_release_tube.value() == 0:
                on_motor1()
                silo_box1_state = 1
                print("3")

        elif silo_box1_state == 1:
            print("4")
            if limit_box1_select_tube.value() == 1:
                silo_box1_state = 2
                silo1_time = time.ticks_ms()
                print("5")
        
        elif silo_box1_state == 2:
            if time.ticks_ms() - silo1_time >= 2000:
                off_all_motor()
                print("6")
                silo_box1_state = 3

        elif silo_box1_state == 3:
            silo6_run()
            print("7")
            silo_box1_state = 4

        elif silo_box1_state == 4:
            print("eee")
            if limit_box1_release_tube.value() == 1:
                stop_silo()
                off_all_motor()
                print("8")
                silo_box1_state = 5

        elif silo_box1_state == 5:
            off_all_motor()
            if release_tube_box1 == True:
                silo6_run()
                print("9")
                silo1_time = time.ticks_ms()
                silo_box1_state = 6
            else:
                off_all_motor()
                stop_silo()
                print("10")
        
        elif silo_box1_state == 6:
            if time.ticks_ms() - silo1_time >= 1000:
                stop_silo()
                print("11")
                release_tube_box1 = False
                silo_box1_state = 0

    except:
        stop_silo()
        off_all_motor()
        message = "ERROR"
        resp_485(message=message)