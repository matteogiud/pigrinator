from lib.Stepper import *
import _thread

step_motor_A = (23, 22, 21, 19)
step_motor_B = (16, 17, 5, 18)

s1 = Stepper(HALF_STEP, *step_motor_A, delay=1)
s2 = Stepper(HALF_STEP, *step_motor_B, delay=1)
t1 = _thread.start_new_thread(s1.step, (FULL_ROTATION))
t2 = _thread.start_new_thread(s2.step, (FULL_ROTATION))
# s1.step(FULL_ROTATION)
# s2.step(FULL_ROTATION)

# c1 = Command(s1, FULL_ROTATION)         # Go all the way round
# c2 = Command(s2, FULL_ROTATION/2, 1)   # Go halfway round, backwards
# # 
# runner = Driver()
# runner.run([c1,c2])
