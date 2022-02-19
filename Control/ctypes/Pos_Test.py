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

#offsets = [15, 0, 50, 0, 70, 60, 26, 0, 50, 80, 90, 62]
offsets = [30, 0, 39, 0, 70, 77, 26, 1, 30, 80, 90, 62]
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
'''
for j in range(1,5):
	u = 10*j
	r = range(u, u+3)
	for i in r:
		print("Motor {}: {} mV ?".format(i, motor.getVoltage(i)))


pos = [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
h = 0
for j in range(1,5):
	u = 10*j
	r = range(u, u+3)
	for i in r:
		motor.move(i, int(pos[h]), 1500)
		h+=1
time.sleep(3)
'''
pos = [500, 750, 608, 500, 250, 390, 500, 750, 608, 500, 250, 390]
#pos = get_action(0)
h = 0
for j in range(1,5):
	u = 10*j
	r = range(u, u+3)
	for i in r:
		if h>5:
			motor.move(i, int(pos[h]), 1000)
		else:
			motor.move(i, int(pos[h]), 1500)
		h+=1
time.sleep(3)
'''
motor.move(11, 1000, 1500)
motor.move(21, 000, 1500)
motor.move(31, 1000, 1500)
motor.move(41, 000, 1500)
time.sleep(3)
'''