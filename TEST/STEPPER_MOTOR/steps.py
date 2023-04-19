class Stepper_28BYJ_48:
    def __init__(self, pin1, pin2, pin3, pin4):
        from machine import Pin
        self.pin1 = Pin(pin1, Pin.OUT)
        self.pin2 = Pin(pin2, Pin.OUT)
        self.pin3 = Pin(pin3, Pin.OUT)
        self.pin4 = Pin(pin4, Pin.OUT)
        self.__step_number = 0
        self.steps_per_revolution = 2048

    def one_step(self, dir: bool):
        if (dir):
            if self.__step_number == 0:
                self.pin1.on()
                self.pin2.off()
                self.pin3.off()
                self.pin4.off()
            elif self.__step_number == 1:
                self.pin1.off()
                self.pin2.on()
                self.pin3.off()
                self.pin4.off()
            elif self.__step_number == 2:
                self.pin1.off()
                self.pin2.off()
                self.pin3.on()
                self.pin4.off()
            elif self.__step_number == 3:
                self.pin1.off()
                self.pin2.off()
                self.pin3.off()
                self.pin4.on()

        else:
            if self.__step_number == 0:
                self.pin1.off()
                self.pin2.off()
                self.pin3.off()
                self.pin4.on()
            elif self.__step_number == 1:
                self.pin1.off()
                self.pin2.off()
                self.pin3.on()
                self.pin4.off()
            elif self.__step_number == 2:
                self.pin1.off()
                self.pin2.on()
                self.pin3.off()
                self.pin4.off()
            elif self.__step_number == 3:
                self.pin1.on()
                self.pin2.off()
                self.pin3.off()
                self.pin4.off()

        self.__step_number += 1
        if self.__step_number > 3:
            self.__step_number = 0

    def steps(self, count, dir=False, delay=2):
        from time import sleep_ms
        for _ in range(count):
            self.one_step(dir)
            sleep_ms(delay)
            
        self.reset()
            
    def reset(self):
        self.__step_number = 0
        self.pin1.off()
        self.pin2.off()
        self.pin3.off()
        self.pin4.off()
        
        
class CarMotors:
    
    def __init__(self, motor_A, motor_B, wheels_diameter_cm=6.7, wheels_distances_cm=13.5, delay_ms=2):
        import math
        self.motor_A = motor_A
        self.motor_B = motor_B
        self.wheels_circumference_cm = math.pi*wheels_diameter_cm
        self.steps_per_revolution = 2048
        self.wheels_distances_cm = wheels_distances_cm
        self.delay_ms = delay_ms

        
    def steps(self, count, dir=False, delay_ms=None):
        from time import sleep_ms

        for i in range(count):
            self.motor_A.one_step(dir)
            self.motor_B.one_step(dir)
            sleep_ms(self.delay_ms if delay_ms is None else delay_ms)
        self.motor_A.reset()
        self.motor_B.reset()
    
    
    def forward_cm(self, distance_cm):
        from time import sleep_ms
        steps = int(distance_cm * self.steps_per_revolution / self.wheels_circumference_cm)

        for i in range(steps):
            self.motor_A.one_step(False)
            self.motor_B.one_step(False)
            sleep_ms(self.delay_ms)
        self.motor_A.reset()
        self.motor_B.reset()
        
    def backward_cm(self, distance_cm):
        from time import sleep_ms
        steps = int(distance_cm * self.steps_per_revolution / self.wheels_circumference_cm)

        for i in range(steps):
            self.motor_A.one_step(True)
            self.motor_B.one_step(True)
            sleep_ms(self.delay_ms)
        self.motor_A.reset()
        self.motor_B.reset()
                
    def left(self, degrees, delay_ms=None):
        from time import sleep_ms
        from math import pi
        distance_cm = (self.wheels_distances_cm * pi) * degrees / 360
        steps = int(distance_cm * self.steps_per_revolution / self.wheels_circumference_cm)        
        
        
        for i in range(steps):
            self.motor_A.one_step(True)
            self.motor_B.one_step(False)
            sleep_ms(self.delay_ms if delay_ms is None else delay_ms)
        self.motor_A.reset()
        self.motor_B.reset()
        
    def right(self, degrees):
        from time import sleep_ms
        distance_cm = (self.wheels_distances_cm * degrees) / 2
        steps = int(distance_cm * self.steps_per_revolution / self.wheels_circumference_cm)        
        
        
        for i in range(steps):
            self.motor_A.one_step(False)
            self.motor_B.one_step(True)
            sleep_ms(self.delay_ms)
        self.motor_A.reset()
        self.motor_B.reset()
    
    
    


# import _thread
# 
# 
# 
# def run_mot_A(steps):
#     pins_motor_A = (23, 22, 21, 19)
#     st1 = Stepper_28BYJ_48(*pins_motor_A)
#     st1.steps(steps)
#     
# def run_mot_B(steps):
#     pins_motor_B = (16, 17, 5, 18)
#     st2 = Stepper_28BYJ_48(*pins_motor_B)
#     st2.steps(steps)
#     
# _thread.start_new_thread(run_mot_A,(2048,))
# _thread.start_new_thread(run_mot_B,(2048,))
