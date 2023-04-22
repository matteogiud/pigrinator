from steps import *
from time import sleep_ms
from math import pi

pins_motor_A = (23, 22, 21, 19)
st1 = Stepper_28BYJ_48(*pins_motor_A)

pins_motor_B = (16, 17, 5, 18)
st2 = Stepper_28BYJ_48(*pins_motor_B)
    
motors = CarMotors(st1,st2, delay_ms=3)
motors.forward_cm(20)
sleep_ms(1000)
motors.left(90, delay_ms=4)
sleep_ms(1000)
motors.forward_cm(20)
sleep_ms(1000)
motors.left(90, delay_ms=4)
sleep_ms(1000)
motors.forward_cm(20)
sleep_ms(1000)
motors.left(90, delay_ms=4)
sleep_ms(1000)
motors.forward_cm(20)
sleep_ms(1000)
motors.left(90, delay_ms=4)


