from pi74HC595_stepper import pi74HC595_stepper
import time

stepper = pi74HC595_stepper()
stepper.enable_timer(latch_every = 0.1)
time.sleep(1)
stepper.disable_timer()