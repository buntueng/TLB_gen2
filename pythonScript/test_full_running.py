import serial   
import time 
comport = 'COM7'
ser = serial.Serial(port=comport,baudrate=115200,timeout=1)
time.sleep(3)
cmd = "1r\n"
cmd_bytes = cmd.encode()
ser.write(cmd_bytes)
time.sleep(5)

for loop_counter in range(0,100):
    print("===============================")
    print("loop: ",loop_counter+1)
    for box_number in range(1,5):
        resp = ser.readall()
        print(resp)
        message = '1g'+str(box_number)+"\n"
        message_bytes = message.encode()
        ser.write(message_bytes)
        print("box number: ",box_number)
        time.sleep(8)
    