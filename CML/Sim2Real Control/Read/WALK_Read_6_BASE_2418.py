import numpy as np
import time
import sys
from ServoMotor import *
from fns import *

# MAX delta_pos allowed in any given movement
delta_p = 50.0

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

# Front and back legs diff
# Return target position
def act(t, a, b, c, d, e, f):
	# Calculate desired position
	f_pos = a * np.sin(t * e) + b
	f_neg = -a * np.sin(t * e) + b
	b_pos = c * np.sin(t * e + f) + d
	b_neg = -c * np.sin(t * e + f) + d

	# Assign	
	desired_p = [0, f_pos, f_pos, 0, f_neg, f_neg, 0, b_pos, b_pos, 0, b_neg, b_neg]

	# Return desired new position
	return convFns(desired_p, "sim2real")

# Return position to take
def get_action(steps):
	#params = np.array(np.load('params/HillClimber/23_01_2022/best_overall.npy'))
	params = np.array([-0.16476964, 0.02548534, 0.16893791, 0.09441782, 9.44620473, -6.1950588]) # 27_01_2022 params trained on envs auto-tuned to be close to the env I manually tuned
	#params[4]-=4
	#params = np.array([0.24495851730947005, 0.18187873796178136, 0.2020333429029758, -0.3852743697870839, -0.2094960812992037]) # Trained sin_gait 7, Oct 11 19:01
	#params = np.array([0.2980418533307479, 0.01878523690431866, 0.022546654023646796, -0.2685025304630598, -0.2080157428428239]) # Trained sin_gait 5, Oct 12 13:21
	#params = np.array([0.15, 0.0, 0.2, 0.15, 0.2]) # Smooth Criminal
	#params = np.array([0.15, 0.0, 0.19, 0.2, 0.23, 2.05])
	return act(steps, *params)

# Read motor positions
def read():
	h = 0
	real_pos = []
	for j in range(1,5):
		u = 10*j
		r = range(u, u+3)
		for i in r:
			real_pos.append(motor.readPosition(i))
			h+=1
		time.sleep(0.005)
	return real_pos

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
offsets = [30, 0, 64, 0, 70, 50, 26, 100, 55, 80, 90, 35]
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
pos = [500, 750, 583, 500, 250, 417, 500, 750, 583, 500, 250, 417]
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


# WALK
j = 1
real_pos = read()
while j < 100:
	# Keep track of previous real robot pos
	prev_pos = real_pos
	# Get target position
	action = get_action(j)
	# Clip it for max delta_pos
	delta = np.clip([action[i]-prev_pos[i] for i in range(len(action))], -delta_p, delta_p)
	pos = [prev_pos[i]+delta[i] for i in range(len(delta))]
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