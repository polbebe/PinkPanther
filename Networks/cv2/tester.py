#!/usr/bin/env python3
import numpy as np
from ServoMotor import *
import math as m
import time


filename = "/dev/ttyUSB0"
motor = ServoMotor(filename)

# Initialize USB Port
IO = motor.IO_Init()
if IO < 0:
    print('IO exit')
    sys.exit()

# Set servo mode to all servos
# LEFT front
motor.setServoMode(10)
motor.setServoMode(12)
motor.setServoMode(11)
# LEFT back
motor.setServoMode(30)
motor.setServoMode(32)
motor.setServoMode(31)
# RIGHT front
motor.setServoMode(20)
motor.setServoMode(22)
motor.setServoMode(21)
# RIGTH back
motor.setServoMode(40)
motor.setServoMode(42)
motor.setServoMode(41)

pos = [500.00000000000006, 583.3333333333334, 750.0, 500.00000000000006, 583.3333333333334, 750.0, 500.00000000000006, 416.6666666666667, 250.00000000000003, 500.00000000000006, 416.6666666666667, 250.00000000000003]


# Move all servos to their corresponding position
# LEFT front
motor.move(10, int(pos[0]), 0)
motor.move(12, int(pos[1]), 0)
motor.move(11, int(pos[2]), 0)
# LEFT back
motor.move(30, int(pos[6]), 0)
motor.move(32, int(pos[7]), 0)
motor.move(31, int(pos[8]), 0)
# RIGHT front
motor.move(20, int(pos[3]), 0)
motor.move(22, int(pos[4]), 0)
motor.move(21, int(pos[5]), 0)
# RIGTH back
motor.move(40, int(pos[9]), 0)
motor.move(42, int(pos[10]), 0)
motor.move(41, int(pos[11]), 0)



