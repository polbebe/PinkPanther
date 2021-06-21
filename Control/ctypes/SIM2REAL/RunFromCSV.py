import numpy as np
from ServoMotor import *
import sys
import time as timer

data = np.genfromtxt("commanded_pos.csv", delimiter=",", names=["10", "11", "12", "20", "21", "22", "30", "31", "32", "40", "41", "42"])

# Initialize ServoMotor class
filename = "/dev/ttyUSB0"
motor = ServoMotor(filename)

# Initialize USB Port
IO = motor.IO_Init()
if IO < 0:
	print('IO exit')
	sys.exit()

offsets = [30, 0, 64, 0, 70, 50, 26, 0, 55, 80, 90, 35]

h = 0
# Set servo mode to all servos with their offset
for j in range(1,5):
	u = 10*j
	r = range(u, u+3)
	for i in r:
		motor.setServoMode(i)
		if offsets[h]!=0:
			motor.setPositionOffset(i,offsets[h])
		h+=1

# Time allowed for servos to take their positions
time = 500

for x in range(len(data)):

	# Move all servos to next position specified in csv
	for j in range(1,5):
		u = 10*j
		r = range(u, u+3)
		for i in r:
			motor.move(i, int(data['{}'.format(i)][x]), time)

	timer.sleep(0.3)


