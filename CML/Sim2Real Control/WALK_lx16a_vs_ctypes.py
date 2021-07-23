import numpy as np
import time
import sys
from ServoMotor import *
from fns import *
import pandas as pd
import math as m

# Initialize motor control library & USB Port
filename = "/dev/ttyUSB0"
motor = ServoMotor(filename)
IO = motor.IO_Init()
if IO < 0:
	print('IO exit')
	sys.exit()


version= "0.2.0"
# Read v values from those saved from simulation
df = pd.read_csv('V/Hardcoded_{}.csv'.format(version))
v = np.array(df['Best Values'])

# Call corresponding function to convert sim2real/real2sim
def convFns(pos, convType):
	conv =	[left_armpit, left_elbow, left_shoulder, right_armpit, right_elbow, right_shoulder, 
			left_armpit, left_elbow, left_shoulder, right_armpit, right_elbow, right_shoulder]
	targ = np.zeros(12)
	for i in range(len(pos)):
		if i==0:
			targ[i] = conv[i](pos[i], convType, "front")
		elif i==6:
			targ[i] = conv[i](pos[i], convType, "back")
		else:
			targ[i] = conv[i](pos[i], convType)
	return targ


# Return position to take
def get_action(state, i):

	nextPos = [	0, (v[6] + v[7]*m.sin(i*v[36] + v[8])), (v[3] + v[4]*m.sin(i*v[36] + v[5])),
				0, (v[15] + v[16]*m.sin(i*v[36] + v[17])), (v[12] + v[13]*m.sin(i*v[36] + v[14])),
				0, (v[24] + v[25]*m.sin(i*v[36] + v[26])), (v[21] + v[22]*m.sin(i*v[36] + v[23])),
				0, (v[33] + v[34]*m.sin(i*v[36] + v[35])), (v[30] + v[31]*m.sin(i*v[36] + v[32]))]

	return convFns(nextPos, 'sim2real')

# MOVE MOTOR TO GIVEN POSITION
def walk(pos):
	h = 0
	for j in range(1,5):
		u = 10*j
		r = range(u, u+3)
		for i in r:
			motor.move(i, int(pos[h]), 0)
			h+=1
		#time.sleep(0.015)

# Read motor positions
def get_state():
	state = []
	for j in range(1,5):
		u = 10*j
		r = range(u, u+3)
		for i in r:
			state.append(motor.readPosition(i))
	return state

# Initialize motors as servos and set offset
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

# RESET position and stand down & up before walking
pos = [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
h = 0
for j in range(1,5):
	u = 10*j
	r = range(u, u+3)
	for i in r:
		motor.move(i, int(pos[h]), 1000)
		h+=1
time.sleep(5)
pos = [500, 750, 583, 500, 250, 417, 500, 750, 583, 500, 250, 417]
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
time.sleep(3)

# WALK
while j < 10000:
	# Get current position of motors
	# state = get_state()
	# Get target position
	pos = get_action(state, j)
	# Move robot to target position
	walk(pos)

	j += 1
	
