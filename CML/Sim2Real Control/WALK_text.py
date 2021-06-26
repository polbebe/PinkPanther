import numpy as np
import time
import sys

pos = []

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
	def transformMotorsS2R(pos):
		null = lambda x: 500
		fns =	[null, servo_left_elbow_sim2real, servo_left_shoulder_sim2real, null, servo_right_elbow_sim2real, servo_right_shoulder_sim2real, 
				null, servo_left_elbow_sim2real, servo_left_shoulder_sim2real, null, servo_right_elbow_sim2real, servo_right_shoulder_sim2real]
		targ = np.zeros(12)
		for i in range(len(pos)):
			targ[i] = fns[i](pos[i])
		return targ

	# Call corresponding function to convert sim2real
	def transformMotorsR2S(pos):
		null = lambda x: 0
		fns =	[null, servo_left_elbow_sim2real, servo_left_shoulder_sim2real, null, servo_right_elbow_sim2real, servo_right_shoulder_sim2real, 
				null, servo_left_elbow_sim2real, servo_left_shoulder_sim2real, null, servo_right_elbow_sim2real, servo_right_shoulder_sim2real]
		targ = np.zeros(12)
		for i in range(len(pos)):
			targ[i] = fns[i](pos[i])
		return targ

	# Return real positions for a given simulated position
	def sim2real(pos):
		p = transformMotorsS2R(pos)
		return p

	# Return real positions for a given simulated position
	def real2sim(pos):
		p = transformMotorsR2S(pos)
		return p

	# Return target position
	def act(obs, t, a, b, c):
		# Current motor positions
		current_p = real2sim(obs[:12])
		# Target position to be populated
		desired_p = np.zeros(12)
		# Populate
		v = a * np.sin(t * b) + c
		pos = [1, 10, 2, 11]
		neg = [4, 7, 5, 8]
		zero = [0, 3, 6, 9]
		desired_p[pos] = v
		desired_p[neg] = -v
		desired_p[zero] = 0

		delta_p = (desired_p - current_p)
		delta_p = np.clip(delta_p, -1, 1)
		return delta_p

	# Return position to take
	def get_action(state, steps):
		params = np.array([-0.57472189, -0.97479314, 0.04835059]) # with 10x actions
		#params = np.array([0.83972287, 0.79753211, 0.04102455]) # without 10x actions
		return act(state, steps, *params)

	# Read motor positions
	def get_state():
		return pos

	# RESET position and stand up before walking
	pos = [500, 750, 583, 500, 250, 417, 500, 750, 583, 500, 250, 417]

	print('Start Walking!')

	j = 0
	# WALK
	while j < 10000:
		# Get current position of motors
		state = get_state()
		# Get target position
		target_pos = get_action(state, j)
		# Move robot to target position
		print(pos)
		time.sleep(0.1)

		j += 1

