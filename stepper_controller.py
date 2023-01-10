from pi74HC595_stepper import pi74HC595_stepper
import time

stepper = pi74HC595_stepper()

stepper.stepMotor(5,5,1)
stepper.stepMotor(1,10,1)
stepper.stepMotor(7,8,1)

stepper.enable_timer(latch_every = 0.1)


time.sleep(1)
stepper.disable_timer()