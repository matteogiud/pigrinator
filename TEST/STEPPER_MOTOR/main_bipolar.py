import machine
import utime


in1 = machine.Pin(12, machine.Pin.OUT)
in2 = machine.Pin(14, machine.Pin.OUT)
in3 = machine.Pin(27, machine.Pin.OUT)
in4 = machine.Pin(26, machine.Pin.OUT)


# Sequenza di passi per far girare il motore
HALFSTEP = [[1, 0, 1, 0],
           [0, 1, 1, 0],
           [0, 1, 0, 1],
           [1, 0, 0, 1]]


# Configurazione del delay per stabilire la velocità del motore
DELAY = 0.001

count = 0


while True:
    for i in range(4):
        in1.value(HALFSTEP[i][0])
        in2.value(HALFSTEP[i][1])
        in3.value(HALFSTEP[i][2])
        in4.value(HALFSTEP[i][3])
        utime.sleep(DELAY)

