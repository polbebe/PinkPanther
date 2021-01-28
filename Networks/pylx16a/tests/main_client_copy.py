from test_client import *

import socket

import numpy as np
import math
import time

class Listener():
	def __init__(self):
		# Socket Conneciton
		# MAC find WiFi IP - ipconfig getifaddr en0
		HOST = '192.168.1.29'
		# Port to listen on (non-privileged ports are > 1023)
		PORT = 65432

		# Connect to Socket set up by server
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((HOST, PORT))

		# Robot State values that will be updated
		self.robot_state = np.zeros(15, dtype=np.float32)
		# Servo position values that will be updated
		self.pos = None

		# 
		self.socket = True

		# Initialize both IMU client and SERVO client
		self.test = ImuData()

	# Read and return Robot state
	def read(self):
		# Read SERVO values and add them to Robot State
		self.robot_state[:12] = self.test.read()

		return self.robot_state

	def is_true(self):
		return self.socket

	# Interaction with server on every step of the robot
	def step(self):
		# Send current state of robot
		self.s.sendall(self.read().tobytes())

		# Receive new servo positions to be taken
		p = self.s.recv(1024)
		self.pos = np.frombuffer(p, dtype=np.float32)

		# If there's no more data being received, break the loop
		if not p:
			self.socket = False
			return None

		# Else confirm reception 
		print(self.pos)

if __name__ == '__main__':
	# Construct MAIN CLIENT object
	client = Listener()

	while client.is_true() == True:
		print(2)
		# Perform a step for the robot
		client.step()
		
		time.sleep(0.001)

