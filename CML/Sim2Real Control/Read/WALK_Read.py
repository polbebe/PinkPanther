import numpy as np
import time
import sys
from ServoMotor import *
from fns import *

# Initialize motor control library & USB Port
filename = "/dev/ttyUSB0"
motor = ServoMotor(filename)
IO = motor.IO_Init()
if IO < 0:
	print('IO exit')
	sys.exit()

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
'''
# Return target position
def act_shoulders&armpits(t, a, b, c, d, e):
	# Calculate desired position
	desired_p = np.zeros(12)
	# Positive
	pos_v_shoulder = a * np.sin(t * e) + b
	pos_v_elbow = c * np.sin(t * e) + d
	pos_shoulder = [2, 11]
	pos_elbow = [1, 10]
	# Negative
	neg_v_shoulder = -a * np.sin(t * e) + b
	neg_v_elbow = -c * np.sin(t * e) + d
	neg_shoulder = [5, 8]
	neg_elbow = [4, 7]
	# Zero
	zero = [0, 3, 6, 9]
	# Assign	
	desired_p[pos_shoulder] = pos_v_shoulder
	desired_p[pos_elbow] = pos_v_elbow
	desired_p[neg_shoulder] = neg_v_shoulder
	desired_p[neg_elbow] = neg_v_elbow
	desired_p[zero] = 0

	# Return desired new position
	return convFns(desired_p, "sim2real")
'''

# Front and back legs diff
# Return target position
def act(t, a, b, c, d, e):
	# Calculate desired position
	desired_p = np.zeros(12)

	pos_front_v = a * np.sin(t * e) + b
	neg_front_v = -a * np.sin(t * e) + b
	pos_back_v = c * np.sin(t * e) + d
	neg_back_v = -c * np.sin(t * e) + d

	front_pos = [1, 2]
	front_neg = [4, 5]
	back_pos = [10, 11]
	back_neg = [7, 8]

	zero = [0, 3, 6, 9]

	# Assign	
	desired_p[front_pos] = pos_front_v
	desired_p[front_neg] = neg_front_v
	desired_p[back_pos] = pos_back_v
	desired_p[back_neg] = neg_back_v
	desired_p[zero] = 0

	# Return desired new position
	return convFns(desired_p, "sim2real")


# Return position to take
def get_action(steps):
	#params = np.array([0.15, -0.3, 0.2, 0.3, 0.2]) # From Hardcoded_0.2.0
	params = np.array([0.15, 0.0, 0.2, 0.15, 0.2]) # From Hardcoded_0.2.0
	return act(steps, *params)

# MOVE MOTOR TO GIVEN POSITION
def walk(pos):
	h = 0
	real_pos = []
	for j in range(1,5):
		u = 10*j
		r = range(u, u+3)
		for i in r:
			real_pos.append(motor.readPosition(i))
			motor.move(i, int(pos[h]), 0)
			h+=1
		time.sleep(0.005)
	return real_pos

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
		motor.move(i, int(pos[h]), 1500)
		h+=1
time.sleep(3)
#pos = [500, 750, 583, 500, 250, 417, 500, 750, 583, 500, 250, 417]
pos = get_action(0)
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

# WALK
while j < 300:
	# Get target position
	pos = get_action(j)
	# Move robot to target position
	real_pos = walk(pos)

	j += 1

# RESET position and stand down & up before walking
pos = [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
h = 0
for j in range(1,5):
	u = 10*j
	r = range(u, u+3)
	for i in r:
		motor.move(i, int(pos[h]), 1500)
		h+=1
