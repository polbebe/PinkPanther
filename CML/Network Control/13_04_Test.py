import gym
import gym.spaces as spaces
import sys

import socket

from _thread import *
import os

import numpy as np
import pandas as pd
import math as m
import time
import random

class NetEnv(gym.Env):
	def __init__(self):
		self.servo_pos = np.array([500, 650, 533, 500, 350, 467, 500, 650, 533, 500, 350, 467], dtype=np.float32)
		self.delta_pos = 25.0
		self.act_dim = 12
		self.state_dim = 17
		self.ep_len = 200

		#self.robot_state = np.zeros(self.state_dim, dtype=np.float32)

		HOST = '192.168.1.29'
		PORT = 65431
		print('Connected')

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.s.bind((HOST, PORT))
		except socket.error as e:
			print(str(e))
		print('Waiting for connection[s]...')
		self.s.listen()
		self.conn1, addr1 = self.s.accept()
		print('Connected by: ', addr1)
		start_new_thread(self.main_client_thread, (self.conn1,))
		self.socket = True

	def main_client_thread(self, conn):
		conn.sendall(self.servo_pos.tobytes())
		print('sent')
		pp_state = np.frombuffer(conn.recv(1024), dtype=np.float32)
		print('recvd')
		# 
		# 
		# Current taken from read
		for i in range(12):
			self.servo_pos[i] = pp_state[i]
		print(self.servo_pos)

	def reset(self):
		self.main_client_thread(self.conn1)
		self.i = 0
		return self.servo_pos

	def step(self, action):
		print(self.servo_pos)
		self.servo_pos += self.delta_pos * action
		print(self.servo_pos)
		self.main_client_thread(self.conn1)
		print('ok')
		self.i += 1
		done = self.i >= self.ep_len
		r = 1
		return self.servo_pos, r, done, {}

	def pos(self):
		return self.servo_pos

	def is_true(self):
		return self.socket


if __name__ == '__main__':

	def servo12(pos12):
		if pos12>=583.3:
			targ12 = (140 - (6/25)*pos12)*(1.2/65)
		else:
			targ12 = -((6/25)*pos12 - 140)*(1/25)
		return targ12
	def servo11(pos11):
		if pos11>=750:
			targ11 = ((6/25)*pos11 - 180)*(1.5/60)
		else:
			targ11 = -(180 - (6/25)*pos11)*(0.6/40)
		return targ11

	def servo32(pos32):
		if pos32>=583.3:
			targ32 = (140 - (6/25)*pos32)*(1.2/65)
		else:
			targ32 = -((6/25)*pos32 - 140)*(1/25)
		return targ32
	def servo31(pos31):
		if pos31>=750:
			targ31 = ((6/25)*pos31 - 180)*(1.5/60)
		else:
			targ31 = -(180 - (6/25)*pos31)*(0.6/40)
		return targ31

	def servo22(pos22):
		if pos22>=416.6:
			targ22 = ((6/25)*pos22 - 100)*(1.2/65)
		else:
			targ22 = -(100 - (6/25)*pos22)*(1/25)
		return targ22
	def servo21(pos21):
		if pos21>=250:
			targ21 = (60 - (6/25)*pos21)*(1.5/60)
		else:
			targ21 = -((6/25)*pos21 - 60)*(0.6/60)
		return targ21

	def servo42(pos42):
		if pos42>=416.6:
			targ42 = ((6/25)*pos42 - 100)*(1.2/65)
		else:
			targ42 = -(100 - (6/25)*pos42)*(1/25)
		return targ42
	def servo41(pos41):
		if pos41>=250:
			targ41 = (60 - (6/25)*pos41)*(1.5/60)
		else:
			targ41 = -((6/25)*pos41 - 60)*(0.6/60)
		return targ41

	def transformMotors(pos):
		null = lambda x: (x-500)/500
		fns = [null, servo11, servo12, null, servo21, servo22, null, servo31, servo32, null, servo41, servo42]
		targ = np.zeros(12)
		for i in range(len(pos)):
			targ[i] = fns[i](pos[i])
		return targ

	def real2sim(obs):
		obs = np.array(obs)
		pos = obs[:12]
		pos = transformMotors(pos) / 4
		return pos

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

	env = NetEnv()

	obs = env.reset()
	obs = real2sim(obs)

	input('Press any key to begin episode: ')

	start = time.time()
	j = 0
	while env.is_true() == True:
		action = get_action(obs, j)

		action[0::3] = 0
		obs, r, done, info = env.step(action)
		print(j)
		obs = real2sim(obs)
		print(j)

		j += 1
		sys.stdout.write(str(j) + ' in: ' + str(round(time.time() - start, 3)) + ' Averaging: ' + str(
			round(j / (time.time() - start), 2)) + ' actions/s\r')
	
	print('Done')
