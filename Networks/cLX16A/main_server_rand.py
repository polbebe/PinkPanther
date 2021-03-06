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
		# Robot State values that will be bounced with client
		self.robot_state = None
		# Servo positions that will be sent to client
		self.servo_pos = None
		# abs(Value) of random change between robot positions
		self.delta_pos = 25

		# Start counter for walking robot
		self.i = 0

		# Socket Conneciton
		# MAC find WiFi IP - ipconfig getifaddr en0
		HOST = '192.168.1.29'
		# Port to listen on (non-privileged ports are > 1023)
		PORT = 65432
		print('Connected')

		# Set up Socket
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.s.bind((HOST, PORT))
		except socket.error as e:
			print(str(e))

		print('Waiting for connection[s]...')
		
		# Wait for client[s] to join socket
		self.conn1, addr1 = self.s.accept()
		print('Connected by: ', addr1)
		start_new_thread(self.main_client_thread, (self.conn1, ))

		self.conn2, addr2 = self.s.accept()
		print('Connected by: ', addr2)
		start_new_thread(self.cam_client_thread, (self.conn2, ))


	def main_client_thread(self, conn):
		# Receive Robot State from client
		self.robot_state = np.frombuffer(self.conn.recv(1024), dtype=np.float32)
		conn.sendall(self.servo_pos.tobytes())


	def cam_client_thread(self, conn):
		data = conn.recv(1024)
		print('Cam client says: {}'.format(data.decode('utf-8')))
		conn.sendall(str.encode('Hi'))


	def reset(self):
		# Set robot to position
		# Stand down
		self.servo_pos = np.array([500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500], dtype=np.float32)
		self.main_client_thread(self.conn1)
		# Stand up
		self.servo_pos = np.array([510, 750, 583, 500, 250, 417, 500, 750, 583, 500, 250, 417], dtype=np.float32)
		self.main_client_thread(self.conn2)


		self.robot_state = np.frombuffer(self.conn.recv(1024), dtype=np.float32)
		data = [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
		pos = np.array(data, dtype=np.float32)
		self.conn.sendall(pos.tobytes())
		# Stand up
		self.robot_state = np.frombuffer(self.conn.recv(1024), dtype=np.float32)
		data = [510, 750, 583, 500, 250, 417, 500, 750, 583, 500, 250, 417]
		pos = np.array(data, dtype=np.float32)
		self.conn.sendall(pos.tobytes())

		self.i = 0

		self.robot_state = None

		return self.robot_state


	def step(self):
		

		# Move motors to current position plus RANDOM delta_pos
		for l in range(12):
			if l%3 == 0:
				self.servo_pos[l] = self.robot_state[l]
			else:
				if random.getrandbits(1) > 0:
					self.servo_pos[l] = self.robot_state[l] + self.delta_pos
				else:
					self.servo_pos[l] = self.robot_state[l] - self.delta_pos

		# Prepare and send position data to clients
		self.conn.sendall(self.servo_pos.tobytes())

		# Update counter
		self.i += 1

		return self.robot_state


if __name__ == '__main__':
	# Construct MAIN SERVER object
	env = NetEnv()

	# Reset environment
	r_state = env.reset()

	# Get input from user
	input('Press any key to begin episode: ')

	# Keep track of time for average actions/second calculation
	start = time.time()
	j = 0
	# WALK
	for i in range(100):
		# Return current robot state on every loop
		r_state = env.step()
		# Print only every 10 loops
		if i%10 == 0:
			print(r_state)
		j+=4
		# Keep track of number of actions/second
		sys.stdout.write(str(i)+' in: '+str(round(time.time()-start,3))+' Averaging: '+str(round(j/(time.time()-start),2))+' actions/s\r')
	
	print('Done')

