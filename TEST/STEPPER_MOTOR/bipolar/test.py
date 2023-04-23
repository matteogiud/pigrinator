from machine import Pin
import time

# Configurazione dei pin del driver L298N
in1A = Pin(12, Pin.OUT)
in2A = Pin(14, Pin.OUT)
in4A = Pin(27, Pin.OUT)
in4A = Pin(26, Pin.OUT)


# Definizione dei passi per la rotazione del motore
step_sequence = [[1, 0, 0, 1], [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1]]

# Definizione della velocità di rotazione
delay = 0.001

def set_step(step):
    # Impostazione del passo corrente
    in1A.value(step[0])
    in2A.value(step[1])
    in4A.value(step[2])
    in4A.value(step[3])   


def rotate(steps, direction):
    # Calcolo del numero di cicli necessari per compiere il numero di passi richiesto
    cycles = int(steps / 8)
    # Ciclo di rotazione
    for i in range(cycles):
        # Ciclo di passi per ciascun ciclo
        for j in range(8):
            if direction == "cw":
                set_step(step_sequence[j])
            else:
                set_step(step_sequence[7-j])
            time.sleep(delay)
    
# Esempio di rotazione di 512 passi in senso orario (cw)
rotate(4096, "cw") # un giro completo