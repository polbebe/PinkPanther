#!/usr/bin/env python3
import numpy as np
import pandas as pd
import math as m
import time
import sys
from ServoMotor import *

# Functions for servo position conversion
def servo12(targ12):
	if targ12>=0:
		pos12 = (140 - (targ12/1.2)*65)*(25/6)
	else:
		pos12 = ((abs(targ12)/1)*25 + 140)*(25/6)
	return int(round(pos12))
def servo11(targ11):
	if targ11>=0:
		pos11 = ((targ11/1.5)*60 + 180)*(25/6)
	else:
		pos11 = (180 - (abs(targ11)/0.6)*40)*(25/6)
	return int(round(pos11))
def servo32(targ32):
	if targ32>=0:
		pos32 = (140 - (targ32/1.2)*65)*(25/6)
	else:
		pos32 = ((abs(targ32)/1)*25 + 140)*(25/6)
	return int(round(pos32))
def servo31(targ31):
	if targ31>=0:
		pos31 = ((targ31/1.5)*60 + 180)*(25/6)
	else:
		pos31 = (180 - (abs(targ31)/0.6)*40)*(25/6)
	return int(round(pos31))
def servo22(targ22):
	if targ22>=0:
		pos22 = ((targ22/1.2)*65 + 100)*(25/6)
	else:
		pos22 = (100 - (abs(targ22)/1)*25)*(25/6)
	return int(round(pos22))
def servo21(targ21):
	if targ21>=0:
		pos21 = (60 - (targ21/1.5)*60)*(25/6)
	else:
		pos21 = ((abs(targ21)/0.6)*60 + 60)*(25/6)
	return int(round(pos21))
def servo42(targ42):
	if targ42>=0:
		pos42 = ((targ42/1.2)*65 + 100)*(25/6)
	else:
		pos42 = (100 - (abs(targ42)/1)*25)*(25/6)
	return int(round(pos42))
def servo41(targ41):
	if targ41>=0:
		pos41 = (60 - (targ41/1.5)*60)*(25/6)
	else:
		pos41 = ((abs(targ41)/0.6)*60 + 60)*(25/6)
	return int(round(pos41))

version= "0.2.1"

# Read v values from those saved from simulation
df = pd.read_csv('V/Hardcoded_{}.csv'.format(version))
v = np.array(df['Best Values'], dtype=np.float32)
# Create positons array that will be calculated on each step
# and sent to client
pos = np.zeros(12, dtype=np.float32)
prev_pos = np.zeros(12, dtype=np.float32)
diff = []

filename = "/dev/ttyUSB0"
motor = ServoMotor(filename)

# Initialize USB Port
IO = motor.IO_Init()
if IO < 0:
	print('IO exit')
	sys.exit()

# Set servo mode to all servos
# LEFT front
motor.setServoMode(10)
motor.setServoMode(12)
motor.setServoMode(11)
# LEFT back
motor.setServoMode(30)
motor.setServoMode(32)
motor.setServoMode(31)
# RIGHT front
motor.setServoMode(20)
motor.setServoMode(22)
motor.setServoMode(21)
# RIGTH back
motor.setServoMode(40)
motor.setServoMode(42)
motor.setServoMode(41)


max_diff = 0

i = 0
j = 0
max_time = 400
start = time.time()
while j<max_time:
	# Calculate servo positions
	pos[0] = 510
	pos[1] = servo12(v[3] + v[4]*m.sin(i*v[36] + v[5]))
	pos[2] = servo11(v[6] + v[7]*m.sin(i*v[36] + v[8]))
	pos[3] = 500
	pos[4] = servo22(v[12] + v[13]*m.sin(i*v[36] + v[14]))
	pos[5] = servo21(v[15] + v[16]*m.sin(i*v[36] + v[17]))
	pos[6] = 500
	pos[7] = servo32(v[21] + v[22]*m.sin(i*v[36] + v[23]))
	pos[8] = servo31(v[24] + v[25]*m.sin(i*v[36] + v[26]))
	pos[9] = 500
	pos[10] = servo42(v[30] + v[31]*m.sin(i*v[36] + v[32]))
	pos[11] = servo41(v[33] + v[34]*m.sin(i*v[36] + v[35]))
	
	if j>0:
		zip_object = zip(pos, prev_pos)
		for pos_i, prev_pos_i in zip_object:
			diff.append(abs(pos_i - prev_pos_i))
		if max(diff) > max_diff:
			max_diff = max(diff)
	
	prev_pos[0] = pos[0] 
	prev_pos[1] = pos[1]
	prev_pos[2] = pos[2] 
	prev_pos[3] = pos[3] 
	prev_pos[4] = pos[4] 
	prev_pos[5] = pos[5] 
	prev_pos[6] = pos[6] 
	prev_pos[7] = pos[7] 
	prev_pos[8] = pos[8] 
	prev_pos[9] = pos[9] 
	prev_pos[10] = pos[10]
	prev_pos[11] = pos[11]

	
	
	# Move all servos to their corresponding position
	# LEFT front
	motor.move(10, int(pos[0]), 100)
	motor.move(12, int(pos[1]), 100)
	motor.move(11, int(pos[2]), 100)
	# LEFT back
	motor.move(30, int(pos[6]), 100)
	motor.move(32, int(pos[7]), 100)
	motor.move(31, int(pos[8]), 100)
	# RIGHT front
	motor.move(20, int(pos[3]), 100)
	motor.move(22, int(pos[4]), 100)
	motor.move(21, int(pos[5]), 100)
	# RIGTH back
	motor.move(40, int(pos[9]), 100)
	motor.move(42, int(pos[10]), 100)
	motor.move(41, int(pos[11]), 100)

	time.sleep(0.1)

	# Calculate the actions/second
	sys.stdout.write(str(i)+' in: '+str(round(time.time()-start,3))+' Averaging: '+str(round(i/(time.time()-start),2))+' actions/s\r')
	i += 4
	j += 1

print(str(i)+' in: '+str(round(time.time()-start,3))+' Averaging: '+str(round(i/(time.time()-start),2))+' actions/s')
print('Max difference between any two positions was {}'.format(max_diff))


