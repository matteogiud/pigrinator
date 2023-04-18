from lib.Stepper import StepperMotor, CarMotors
from machine import Pin

step_motor_A = StepperMotor(26, 25, 33, 32)
step_motor_B = StepperMotor(16, 17, 05, 18)

car_motors = CarMotors(step_motor_A, step_motor_B)


# car_motors.forward(1024,1000)
