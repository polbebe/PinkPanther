#!/usr/bin/env python3
from ServoMotor import *
import time


filename = "/dev/ttyUSB0"
motor = ServoMotor(filename)

# Initialize USB Port
IO = motor.IO_Init()
if IO < 0:
    print('IO exit')
    sys.exit()

# Set servo mode to all servos
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

pos = [510, 583, 750, 500, 417, 250, 500, 583, 750, 500, 417, 250]
motor.move(10, int(pos[0]), 1000)
motor.move(12, int(pos[1]), 1000)
motor.move(11, int(pos[2]), 1000)
motor.move(30, int(pos[6]), 700)
motor.move(32, int(pos[7]), 700)
motor.move(31, int(pos[8]), 700)
motor.move(20, int(pos[3]), 1000)
motor.move(22, int(pos[4]), 1000)
motor.move(21, int(pos[5]), 1000)
motor.move(40, int(pos[9]), 700)
motor.move(42, int(pos[10]), 700)
motor.move(41, int(pos[11]), 700)
