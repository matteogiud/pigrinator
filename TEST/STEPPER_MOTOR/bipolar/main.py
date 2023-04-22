from bipolar_stepper import *
from time import sleep_ms
from math import pi

pins_motor_A = (12, 14, 27, 16)
bp_st1 = Stepper_28BYJ_48_bipolar(*pins_motor_A)

pins_motor_B = (16, 17, 5, 18)
bp_st2 = Stepper_28BYJ_48_bipolar(*pins_motor_B)

motors = CarMotors(bp_st1, bp_st2)
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
