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
		self.robot_state = np.zeros(17, dtype=np.float32)
		# Servo positions that will be sent to client
		self.servo_pos = np.array([500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500], dtype=np.float32)
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
		
		self.s.listen()

		

		self.conn2, addr2 = self.s.accept()
		print('Connected by: ', addr2)
		start_new_thread(self.cam_client_thread, (self.conn2, ))




	def cam_client_thread(self, conn):
		# Send connection test to cam client
		conn.sendall(str.encode('i'))
		# Receive xy state from cam client & append to Robot State
		cam_state = np.frombuffer(conn.recv(1024), dtype=np.float32)
		if m.isnan(cam_state[0]) != True:
			self.robot_state[15] = cam_state[0]
			self.robot_state[16] = cam_state[1]



	def step(self):


		# CAM CLIENT
		# Get xy position from camera
		self.cam_client_thread(self.conn2)

		# Update counter
		self.i += 1

		return self.robot_state


if __name__ == '__main__':
	# Construct MAIN SERVER object
	env = NetEnv()



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
		#if i%10 == 0:
		print(r_state)
		j+=4
		# Keep track of number of actions/second
		sys.stdout.write(str(i)+' in: '+str(round(time.time()-start,3))+' Averaging: '+str(round(j/(time.time()-start),2))+' actions/s\r')
	
	print('Done')