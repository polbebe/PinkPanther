from ServoMotor import *

import numpy as np
import sys


# Initialize ServoMotor class
filename = "/dev/ttyUSB0"
motor = ServoMotor(filename)

# Initialize USB Port
IO = motor.IO_Init()
if IO < 0:
    print('IO exit')
    sys.exit()

motor.setServoMode(10)
motor.setServoMode(12)
motor.setServoMode(11)

motor.setServoMode(30)
motor.setServoMode(32)
motor.setServoMode(31)

motor.setServoMode(20)
motor.setServoMode(22)
motor.setServoMode(21)

motor.setServoMode(40)
motor.setServoMode(42)
motor.setServoMode(41)


for i in range(40,43,1):
    motor.setPositionLimits(i, 0, 1000)
    print('{}: {}'.format(i, motor.getPositionLimits(i)))

motor.move(10, 500, 300)
motor.move(12, 621, 300)
motor.move(11, 721, 300)

motor.move(30, 500, 300)
motor.move(32, 621, 300)
motor.move(31, 721, 300)

motor.move(20, 500, 300)
motor.move(22, 375, 300)
motor.move(21, 499, 300)

motor.move(40, 500, 300)
motor.move(42, 375, 300)
motor.move(41, 279, 300)
