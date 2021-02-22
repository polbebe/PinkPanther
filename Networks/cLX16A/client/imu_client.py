from sense_hat import SenseHat

import numpy as np

import time
import sys

class ImuData():
	# Constructor method
	def __init__(self):
		# Imu values that will be updated
		self.imu_values = np.zeros(3, dtype=np.float64)

		# Set up sense hat
		self.sense = SenseHat()
		self.sense.clear()

	# Read and return IMU Values
	def read(self):
		# Get the roll-pitch-yaw values from sense hat
		o = self.sense.get_orientation()

		# Write new IMU values
		self.imu_values[0] = o["roll"]
		self.imu_values[1] = o["pitch"]
		self.imu_values[2] = o["yaw"]

		return self.imu_values

'''
if __name__ == '__main__':
	# Construct IMU object and allow use of methods
	i = ImuData()

	# UNIT TEST
	while True:
		# Get IMU data from robot
		a = i.read()
		print(a)
'''