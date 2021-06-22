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

pos = [510, 750, 583, 500, 250, 417, 500, 750, 583, 500, 250, 417]
h = 0
for j in range(1,5):
	u = 10*j
	r = range(u, u+3)
	for i in r:
		if h>5:
			motor.move(i, int(pos[h]), 700)
		else:
			motor.move(i, int(pos[h]), 1000)
		h+=1

h = 0
for j in range(1,5):
	u = 10*j
	r = range(u, u+3)
	for i in r:
		print("Motor {}: {} Pos Error".format(i, abs(pos[h] - motor.readPosition(i))))
		h+=1


pos = [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
h = 0
for j in range(1,5):
	u = 10*j
	r = range(u, u+3)
	for i in r:
		motor.move(i, int(pos[h]), 1000)
		h+=1

h = 0
for j in range(1,5):
	u = 10*j
	r = range(u, u+3)
	for i in r:
		print("Motor {}: {} Pos Error".format(i, abs(pos[h] - motor.readPosition(i))))
		h+=1
