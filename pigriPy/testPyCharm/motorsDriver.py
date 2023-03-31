class MotorsDriver:

    def __init__(self, inPin1, inPin2, inPin3, inPin4, enPinA, enPinB) -> None:
        self.inPin1 = inPin1
        self.inPin2 = inPin2
        self.enPinA = enPinA
        self.inPin3 = inPin3
        self.inPin4 = inPin4
        self.enPinB = enPinB


    def forward(self) -> None:
        self.inPin1.value(1)
        self.inPin2.value(0)
        self.inPin3.value(1)
        self.inPin4.value(0)
        self.enPinA.value(1)
        self.enPinB.value(1)

    def backward(self) -> None:
        self.inPin1.value(0)
        self.inPin2.value(1)
        self.enPinA.value(1)
        self.inPin3.value(0)
        self.inPin4.value(1)
        self.enPinB.value(1)

    def stop(self) -> None:
        self.inPin1.value(0)
        self.inPin2.value(0)
        self.enPinA.value(0)
        self.inPin3.value(0)
        self.inPin4.value(0)
        self.enPinB.value(0)
