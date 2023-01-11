import RPi.GPIO as gpio
import numpy as np
import signal


NUM_STEPPERS = 8
MAX_STEPS = 20

class pi74HC595_stepper:
    def __init__(
        self, DS: int = 36, ST: int = 32, SH: int = 40, daisy_chain: int = 1,
    ):

        if not (isinstance(DS, int) or isinstance(ST, int) or isinstance(SH, int)):
            raise ValueError("Pins must be int")
        elif DS < 1 or DS > 40 or ST < 1 or ST > 40 or SH < 1 or SH > 40:
            raise ValueError("Pins (DS, ST, SH) must be within pin range")

        if not isinstance(daisy_chain, int):
            raise ValueError("daisy_chain must be int")
        elif daisy_chain < 1:
            raise ValueError("daisy_chain must be positive")

        signal.signal(signal.SIGALRM, self._latch_output_timer_handler)

        self.data = DS  # DS
        self.parallel = ST  # ST_CP
        self.serial = SH  # SH_CP
        self.daisy_chain = daisy_chain  # Number of 74HC595s
        self.current = [0, 0, 0, 0, 0, 0, 0, 0] * self.daisy_chain
        self.control_sequence = np.zeros((2*NUM_STEPPERS,MAX_STEPS),dtype=int)
        self._setup_board()
        self.clear()

    def _setup_board(self):
        gpio.setmode(gpio.BOARD)
        gpio.setwarnings(True)
        gpio.setup(self.data, gpio.OUT)
        gpio.output(self.data, gpio.LOW)
        gpio.setup(self.parallel, gpio.OUT)
        gpio.output(self.parallel, gpio.LOW)
        gpio.setup(self.serial, gpio.OUT)
        gpio.output(self.serial, gpio.LOW)

    def _output(self):  # ST_CP
        gpio.output(self.parallel, gpio.HIGH)
        gpio.output(self.parallel, gpio.LOW)

    def _tick(self):  # SH_CP
        gpio.output(self.serial, gpio.HIGH)
        gpio.output(self.serial, gpio.LOW)
        
    # This should happen with correct timing as it will affect the stepper motors
    def _latch_output_timer_handler(self, signum, frame): 
        
        bitstream = self.control_sequence.T[:1,]
        #self.printControlSequence()
        #print(bitstream)
        
        for bit in bitstream[0]:
            if (bit):
                gpio.output(self.data, gpio.HIGH)
            else:
                gpio.output(self.data, gpio.LOW)
            self._tick()
        self._output()
        #print()
        
    
        self.control_sequence = np.roll(self.control_sequence, -1, axis=1) 
        self.control_sequence[:,-1] = 0

    def _set_values(self, values):
        for bit in values:
            self.current.append(bit)
            del self.current[0]
            if bit == 1:
                gpio.output(self.data, gpio.HIGH)
            elif bit == 0:
                gpio.output(self.data, gpio.LOW)
            self._tick()
        self._output()
        

    
    def enable_timer(self, latch_every):
        signal.setitimer(signal.ITIMER_REAL, 0.0000001, latch_every)

    def disable_timer(self):
        signal.setitimer(signal.ITIMER_REAL, 0) # Disable the alarm
        
    def stepMotor(self, motor, steps, direction):
        if (np.sum(self.control_sequence[2*motor])):
            print("Motor", motor ,"is busy, please try again later")
            return 1
        self.control_sequence[2*motor,1:2*steps:2] = 1
        self.control_sequence[2*motor+1,:2*steps:1] = [direction]

    def printControlSequence(self):
        print(self.control_sequence)

    def set_ds(self, pin: int):
        """
        Sets the pin for the serial data input (DS)

        Returns: None

        """
        if not isinstance(pin, int):
            raise ValueError("Argument must be int")
        elif pin < 1 or pin > 40:
            raise ValueError("Argument must be within pin range")

        self.data = DS

    def set_sh(self, pin: int):
        """
        Sets the pin for the shift register clock pin (SH_CP)

        Returns: None

        """
        if not isinstance(pin, int):
            raise ValueError("Argument must be int")
        elif pin < 1 or pin > 40:
            raise ValueError("Argument must be within pin range")

        self.parallel = DS

    def set_st(self, pin: int):
        """
        Sets the pin for the storage register clock pin (ST_CP)

        Returns: None

        """
        if not isinstance(pin, int):
            raise ValueError("Argument must be int")
        elif pin < 1 or pin > 40:
            raise ValueError("Argument must be within pin range")

        self.serial = ST

    def set_daisy_chain(self, num: int):
        """
        Sets the the number of 74HC595s used in Daisy Chain

        Returns: None

        """
        if not isinstance(num, int):
            raise ValueError("Argument must be int")
        elif num < 1:
            raise ValueError("Argument must be positive")

        self.daisy_chain = num

    def get_values(self) -> list:
        """
        Returns the values of the current 74HC595(s)

        args: None

        Returns: List of current state
            [0, 1, 0,...]

        """
        return self.current
    
    def clear(self):
        """
        Sets the 74HC595 back to all off

        Returns: None

        """
        self._set_values([0, 0, 0, 0, 0, 0, 0, 0] * self.daisy_chain)

    def cleanup(self):
        gpio.cleanup()