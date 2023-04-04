from machine import Pin, PWM
from motorsDriver import MotorsDriver


MD = MotorsDriver(Pin(27, Pin.OUT), Pin(14, Pin.OUT), Pin(33, Pin.OUT), Pin(32, Pin.OUT), PWM(Pin(26, Pin.OUT)), PWM(Pin(25, Pin.OUT)))
MD.forward()