# SuperFastPython.com
# example of using a thread timer object
from threading import Timer
from board import SCL, SDA
import busio

import signal
import time

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685


PCA9685_FREQUENCY=1800
NUM_MOTORS=8

# target task function
def stopMotor0(signum, frame):
    # report the custom message
    pca.channels[0*2].duty_cycle = 0x0
    print("stopMotor: Stopping motor",0)

        
def calcDuration(freq, steps):
    return (1/freq * steps)

def stepMotor(motor, freq, steps, direction):
   print("stepMotor: New request for Motor #",motor," Steps =",steps," Direction =",direction)

   duration = calcDuration(freq,steps)
   print("On Duration is",duration,"s")
   pca.channels[motor+1].duty_cycle = direction
   #timer = Timer(duration, stopMotor, args=(motor,))

   #timer.start()
   signal.signal(signal.SIGALRM, stopMotor0)

   # Turn on the PWM output for this motor
   pca.channels[motor*2].duty_cycle = 0x7FFF
   signal.setitimer(signal.ITIMER_REAL, 0.000001, 0.1)


if __name__ == "__main__":
    # Create the I2C bus interface.
    i2c_bus = busio.I2C(SCL, SDA)
    # Create a simple PCA9685 class instance.
    pca = PCA9685(i2c_bus)

    # Set the PWM frequency to 40hz.
    pca.frequency = PCA9685_FREQUENCY
    for i in range(0,NUM_MOTORS*2,2):
        #print("Init: Switching off PWM on PCA9685 output",i)
        pca.channels[i].duty_cycle = 0x0
        
    stepMotor(0,PCA9685_FREQUENCY,1,0xFFFF)
    time.sleep(1)
    signal.setitimer(signal.ITIMER_REAL, 0) # Disable the alarm


