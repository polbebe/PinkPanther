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


offsets = [30, 0, 64, 0, 70, 50, 26, 0, 55, 80, 90, 35]

h = 0
# Set servo mode to all servos with their offset
for j in range(1,5):
	u = 10*j
	r = range(u, u+3)
	for i in r:
		motor.setServoMode(i)
		if offsets[h]!=0:
			motor.setPositionOffset(i,offsets[h])
		h+=1

pos = [500, 354, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
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
