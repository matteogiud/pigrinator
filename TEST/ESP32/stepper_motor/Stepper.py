import machine
import utime

class StepperMotor:
    def __init__(self, pin1, pin2, pin3, pin4):
        # Definiamo i pin per controllare il motore stepper
        self.coil_A_1_pin = machine.Pin(pin1, machine.Pin.OUT)
        self.coil_A_2_pin = machine.Pin(pin2, machine.Pin.OUT)
        self.coil_B_1_pin = machine.Pin(pin3, machine.Pin.OUT)
        self.coil_B_2_pin = machine.Pin(pin4, machine.Pin.OUT)

        # Definiamo la sequenza dei pin di controllo del motore stepper
        self.seq = [[1,0,0,1],
                    [1,0,0,0],
                    [1,1,0,0],
                    [0,1,0,0],
                    [0,1,1,0],
                    [0,0,1,0],
                    [0,0,1,1],
                    [0,0,0,1]]

    # Definiamo la funzione per far girare il motore
    def step(self, delay, steps):
        for i in range(steps):
            for halfstep in range(8):
                for pin in range(4):
                    if self.seq[halfstep][pin]!=0:
                        if pin==0:
                            self.coil_A_1_pin.on()
                        elif pin==1:
                            self.coil_A_2_pin.on()
                        elif pin==2:
                            self.coil_B_1_pin.on()
                        elif pin==3:
                            self.coil_B_2_pin.on()
                    else:
                        if pin==0:
                            self.coil_A_1_pin.off()
                        elif pin==1:
                            self.coil_A_2_pin.off()
                        elif pin==2:
                            self.coil_B_1_pin.off()
                        elif pin==3:
                            self.coil_B_2_pin.off()
                utime.sleep_us(delay)

    # Definiamo la funzione per far girare il motore in una direzione specifica
    def rotate(self, direction, speed, degrees):
        steps = int(degrees/0.0879) # calcoliamo il numero di steps necessari per ruotare di n gradi
        delay = int(1000000/speed) # calcoliamo il ritardo necessario per la velocità desiderata
        if direction == "CW":
            self.step(delay, steps)
        elif direction == "CCW":
            self.seq = list(reversed(self.seq)) # invertiamo la sequenza per far girare il motore in senso antiorario
            self.step(delay, steps)
            self.seq = list(reversed(self.seq)) # ripristiniamo la sequenza

    # Definiamo la funzione per far girare il motore in entrambe le direzioni
    def oscillate(self, speed, degrees):
        self.rotate("CW", speed, degrees)
        self.rotate("CCW", speed, degrees)

    # Definiamo la funzione per fermare il motore
    def stop(self):
        self.coil_A_1_pin.off()
        self.coil_A_2_pin.off()
        self.coil_B_1_pin.off()
        self.coil_B_2_pin.off()
        
        


class CarMotors:
    def __init__(self, motor_A, motor_B):
        # Inizializziamo i due motori stepper
        print(motor_A, motor_B)
        self.motor_A = motor_A
        self.motor_B = motor_B
    
    # Definiamo la funzione per far avanzare la macchinina
    def forward(self, speed, distance):
        print(self.motor_A)
        degrees = distance / 0.13 # calcoliamo il numero di gradi necessari per percorrere una certa distanza
        self.motor_A.rotate("CW", speed, degrees)
        self.motor_B.rotate("CCW", speed, degrees)

    # Definiamo la funzione per far retrocedere la macchinina
    def backward(self, speed, distance):
        degrees = distance / 0.13 # calcoliamo il numero di gradi necessari per percorrere una certa distanza
        self.motor_A.rotate("CCW", speed, degrees)
        self.motor_B.rotate("CW", speed, degrees)

    # Definiamo la funzione per girare a destra
    def turn_right(self, speed, degrees):
        self.motor_A.rotate("CW", speed, degrees)
        self.motor_B.rotate("CW", speed, degrees)

    # Definiamo la funzione per girare a sinistra
    def turn_left(self, speed, degrees):
        self.motor_A.rotate("CCW", speed, degrees)
        self.motor_B.rotate("CCW", speed, degrees)

    # Definiamo la funzione per fermare la macchinina
    def stop(self):
        self.motor_A.stop()
        self.motor_B.stop()

