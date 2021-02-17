#!/usr/bin/env python3
import numpy as np
import pandas as pd
import math as m
import time
import sys
from ServoMotor import *
import random


# Set up C-types
filename = "/dev/ttyUSB0"
motor = ServoMotor(filename)
IO = motor.IO_Init()
if IO < 0:
	print('IO exit')
	sys.exit()

# Set up all motors in servo mode
for j in range(1,5):
	a = 10*j
	r = range(a, a+3)
	for i in r:
		motor.setServoMode(i)

# Initialize
pos = np.zeros(12, dtype=np.float32)
delta_pos = 25
i = 0
j = 0
max_actions = 100 #Real = max_actions*4
start = time.time()

# WALK
while j<max_actions:

	# Get current position of motors
	z = 0
	for k in range(1,5):
		a = 10*k
		r = range(a, a+3)
		for l in r:
			pos[z] = motor.readPosition(l)
			z += 1

	
	# Move motors to current position plus RANDOM delta_pos
	z = 0
	for k in range(1,5):
		a = 10*k
		r = range(a, a+3)
		for l in r:
			if l%10 == 0:
				motor.move(l, int(pos[z]), 100)
			else:
				if random.getrandbits(1) > 0:
					motor.move(l, int(pos[z] + delta_pos), 100)
				else:
					motor.move(l, int(pos[z] - delta_pos), 100)
			z += 1

	# patience
	time.sleep(0.1)

	# Calculate the actions/second
	sys.stdout.write(str(i)+' in: '+str(round(time.time()-start,3))+' Averaging: '+str(round(i/(time.time()-start),2))+' actions/s\r')
	
	i += 4
	j += 1

# Real actons/second
print(str(i)+' in: '+str(round(time.time()-start,3))+' Averaging: '+str(round(i/(time.time()-start),2))+' actions/s')


