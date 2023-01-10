import numpy as np

NUM_STEPPERS = 8
MAX_STEPS = 20

def clockOut():
    global control_sequence
    control_sequence = np.roll(control_sequence, -1, axis=1) 
    control_sequence[:,-1] = 0


def stepMotor(motor,steps,direction):
    global control_sequence

    if (np.sum(control_sequence[2*motor])):
        print("Motor", motor ,"is busy, please try again later")
        return 1

    control_sequence[2*motor,1:2*steps:2] = 1
    control_sequence[2*motor+1,:2*steps:1] = [direction]




signal, stepper = (1, 2*NUM_STEPPERS)
control_sequence = np.zeros((2*NUM_STEPPERS,MAX_STEPS))

stepMotor(5,5,1)
stepMotor(1,10,1)
stepMotor(7,8,1)
stepMotor(5,5,1)

print(control_sequence)

#for i in range(10):
#    clockOut()
print(control_sequence[:,1])
