import numpy as np
import time
import sys
from ServoMotor import *

filename = "/dev/ttyUSB0"
motor = ServoMotor(filename)

# Initialize USB Port
IO = motor.IO_Init()
if IO < 0:
	print('IO exit')
	sys.exit()

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

if __name__ == '__main__':

	# SIM 2 REAL
	def servo_left_shoulder_sim2real(targ):
		if targ>=0:
			pos = (621 - (targ/1.2)*(621-290))
		else:
			pos = (621 + (abs(targ)/0.3)*(688-621))
		return int(round(pos))
	def servo_left_elbow_sim2real(targ):
		if targ>=0:
			pos = (721 + (targ/1.2)*(1000-721))
		else:
			pos = (721 - (abs(targ)/0.9)*(721-500))
		return int(round(pos))

	def servo_right_shoulder_sim2real(targ):
		if targ>=0:
			pos = (375 + (targ/1.2)*(700-375))
		else:
			pos = (375 - (abs(targ)/0.3)*(375-313))
		return int(round(pos))
	def servo_right_elbow_sim2real(targ):
		if targ>=0:
			pos = (279 - (targ/1.2)*(279-0))
		else:
			pos = (279 + (abs(targ)/0.9)*(500-279))
		return int(round(pos))

	# Call corresponding function to convert sim2real
	def transformMotors(pos):
		null = lambda x: (x-500)/500
		fns =	[null, servo_left_elbow_sim2real, servo_left_shoulder_sim2real, null, servo_right_elbow_sim2real, servo_right_shoulder_sim2real, 
				null, servo_left_elbow_sim2real, servo_left_shoulder_sim2real, null, servo_right_elbow_sim2real, servo_right_shoulder_sim2real]
		targ = np.zeros(12)
		for i in range(len(pos)):
			targ[i] = fns[i](pos[i])
		return targ

	# Return real positions for a given simulated position
	def sim2real(pos):
		p = transformMotors(pos)
		return p

	# Return target position
	def act(obs, t, a, b, c):
		# Current position
		pos = obs[:12]
		# Desired position
		des = np.zeros(12)
		# Desired position populated according to parameters
		v = a * np.sin(t * b) + c
		positive = [1, 10, 2, 11]
		negative = [4, 7, 5, 8]
		zero = [0, 3, 6, 9]
		des[positive] = v
		des[negative] = -v
		des[zero] = 0
		# Convert desired position to real motor position 
		action = sim2real(0.1*des)
		# Define target position
		target_pos = pos + action
		return target_pos

	# Return position to take
	def get_action(state, steps):
		params = np.array([-0.57472189, -0.97479314, 0.04835059]) # with 10x actions
		#params = np.array([0.83972287, 0.79753211, 0.04102455]) # without 10x actions
		return act(state, steps, *params)

	# Read motor positions
	def get_state():
		state = []
		for j in range(1,5):
			u = 10*j
			r = range(u, u+3)
			for i in r:
				state.append(motor.readPosition(i))
		return state

	# MOVE MOTOR TO GIVEN POSITION
	def walk(pos):
		h = 0
		for j in range(1,5):
			u = 10*j
			r = range(u, u+3)
			for i in r:
				motor.move(i, int(pos[h]), 100)
				h+=1
		time.sleep(0.5)


	# RESET position and stand up before walking
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

	print('Start Walking!')

	# WALK
	while j < 10000:
		# Get current position of motors
		state = get_state()
		# Get target position
		pos = get_action(state, j)
		# Move robot to target position
		walk(pos)

		j += 1

