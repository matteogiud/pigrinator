from bipolar_stepper_like_arduino import *
import time

stepsPerRevolution = 32

stp1 = Stepper(stepsPerRevolution, 13, 12, 14, 27)
stp2 = Stepper(stepsPerRevolution, 26, 25, 33, 32)

car_motors = CarMotors(stp1, stp2)

car_motors.forward_cm(20)
time.sleep(1)
car_motors.left(90)
time.sleep(1)
car_motors.forward_cm(20)
time.sleep(1)

    


# while True:
#     for i in range(4):
#         stp1.step_motor(i)
#         stp2.step_motor(i)
#         time.sleep(0.002)
