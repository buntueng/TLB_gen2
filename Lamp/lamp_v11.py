import time
from mysql.connector import connect 
import serial

ser = serial.Serial(
        port='COM8',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.5 )


# on-off message
onRelay1 = [0x01,0x05,0x00,0x00,0xFF,0x00,0x8C,0x3A]
offRelay1 = [0x01,0x05,0x00,0x00,0x00,0x00,0xCD,0xCA]
onRelay2 = [0x01,0x05,0x00,0x01,0xFF,0x00,0xDD,0xFA]
offRelay2 = [0x01,0x05,0x00,0x01,0x00,0x00,0x9C,0x0A]
onRelay3 = [0x01,0x05,0x00,0x02,0xFF,0x00,0x2D,0xFA]
offRelay3 = [0x01,0x05,0x00,0x02,0x00,0x00,0x6C,0x0A]
onRelay4 = [0x01,0x05,0x00,0x03,0xFF,0x00,0x7C,0x3A]
offRelay4 = [0x01,0x05,0x00,0x03,0x00,0x00,0x3D,0xCA]

db_connector =  connect(host="localhost", user="root", port = 3333, passwd="edgelabeling555",  db="sbj",  charset="utf8"  )
database_cursor = db_connector.cursor()
#time.sleep(20)

def read_cmd():
    result_list = []
    try:
        sql_query = 'SELECT lamp_number FROM TLB_Lamp WHERE flag = 1 ORDER BY time_stamp DESC LIMIT 1'
        database_cursor.execute(sql_query)
        result_list = database_cursor.fetchall()
        print(result_list)
    except:
        pass
    return result_list
def clear_flag():
    sql_query = 'UPDATE TLB_Lamp SET flag = 0 WHERE flag = 1 ORDER BY time_stamp DESC LIMIT 1'
    database_cursor.execute(sql_query)
    db_connector.commit()

def on_lamp1():
    hexMessage = serial.to_bytes(onRelay1)
    ser.write(hexMessage)
    time.sleep(0.5)
    ser.read(10)

def on_lamp2():
    hexMessage = serial.to_bytes(onRelay2)
    ser.write(hexMessage)
    time.sleep(0.5)
    ser.read(10)

def on_lamp3():
    hexMessage = serial.to_bytes(onRelay3)
    ser.write(hexMessage)
    time.sleep(0.5)
    ser.read(10)

def on_lamp4():
    hexMessage = serial.to_bytes(onRelay4)
    ser.write(hexMessage)
    time.sleep(0.5)
    ser.read(10)

def off_all_lamp():
    hexMessage = serial.to_bytes(offRelay1)
    ser.write(hexMessage)
    time.sleep(0.5)
    ser.read(10)

    hexMessage = serial.to_bytes(offRelay2)
    ser.write(hexMessage)
    time.sleep(0.5)
    ser.read(10)

    hexMessage = serial.to_bytes(offRelay3)
    ser.write(hexMessage)
    time.sleep(0.5)
    ser.read(10)

    hexMessage = serial.to_bytes(offRelay4)
    ser.write(hexMessage)
    time.sleep(0.5)
    ser.read(10)

while True:
    time.sleep(2)
    result = read_cmd()
    if len(result) > 0:
        cmd = result[0]
        lamp_number = cmd[0]
        if lamp_number == 1:
            print("on lamp1")
            on_lamp1()
            clear_flag()
        elif lamp_number == 2:
            print("on lamp2")
            on_lamp2()
            clear_flag()
        elif lamp_number == 3:
            print("on lamp3")
            on_lamp3()
            clear_flag()
        elif lamp_number == 4:
            print("on lamp4")
            on_lamp4()
            clear_flag()
        if lamp_number == b'1':
            print("on lamp1")
            on_lamp1()
            clear_flag()
        elif lamp_number == b'2':
            print("on lamp2")
            on_lamp2()
            clear_flag()
        elif lamp_number == b'3':
            print("on lamp3")
            on_lamp3()
            clear_flag()
        elif lamp_number == b'4':
            print("on lamp4")
            on_lamp4()
            clear_flag()
        else:
            print("off all lamp")
            off_all_lamp()
            clear_flag()
db_connector.close()
