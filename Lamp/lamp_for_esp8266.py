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

def R1():
    ser.write("R1\n".encode())
def R2():
    ser.write("R2\n".encode())
def R3():
    ser.write("R3\n".encode())
def R4():
    ser.write("R4\n".encode())
def R0():
    ser.write("R0\n".encode())

db_connector =  connect(host="localhost", user="root", port = 3333, passwd="edgelabeling555",  db="sbj",  charset="utf8"  )
database_cursor = db_connector.cursor()

def read_cmd():
    result_list = []
    try:
        sql_query = 'SELECT lamp_number FROM TLB_Lamp WHERE flag = 1 ORDER BY time_stamp DESC LIMIT 1'
        database_cursor.execute(sql_query)
        result_list = database_cursor.fetchall()
    except:
        pass
    return result_list

def clear_flag():
    sql_query = 'UPDATE TLB_Lamp SET flag = 0 WHERE flag = 1 ORDER BY time_stamp DESC LIMIT 1'
    database_cursor.execute(sql_query)
    db_connector.commit()
R1()
time.sleep(0.5)
R2()
time.sleep(0.5)
R3()
time.sleep(0.5)
R4()
time.sleep(0.5)
R0()
time.sleep(0.5)

while True:
    time.sleep(2)
    result = read_cmd()
    if len(result) > 0:
        cmd = result[0]
        lamp_number = cmd[0]
        lamp_number = lamp_number.decode('utf-8')
        if lamp_number == '1':
            R0()
            time.sleep(0.1)
            R1()
            time.sleep(0.2)
            clear_flag()
        elif lamp_number == '2':
            R0()
            time.sleep(0.1)
            R2()
            time.sleep(0.2)
            clear_flag()
        elif lamp_number == '3':
            R0()
            time.sleep(0.1)
            R3()
            time.sleep(0.2)
            clear_flag()
        elif lamp_number == '4':
            R0()
            time.sleep(0.1)
            R4()
            time.sleep(0.2)
            clear_flag()
        elif lamp_number == '0':
            R0()
            time.sleep(0.2)
            clear_flag()
db_connector.close()