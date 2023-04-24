class MotorsStatus:
    FORWARD = 1
    BACKWARD = 2
    RIGHT = 3
    LEFT = 4
    STOP = 5
    
class MotorsDriver:   

    def __init__(self, inPin1, inPin2, inPin3, inPin4, enPinA, enPinB, __pwmVelocity=1000, diameterWheelA=67, diameterWheelB=67) -> None:
        self.inPin1 = inPin1
        self.inPin2 = inPin2
        self.enPinA = enPinA
        self.inPin3 = inPin3
        self.inPin4 = inPin4
        self.enPinB = enPinB
        self.diameterWheelA = diameterWheelA
        self.diameterWheelB = diameterWheelB
        self.__pwmVelocity = __pwmVelocity
        self.enPinB.freq(1000)
        self.enPinA.freq(1000)
        self.__motorStatus = None        


    def forward(self) -> None:
        self.inPin1.value(1)
        self.inPin2.value(0)
        self.inPin3.value(1)
        self.inPin4.value(0)
        self.enPinA.duty(self.__pwmVelocity)
        self.enPinB.duty(self.__pwmVelocity)
        self.__motorStatus = MotorsStatus.FORWARD
        

    def backward(self) -> None:
        self.inPin1.value(0)
        self.inPin2.value(1)
        self.enPinA.duty(self.__pwmVelocity)
        self.inPin3.value(0)
        self.inPin4.value(1)
        self.enPinB.duty(self.__pwmVelocity)
        self.__motorStatus = MotorsStatus.BACKWARD


    def stop(self) -> None:
        self.inPin1.value(0)
        self.inPin2.value(0)
        self.enPinA.duty(0)
        self.inPin3.value(0)
        self.inPin4.value(0)
        self.enPinB.duty(0)
        self.__motorStatus = MotorsStatus.STOP
        
        
    def left(self) -> None:
        self.enPinA.duty(self.__pwmVelocity)
        self.enPinB.duty(self.__pwmVelocity)
        self.inPin1.value(0)
        self.inPin2.value(1)
        self.inPin3.value(1)
        self.inPin4.value(0)
        self.__motorStatus = MotorsStatus.LEFT

        
    def right(self) -> None:
        self.enPinA.duty(self.__pwmVelocity)
        self.enPinB.duty(self.__pwmVelocity)
        self.inPin1.value(1)
        self.inPin2.value(0)
        self.inPin3.value(0)
        self.inPin4.value(1)
        self.__motorStatus = MotorsStatus.RIGHT

        
    def set__pwmVelocity(self, value) -> None:
        self.__pwmVelocity = value
        if self.__motorStatus == MotorsStatus.FORWARD:
            self.forward()
        elif self.__motorStatus == MotorsStatus.BACKWARD:
            self.backward()
        elif self.__motorStatus == MotorsStatus.STOP:
            self.stop()

