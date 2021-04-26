import gym
import gym.spaces as spaces
import sys

import socket

from _thread import *
import os

import csv

import numpy as np
import pandas as pd
import math as m
import time
import random

class Interface:
	def __init__(self, host='128.59.145.148', port=8123, act_dim=1, state_dim=1):
		print('before')
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((host, port))
		print('after')
		msg = self.s.recv(1024)
		d = np.array([state_dim, act_dim], dtype=np.int)
		if msg == b'Init':
			print(d)
			self.s.sendall(d.tobytes())

	def get_action(self, obs, r=0, done=False):
		self.update(obs, r, done)
		action = np.frombuffer(self.s.recv(1024), dtype=np.float32)
		return action.copy()

	def update(self, obs, r, done):
		state = np.zeros(len(obs)+2, dtype=np.float32)
		print(state)
		print(state.shape)
		print(obs)
		print(obs.shape)
		state[:-2] = obs
		state[-2] = r
		if done:
			state[-1] = 1
		self.s.sendall(state.tobytes())

class Agent:
	def __init__(self, act_dim, state_dim, interface=None):
		self.act_dim, self.state_dim = act_dim, state_dim
		self.interface = interface

	def policy(self, state, train=False):
		if train:
			return np.random.uniform(-2, 2, self.act_dim) #np.random.choice([1, -1], self.act_dim)
		else:
			return self.interface.get_action(state)

class NetEnv(gym.Env):
	def __init__(self):
		# Servo positions that will be sent to client
		self.servo_pos = np.array([500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500], dtype=np.float32)
		self.servo_pos_0 = np.array([500, 650, 533, 500, 350, 467, 500, 650, 533, 500, 350, 467], dtype=np.float32)
		# abs(Value) of random change between robot positions
		self.delta_pos = 25.0
		self.act_dim = 12
		self.state_dim = 17
		self.ep_len = 200

		# Robot State values that will be bounced with client
		self.robot_state = np.zeros(self.state_dim, dtype=np.float32)

		# Socket Conneciton
		# MAC find WiFi IP - ipconfig getifaddr en0
		HOST = '192.168.1.29'
		# Port to listen on (non-privileged ports are > 1023)
		PORT = 65434
		print('Connected')

		# Set up Socket
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.s.bind((HOST, PORT))
		except socket.error as e:
			print(str(e))

		print('Waiting for connection[s]...')

		self.s.listen()

		# Wait for client[s] to join socket
		self.conn1, addr1 = self.s.accept()
		print('Connected by: ', addr1)
		start_new_thread(self.main_client_thread, (self.conn1,))

		self.conn2, addr2 = self.s.accept()
		print('Connected by: ', addr2)
		start_new_thread(self.cam_client_thread, (self.conn2,))

		# Keep track of whether socket should be on or off
		self.socket = True

	def main_client_thread(self, conn):
		# Send motor position to main client
		conn.sendall(self.servo_pos.tobytes())
		# Receive Robot State from main client
		pp_state = np.frombuffer(conn.recv(1024), dtype=np.float32)
		for i in range(15):
			if i < 12:
				self.servo_pos[i] = pp_state[i]
			self.robot_state[i] = pp_state[i]

	def cam_client_thread(self, conn):
		# Send connection test to cam client
		conn.sendall(str.encode('i'))
		# Receive xy state from cam client & append to Robot State
		cam_state = np.frombuffer(conn.recv(1024), dtype=np.float32)
		# If apriltag is recognizable, continue, otherwise stop connection
		if m.isnan(cam_state[0]) != True:
			self.robot_state[15] = cam_state[0]
			self.robot_state[16] = cam_state[1]
		else:
			self.robot_state[15] = 0
			self.robot_state[16] = 0
			self.socket = False


	def reset(self):
		# Set robot to position
		# Stand up
		self.servo_pos = np.array([500, 650, 533, 500, 350, 467, 500, 650, 533, 500, 350, 467], dtype=np.float32)
		self.main_client_thread(self.conn1)
		self.i = 0

		return self.robot_state

	def step(self, action):
		# MAIN CLIENT
		# Move motors to current position plus RANDOM delta_pos
		self.servo_pos += self.delta_pos * action
		self.servo_pos_0 = self.servo_pos
		#self.write_csv_theory(self.servo_pos_0)

		# Send new position data to clients
		self.main_client_thread(self.conn1)

		# CAM CLIENT
		# Get xy position from camera
		self.cam_client_thread(self.conn2)

		self.i += 1

		done = self.i >= self.ep_len
		r = self.robot_state[-1] # the y position of the robot state serves as the reward

		return self.robot_state, r, done, {}

	
	# Check whether socket should still be running
	def is_true(self):
		return self.socket


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
	train = False

	# Construct MAIN SERVER object
	env = NetEnv()

	#interface = Interface(act_dim=env.act_dim, state_dim=env.state_dim)
	# Construct Agent object
	#agent = Agent(env.act_dim, env.state_dim, interface)
	# Reset environment
	obs = env.reset()
	obs = real2sim(obs)

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
		with open('gait_v1_platform_data.csv', 'a') as outfile:
			writer = csv.writer(outfile)
			writer.writerow(data)

	input('Press any key to begin episode: ')
	start = time.time()
	j = 0

	# WALK
	while env.is_true() == True:
		# Return current robot state on every loop
		obs = real2sim(obs)
		action = get_action(obs, j)

		# if we want every 3rd to be frozen
		action[0::3] = 0

		obs, r, done, info = env.step(action)
		# Append the action number to end of list
		data = np.append(obs[0], j)

		# Add state to csv
		write_csv_real(obs[:12])

		j += 1

		# Keep track of number of actions/second
		sys.stdout.write(str(j) + ' in: ' + str(round(time.time() - start, 3)) + ' Averaging: ' + str(
			round(j / (time.time() - start), 2)) + ' actions/s\r')
	
	print('Done')
