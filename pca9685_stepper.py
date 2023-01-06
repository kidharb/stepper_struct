# SuperFastPython.com
# example of using a thread timer object
from threading import Timer
from board import SCL, SDA
import busio

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685


PCA9685_FREQUENCY=1800
NUM_MOTORS=8

# target task function
def stopMotor(motor):
    # report the custom message
    pca.channels[motor*2].duty_cycle = 0x0
    print("stopMotor: Stopping motor",motor)
        
def calcDuration(freq, steps):
    return (1/freq * steps)

def stepMotor(motor, freq, steps, direction):
   print("stepMotor: New request for Motor #",motor," Steps =",steps," Direction =",direction)

   duration = calcDuration(freq,steps)
   print("On Duration is ",duration,"s")
   pca.channels[motor+1].duty_cycle = direction
   timer = Timer(duration, stopMotor, args=(motor,))

   timer.start()
   # Turn on the PWM output for this motor
   pca.channels[motor*2].duty_cycle = 0x7FFF

if __name__ == "__main__":
    # Create the I2C bus interface.
    i2c_bus = busio.I2C(SCL, SDA)
    # Create a simple PCA9685 class instance.
    pca = PCA9685(i2c_bus)

    # Set the PWM frequency to 40hz.
    pca.frequency = PCA9685_FREQUENCY
    for i in range(0,NUM_MOTORS*2,2):
        print("Init: Switching of PWM on PCA9685 output",i)
        pca.channels[i].duty_cycle = 0x0
        
    stepMotor(0,PCA9685_FREQUENCY,20,0xFFFF)
