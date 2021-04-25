import numpy as np
from ServoMotor import *
import sys
import time as timer

a_ls = 0.75
c_ls = 0.45

a_le = 0.9
c_le = 0.3

b = 0.1

def movement(a, b, c, t):
	v = a * np.sin(t * b) + c
	return v

# SIM 2 REAL
def servo_left_shoulder_sim2real(targ):
	if targ>=0:
		pos = (621 - (targ/1.2)*(621-354))
	else:
		pos = (621 + (abs(targ)/0.3)*(688-621))
	return int(round(pos))
def servo_left_elbow_sim2real(targ):
	if targ>=0:
		pos = (721 + (targ/1.2)*(1000-721))
	else:
		pos = (721 - (abs(targ)/0.6)*(721-500))
	return int(round(pos))

def servo_right_shoulder_sim2real(targ):
	if targ>=0:
		pos = (375 + (targ/1.2)*(625-375))
	else:
		pos = (375 - (abs(targ)/0.3)*(375-313))
	return int(round(pos))
def servo_right_elbow_sim2real(targ):
	if targ>=0:
		pos = (279 - (targ/1.2)*(279-0))
	else:
		pos = (279 + (abs(targ)/0.6)*(500-279))
	return int(round(pos))


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


t=0
time = 100
while t<300:
	motor.move(12, int(servo_left_shoulder_sim2real(movement(a_ls,b,c_ls,t))), time)
	motor.move(11, int(servo_left_elbow_sim2real(movement(a_le,b,c_le,t))), time)

	#motor.move(32, int(servo32_sim2real(movement(a,b,c,t))), time)
	#motor.move(31, int(servo31_sim2real(movement(a,b,c,t))), time)

	#motor.move(22, int(servo22_sim2real(movement(a,b,c,t))), time)
	#motor.move(21, int(servo21_sim2real(movement(a,b,c,t))), time)

	#motor.move(42, int(servo42_sim2real(movement(a,b,c,t))), time)
	#motor.move(41, int(servo41_sim2real(movement(a,b,c,t))), time)

	timer.sleep(0.1)

	t+=1

	print(int(servo_left_elbow_sim2real(movements(a_le,b,c_le,t))))


