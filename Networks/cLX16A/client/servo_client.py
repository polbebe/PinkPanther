from ServoMotor import *

import numpy as np
import sys
import time

class ServoData():
	# Constructor method
	def __init__(self):
		# Servo position values that will be updated
		self.servo_values = np.zeros(12, dtype=np.float64)
		self.pos = None

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
				# NOT READING SHOULDER SERVOS!!!
				if l%10 == 0:
					self.servo_values[z] = 0
				else:
					self.servo_values[z] = motor.readPosition(l)
				z += 1

		return self.servo_values

if __name__ == '__main__':
	# Construct SERVO object and allow use of methods
	i = ServoData()
