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

# Set servo mode to all servos
# LEFT front
#motor.setServoMode(10)
#motor.setServoMode(12)
motor.setServoMode(11)
# LEFT back
#motor.setServoMode(30)
#motor.setServoMode(32)
#motor.setServoMode(31)
# RIGHT front
#motor.setServoMode(20)
#motor.setServoMode(22)
#motor.setServoMode(21)
# RIGTH back
#motor.setServoMode(40)
#motor.setServoMode(42)
#motor.setServoMode(41)

low_lim, high_lim = motor.getPositionLimits(11)
        
        
# Move all servos to their corresponding position
# LEFT front
#motor.move(10, 130, 100)
#motor.move(12, pos[1], 100)
motor.move(11, low_lim, 100)
# LEFT back
#self.motor.move(30, pos[6], 100)
#motor.move(32, pos[7], 100)
#motor.move(31, pos[8], 100)
# RIGHT front
#self.motor.move(20, pos[3], 100)
#motor.move(22, pos[4], 100)
#motor.move(21, pos[5], 100)
# RIGTH back
#self.motor.move(40, pos[9], 100)
#motor.move(42, pos[10], 100)
#motor.move(41, pos[11], 100)
