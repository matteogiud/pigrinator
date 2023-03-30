from machine import Pin, PWM
import time

# enA = PWM(Pin(26))
in1 = Pin(27, Pin.OUT)
in2 = Pin(14, Pin.OUT)
in3 = Pin(33, Pin.OUT)
in4 = Pin(32, Pin.OUT)
enA = Pin(26, Pin.OUT)
enB = Pin(25, Pin.OUT)
led = Pin(2, Pin.OUT)


def motor_forward():
    in1.value(1)
    in2.value(0)
    enA.value(1)
    in3.value(1)
    in4.value(0)
    enB.value(1)


def motor_backward():
    in1.value(0)
    in2.value(1)
    enA.value(1)
    in3.value(0)
    in4.value(1)
    enB.value(1)


def motor_stop():
    in1.value(0)
    in2.value(0)
    enA.value(0)
    in3.value(0)
    in4.value(0)
    enB.value(0)


motor_forward()
# while True:
#     motor_forward()
#     led.on()
#     time.sleep(1)
#     motor_backward()
#     led.off()
#     time.sleep(1)
#     motor_stop()
#     led.on()

