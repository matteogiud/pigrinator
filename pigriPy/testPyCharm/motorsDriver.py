class MotorsDriver:

    def __init__(self, inPin1, inPin2, inPin3, inPin4, enPinA, enPinB, diameterWheelA = 67, diameterWheelB = 67) -> None:
        self.inPin1 = inPin1
        self.inPin2 = inPin2
        self.enPinA = enPinA
        self.inPin3 = inPin3
        self.inPin4 = inPin4
        self.enPinB = enPinB
        self.diameterWheelA = diameterWheelA
        self.diameterWheelB = diameterWheelB
        self.pwmVelocity = 255


    def forward(self) -> None:
        self.inPin1.value(1)
        self.inPin2.value(0)
        self.inPin3.value(1)
        self.inPin4.value(0)
        self.enPinA.value(self.pwmVelocity)
        self.enPinB.value(self.pwmVelocity)

    def backward(self) -> None:
        self.inPin1.value(0)
        self.inPin2.value(1)
        self.enPinA.value(self.pwmVelocity)
        self.inPin3.value(0)
        self.inPin4.value(1)
        self.enPinB.value(self.pwmVelocity)

    def stop(self) -> None:
        self.inPin1.value(0)
        self.inPin2.value(0)
        self.enPinA.value(0)
        self.inPin3.value(0)
        self.inPin4.value(0)
        self.enPinB.value(0)
