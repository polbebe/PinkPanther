from ServoMotor import *

import numpy as np

import sys
import time
import random

class ServoData():
	# Constructor method
	def __init__(self):
		# Servo position values that will be updated
		self.servo_values = np.zeros(12, dtype=np.float64)

		# Initialize ServoMotor class
		filename = "/dev/ttyUSB0"
		self.motor = ServoMotor(filename)

		# Initialize USB Port
		self.IO = self.motor.IO_Init()
		if self.IO < 0:
			print('IO exit')
			sys.exit()

		# Set servo mode to all servos
		for j in range(1,5):
			a = 10*j
			r = range(a, a+3)
			for i in r:
				self.motor.setServoMode(i)
		
	# Write new current SERVO Values
	def write(self, pos):
		# Move motors to next position
		z = 0
		for k in range(1,5):
			a = 10*k
			r = range(a, a+3)
			for l in r:
				self.motor.move(l, int(pos[z]), 100)
				z += 1
		
		time.sleep(0.1)

	# Read and return SERVO Values
	def read(self):
		# Get the servo values from servos
		z = 0
		for k in range(1,5):
			a = 10*k
			r = range(a, a+3)
			for l in r:
				# NOT READING SHOULDER SERVOS!!! (their ids are 10,20,30,40)
				if l%10 == 0:
					self.servo_values[z] = 0
				else:
					self.servo_values[z] = self.motor.readPosition(l)
				z += 1

		return self.servo_values

'''
if __name__ == '__main__':
	# Construct SERVO object and allow use of methods
	i = ServoData()

	delta_pos = 25

	# UNIT TEST
	while True:
		# Give random movement to robot at each step
		pos = [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]
		for l in range(12):
			if l%3 == 0:
				continue
			else:
				if random.getrandbits(1) > 0:
					pos[l] += delta_pos
				else:
					pos[l] -= delta_pos
		a = i.write(pos)
		
		b = i.read()
		print(b)
'''