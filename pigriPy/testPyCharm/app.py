from machine import Pin
from motorsDriver import MotorsDriver


MD = MotorsDriver(Pin(27, Pin.OUT), Pin(14, Pin.OUT), Pin(33, Pin.OUT), Pin(32, Pin.OUT), Pin(26, Pin.OUT), Pin(25, Pin.OUT))
MD.forward()