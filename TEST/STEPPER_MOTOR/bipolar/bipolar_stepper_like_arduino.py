from utime import sleep_us, ticks_us
from machine import Pin


class Stepper:

    def __init__(self, number_of_steps: int, motor_pin_1: int, motor_pin_2: int, motor_pin_3: int, motor_pin_4: int):
        self.step_number = 0
        self.direction = 0
        self.last_step_time = 0
        self.number_of_steps = number_of_steps

        self.motor_pin_1 = Pin(motor_pin_1, Pin.OUT)
        self.motor_pin_2 = Pin(motor_pin_2, Pin.OUT)
        self.motor_pin_3 = Pin(motor_pin_3, Pin.OUT)
        self.motor_pin_4 = Pin(motor_pin_4, Pin.OUT)
        

    def set_speed(self, what_speed: int):
        self.step_delay = 60 * 1000 * 1000 / self.number_of_steps / what_speed
        

    def step(self, step_to_move: int):
        steps_left = abs(step_to_move)

        self.direction = 1 if step_to_move > 0 else 0

        while steps_left > 0:
            now = ticks_us()

            if now - self.last_step_time >= self.step_delay:
                self.last_step_time = now

                if self.direction == 1:
                    self.step_number += 1
                    if self.step_number == self.number_of_steps:
                        self.step_number = 0

                else:
                    if self.step_number == 0:
                        self.step_number = self.number_of_steps

                    self.step_number -= 1

                steps_left -= 1

                self.step_motor(self.step_number % 4)
            else:
                sleep_us(50)

    def step_motor(self, this_step: int):
        if this_step == 0:
            self.motor_pin_1.on()
            self.motor_pin_2.off()
            self.motor_pin_3.on()
            self.motor_pin_4.off()
        if this_step == 1:
            self.motor_pin_1.off()
            self.motor_pin_2.on()
            self.motor_pin_3.on()
            self.motor_pin_4.off()
        if this_step == 2:
            self.motor_pin_1.off()
            self.motor_pin_2.on()
            self.motor_pin_3.off()
            self.motor_pin_4.on()
        if this_step == 3:
            self.motor_pin_1.on()
            self.motor_pin_2.off()
            self.motor_pin_3.off()
            self.motor_pin_4.on()
            
            
            
class CarMotors:
    
    def __init__(self, motor_A: Stepper, motor_B: Stepper, wheels_diameter_cm=6.7, wheels_distances_cm=13.5, motors_speed = 900):
        import math
        self.motor_A = motor_A
        self.motor_B = motor_B
        self.wheels_circumference_cm = math.pi*wheels_diameter_cm
        self.steps_per_revolution = 2048
        self.wheels_distances_cm = wheels_distances_cm
        self.motor_A.set_speed(motors_speed)
        self.motor_B.set_speed(motors_speed)

        
#     def steps(self, count, dir=False, delay_ms=None):
#         from time import sleep_ms
# 
#         for i in range(count):
#             self.motor_A.one_step(dir)
#             self.motor_B.one_step(dir)
#             sleep_ms(self.delay_ms if delay_ms is None else delay_ms)
#         self.motor_A.reset()
#         self.motor_B.reset()
    
    
    def forward_cm(self, distance_cm):
        steps = int(distance_cm * self.steps_per_revolution / self.wheels_circumference_cm)

        for i in range(steps):
            self.motor_A.step(-1)
            self.motor_B.step(-1)        
        
    def backward_cm(self, distance_cm):
        steps = int(distance_cm * self.steps_per_revolution / self.wheels_circumference_cm)

        for i in range(steps):
            self.motor_A.step(1)
            self.motor_B.step(1)
                
    def left(self, degrees):
        from math import pi
        distance_cm = (self.wheels_distances_cm * pi) * degrees / 360
        steps = int(distance_cm * self.steps_per_revolution / self.wheels_circumference_cm)             
        
        for i in range(steps):
            self.motor_A.step(1)
            self.motor_B.step(-1)
        
    def right(self, degrees):
        from time import sleep_ms
        distance_cm = (self.wheels_distances_cm * degrees) / 2
        steps = int(distance_cm * self.steps_per_revolution / self.wheels_circumference_cm)    
        
        
        for i in range(steps):
            self.motor_A.step(-1)
            self.motor_B.step(1)
         
