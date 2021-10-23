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
def get_action(steps):
	# Test with w=0.21 and armpit joints don't move
	params = np.array([-0.1452217682136046, 0.5370238181034812, 5.453212634461867, 4.161790918008703, -1.6280157636978125, -2.764998743492415, -0.5724522688587933, 0.7226947508679249, -0.6998402793502201, 0.5072764835093281, 0.03661892351135113, 0.4627483024891589, 0.21236724167077375, 0.1380141387384276, -0.27684548026527517, -0.3643201944698517])
	return act(steps, *params)

def act(t, p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15):
	# Calculate desired position
	desired_p = np.zeros(12)
	#LF
	desired_p[0] = 0 #p0 * np.sin(t/8*2*np.pi + p2) + p10
	desired_p[1] = p6 * np.sin(t/8*2*np.pi + p2) + p12
	desired_p[2] = p8 * np.sin(t/8*2*np.pi + p2) + p14
	#RF
	desired_p[3] = 0 #p1 * np.sin(t/8*2*np.pi + p3) + p11
	desired_p[4] = p7 * np.sin(t/8*2*np.pi + p3) + p13
	desired_p[5] = p9 * np.sin(t/8*2*np.pi + p3) + p15
	#LB
	desired_p[6] = 0 #p1 * np.sin(t/8*2*np.pi + p4) + p11
	desired_p[7] = p7 * np.sin(t/8*2*np.pi + p4) + p13
	desired_p[8] = p9 * np.sin(t/8*2*np.pi + p4) + p15
	#RB
	desired_p[9] = 0 #p0 * np.sin(t/8*2*np.pi + p5) + p10
	desired_p[10] = p6 * np.sin(t/8*2*np.pi + p5) + p12
	desired_p[11] = p8 * np.sin(t/8*2*np.pi + p5) + p14
	# Return desired new position
	return convFns(desired_p, "sim2real")

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

# WALK
while j < 300:
	# Get target position
	pos = get_action(j)
	print(pos)
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
