import serial 
import time

ser1 = serial.Serial(
        port='COM5',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.5 )

ser1.flush()
ser1.read(100)

def box1():
    ser1.write("21\n".encode())
    print("Box1")

def box2():
    ser1.write("22\n".encode())
    print("Box2")

def box3():
    ser1.write("23\n".encode())
    print("Box3")

def box4():
    ser1.write("24\n".encode())
    print("Box4")

def box5():
    ser1.write("25\n".encode())
    print("Box5")

def box6():
    ser1.write("26\n".encode())
    print("Box6")

def stop_all():
    ser1.write("20\n".encode())
    print("Stop Box")

delay = 5
stop_all()
time.sleep(2)
for i in range(100):
    print(i)
    time.sleep(3)
    box1()
    time.sleep(2)
    box2()
    time.sleep(2)
    box3()
    time.sleep(2)
    box4()
    time.sleep(2)
    print("loop"+str(i))
    time.sleep(5)
    print(time)
