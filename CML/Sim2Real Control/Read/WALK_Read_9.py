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

# Define next action given parameters
def act(t, p0, p1, p2, p3, p4, p5, p6, p7, p8):
	# front shoulder (+p1)
	f_s = p0 * np.sin(t * p8)
	# front elbow (+p3)
	f_e = p2 * np.sin(t * p8)
	# back shoulder (+p5)
	b_s = p4 * np.sin(t * p8)
	# back elbow (+p7)
	b_e = p6 * np.sin(t * p8)

	desired_p = np.array([0, f_s+p1, f_e+p3, 0, -f_s+p1, -f_e+p3, 0, -b_s+p5, -b_e+p7, 0, b_s+p5, b_e+p7])

	# return desired new position
	return convFns(desired_p, "sim2real")


# Return position to take
def get_action(steps):
	params = np.array(np.load('params/best_overall_95.81.npy'))
	#params = np.array([0.15, 0.0, 0.15, 0.0, 0.2, 0.15, 0.2, 0.15, 0.21]) # Smooth Criminal, Jul 31 19:00

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

# Determine need to smoothen transition to first position
pos_prev = [500, 750, 583, 500, 250, 417, 500, 750, 583, 500, 250, 417]
pos = get_action(0)
delta_pos = abs(pos-pos_prev)
steps = int(max(delta_pos)/15)
m = []
for i in range(len(pos)):
	m.append(np.linspace(pos_prev[i], pos[i], steps))
m_t = np.array(m).T.tolist()
for i in range(len(m_t)):
	for j in range(len(m_t[0])):
		m_t[i][j] = int(round(m_t[i][j]))

# If smoothing is needed, perform actions
for i in m_t:
	real_pos = walk(i)

# WALK
j = 1
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
