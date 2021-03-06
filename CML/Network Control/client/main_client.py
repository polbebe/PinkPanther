from imu_client import *
from servo_client import *

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
		try:
			self.s.connect((HOST, PORT))
		except socket.error as e:
			print(str(e))

		# Robot State values that will be updated
		self.robot_state = np.zeros(15, dtype=np.float32)
		# Servo position values that will be updated
		self.pos = None

		self.socket = True

		# Initialize both IMU client and SERVO client
		self.imu = ImuData()
		self.servo = ServoData()

	# Read and return Robot state
	def read(self):
		# Read SERVO values and add them to Robot State
		self.robot_state[:12] = self.servo.read()

		# Read IMU values and add them to Robot State
		self.robot_state[12:] = self.imu.read()

		return self.robot_state

	# Interaction with server on every step of the robot
	def step(self):
		# Receive new servo positions to be taken
		p = self.s.recv(1024)
		self.pos = np.frombuffer(p, dtype=np.float32)

		# If there's no more data being received, break the loop
		if not p:
			print('CONNECTION BROKEN')
			self.socket = False
			return None
		
		# Else write
		self.servo.write(self.pos, 100)

		# Send current state of robot
		self.s.sendall(np.array(self.read(), dtype=np.float32).tobytes())

	# Reset the robot
	def reset(self):
		# Set robot to position
		# Stand down
		p = self.s.recv(1024)
		self.pos = np.frombuffer(p, dtype=np.float32)
		self.servo.write(self.pos, 1000)
		time.sleep(1)
		self.s.sendall(self.read().tobytes())
		# Stand up
		p = self.s.recv(1024)
		self.pos = np.frombuffer(p, dtype=np.float32)
		self.servo.write(self.pos, 1000)
		time.sleep(1)
		self.s.sendall(self.read().tobytes())

	# Check whether socket should still be running
	def is_true(self):
		return self.socket

if __name__ == '__main__':
	# Construct MAIN CLIENT object
	client = Listener()

	client.reset()

	# While the server is communicating
	while client.is_true() == True:
		# Perform a step for the robot
		client.step()
		
		#time.sleep(0.001)
