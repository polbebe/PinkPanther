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
		self.pos = None
		self.message = np.array(12345, dtype=np.float32)

		# Socket Conneciton
		# MAC find WiFi IP - ipconfig getifaddr en0
		HOST = '192.168.1.29'
		# Port to listen on (non-privileged ports are > 1023)
		PORT = 65432

		self.ThreadCount = 0

		print('Connected')

		# Set up Socket
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.s.bind((HOST, PORT))
		except socket.error as e:
			print(str(e))

		print('Waiting for connection[s]...')

		self.s.listen()

		self.start = 0

		# Wait for client[s] to join socket
		self.conn1, addr1 = self.s.accept()
		print('Connected by: ', addr1)
		start_new_thread(self.main_client_thread, (self.conn1, ))

		self.conn2, addr2 = self.s.accept()
		print('Connected by: ', addr2)
		start_new_thread(self.cam_client_thread, (self.conn2, ))


	def main_client_thread(self, conn):
		data = conn.recv(1024)
		print('Main client says: {}'.format(data.decode('utf-8')))
		conn.sendall(str.encode('Hi'))


	def cam_client_thread(self, conn):
		data = conn.recv(1024)
		print('Cam client says: {}'.format(data.decode('utf-8')))
		conn.sendall(str.encode('Hi'))


	def step(self):
		self.main_client_thread(self.conn1)
		self.cam_client_thread(self.conn2)

if __name__ == '__main__':
	# Construct MAIN SERVER object
	env = NetEnv()

	# WALK
	for i in range(100000):
		env.step()
	
	print('Done')

