from machine import Pin
import time

# define IO pins
led_pin = Pin(25,Pin.OUT)       # onboard led pin
s1_pin = Pin(16,Pin.IN)        # tube detector sensor
s2_pin = Pin(17,Pin.IN)
s3_pin = Pin(18,Pin.IN)

s4_pin = Pin(19,Pin.IN)         # sticker on tube sensor if '1' on m2 motor

m1_pin1 = Pin(26,Pin.OUT)       # drop tube motor
m1_pin2 = Pin(27,Pin.OUT)       # 01 => close       10 = > open

m2_pin1 = Pin(20,Pin.OUT)       # rolling tube
m2_pin2 = Pin(21,Pin.OUT)       # write 10

hall_pin = Pin(28,Pin.IN)               # magnetic detect get '0'

s4_forward_pin = Pin(11,Pin.OUT)        # io interfaces to master node
drop_tube_pin = Pin(12,Pin.IN)
tube_detect_pin = Pin(13,Pin.OUT)

# for i in range(20):
#     m1_pin1.value(1)
#     m1_pin2.value(0)
#     time.sleep(0.1)
#     m1_pin1.value(0)
#     time.sleep(2)
#     m1_pin2.value(1)
#     while hall_pin.value() == 1:
#         pass
#     m1_pin2.value(0)
#     time.sleep(1)

m1_pin1.value(0)
m1_pin2.value(1)
while hall_pin.value() == 1:
    pass
m1_pin2.value(0)




