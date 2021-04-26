import numpy as np
import time
import csv
import sys


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

	def transformMotors(pos):
		null = lambda x: (x-500)/500
		fns =	[null, servo_left_elbow_sim2real, servo_left_shoulder_sim2real, null, servo_right_elbow_sim2real, servo_right_shoulder_sim2real, 
				null, servo_left_elbow_sim2real, servo_left_shoulder_sim2real, null, servo_right_elbow_sim2real, servo_right_shoulder_sim2real]
		targ = np.zeros(12)
		for i in range(len(pos)):
			targ[i] = fns[i](pos[i])
		return targ

	def real2sim(obs):
		obs = np.array(obs)
		pos, rp, xy = obs[0:12], obs[12:14], obs[15:]
		pos = transformMotors(pos) / 4
		# pos = (pos - 500) / 500
		rp = (rp-180) / 180
		xy = xy[::-1] * 0.0025
		return np.concatenate([pos, rp, xy])


	# A parameter to determine if we read actions from the server or select them randomly
	#train = False

	# Construct MAIN SERVER object
	#env = NetEnv()

	#interface = Interface(act_dim=env.act_dim, state_dim=env.state_dim)
	# Construct Agent object
	#agent = Agent(env.act_dim, env.state_dim, interface)
	# Reset environment
	real_obs = [500, 650, 533, 500, 350, 467, 500, 650, 533, 500, 350, 467]
	obs = real2sim(real_obs)

	def act(obs, t, a, b, c):
		current_p = obs[:12]
		desired_p = np.zeros(12)
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

	def get_action(state, steps):
		params = np.array([-0.57472189, -0.97479314, 0.04835059]) # with 10x actions
		#params = np.array([0.83972287, 0.79753211, 0.04102455]) # without 10x actions
		return act(state, steps, *params)

	def write_csv_real(data):
		with open('gait_v1_check_data.csv', 'a') as outfile:
			writer = csv.writer(outfile)
			writer.writerow(data)

	input('Press any key to begin episode: ')
	start = time.time()
	j = 0

	def step(action):
		# Move motors to current position plus RANDOM delta_pos
		robot_state = real_obs + 25 * action

		done = False
		r = 0 # the y position of the robot state serves as the reward

		return robot_state, r, done, {}

	# WALK
	while j < 400:
		# Return current robot state on every loop
		obs = real2sim(real_obs)
		action = get_action(obs, j)

		# if we want every 3rd to be frozen
		action[0::3] = 0

		real_obs, r, done, info = step(action)
		# Append the action number to end of list
		#data = np.append(obs[0], j)

		# Add state to csv
		write_csv_real(real_obs)

		j += 1

		# Keep track of number of actions/second
		sys.stdout.write(str(j) + ' in: ' + str(round(time.time() - start, 3)) + ' Averaging: ' + str(
			round(j / (time.time() - start), 2)) + ' actions/s\r')
	
	print('Done')
