import time
from pymodbus.client import ModbusSerialClient as ModbusClient
from mysql.connector import connect 

time.sleep(3)
client = ModbusClient(method='rtu',port='COM8',stopbitd=1,bytesize=8,parity='N',baudrate=9600,timeout=1)
connection = client.connect()
db_connector =  connect(host="localhost", user="root", port = 3333, passwd="edgelabeling555",  db="sbj",  charset="utf8"  )
database_cursor = db_connector.cursor()
time.sleep(20)

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

def on_lamp1():
    time.sleep(1)
    modbus_result = client.write_coil(address=0,value=1,unit=0xFF)
def on_lamp2():
    time.sleep(1)
    modbus_result = client.write_coil(address=1,value=1,unit=0xFF)
def on_lamp3():
    time.sleep(1)
    modbus_result = client.write_coil(address=2,value=1,unit=0xFF)
def on_lamp4():
    time.sleep(1)
    modbus_result = client.write_coil(address=3,value=1,unit=0xFF)
def off_all_lamp():
    time.sleep(1)
    modbus_result = client.write_coil(address=0,value=0,unit=0xFF)
    modbus_result = client.write_coil(address=1,value=0,unit=0xFF)
    modbus_result = client.write_coil(address=2,value=0,unit=0xFF)
    modbus_result = client.write_coil(address=3,value=0,unit=0xFF)

while True:
    time.sleep(2)
    result = read_cmd()
    if len(result) > 0:
        cmd = result[0]
        match cmd[0]:
            case 1:
                on_lamp1()
                clear_flag()
            case 2:
                on_lamp2()
                clear_flag()
            case 3:
                on_lamp3()
                clear_flag()
            case 4:
                on_lamp4()
                clear_flag()
            case others:
                off_all_lamp()
                clear_flag()
db_connector.close()
