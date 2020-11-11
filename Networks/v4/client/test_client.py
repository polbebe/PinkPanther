import numpy as np
from threading import Thread

class ImuData():
	def __init__(self):
		# Imu values that will be updated
		self.imu_values = np.zeros(12, dtype=np.float64)

	# Read and return IMU Values
	def read(self):
		# Write new IMU values
		self.imu_values[0] = 1
		self.imu_values[1] = 2
		self.imu_values[2] = 3
		return self.imu_values

if __name__ == '__main__':
	# Construct IMU object and allow use of methods
	i = ImuData()