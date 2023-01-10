import numpy as np

NUM_STEPPERS = 8
MAX_STEPS = 20

def clockOut():
    bitstream = column(control_sequence,1)
    print(bitstream)

def stepMotor(motor,steps,direction):
    global control_sequence

    control_sequence[2*motor,1:2*steps:2] = 1
    control_sequence[2*motor+1,:2*steps:1] = [direction]



signal, stepper = (1, 2*NUM_STEPPERS)
control_sequence = np.array([[0] * MAX_STEPS * signal]*stepper)

stepMotor(5,5,1)
stepMotor(1,10,1)
stepMotor(7,8,1)
clockOut()
#print(control_sequence)



#printControlSequence(control_sequence)