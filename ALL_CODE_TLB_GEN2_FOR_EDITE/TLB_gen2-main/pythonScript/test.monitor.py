import serial   
import time 
comport = 'COM3'
ser = serial.Serial(port=comport,baudrate=115200,timeout=1)
time.sleep(3)

while True:
    resp = ser.readall()
    print(resp)
    print(ser.readline())
    pass