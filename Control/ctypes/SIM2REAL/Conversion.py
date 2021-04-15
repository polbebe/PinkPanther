import numpy as np
from ServoMotor import *
import sys
import time

a = 0.3
b = 3
c = 0.1

def movement(a, b, c, t):
	v = a * np.sin(t * b) + c
	return v

# SIM 2 REAL
def servo12_sim2real(targ12):
	if targ12>=0:
		pos12 = (140 - (targ12/1.2)*65)*(25/6)
	else:
		pos12 = ((abs(targ12)/1)*25 + 140)*(25/6)
	return int(round(pos12))
def servo11_sim2real(targ11):
	if targ11>=0:
		pos11 = ((targ11/1.5)*60 + 180)*(25/6)
	else:
		pos11 = (180 - (abs(targ11)/0.6)*40)*(25/6)
	return int(round(pos11))

def servo32_sim2real(targ32):
	if targ32>=0:
		pos32 = (140 - (targ32/1.2)*65)*(25/6)
	else:
		pos32 = ((abs(targ32)/1)*25 + 140)*(25/6)
	return int(round(pos32))
def servo31_sim2real(targ31):
	if targ31>=0:
		pos31 = ((targ31/1.5)*60 + 180)*(25/6)
	else:
		pos31 = (180 - (abs(targ31)/0.6)*40)*(25/6)
	return int(round(pos31))

def servo22_sim2real(targ22):
	if targ22>=0:
		pos22 = ((targ22/1.2)*65 + 100)*(25/6)
	else:
		pos22 = (100 - (abs(targ22)/1)*25)*(25/6)
	return int(round(pos22))
def servo21_sim2real(targ21):
	if targ21>=0:
		pos21 = (60 - (targ21/1.5)*60)*(25/6)
	else:
		pos21 = ((abs(targ21)/0.6)*60 + 60)*(25/6)
	return int(round(pos21))

def servo42_sim2real(targ42):
	if targ42>=0:
		pos42 = ((targ42/1.2)*65 + 100)*(25/6)
	else:
		pos42 = (100 - (abs(targ42)/1)*25)*(25/6)
	return int(round(pos42))
def servo41_sim2real(targ41):
	if targ41>=0:
		pos41 = (60 - (targ41/1.5)*60)*(25/6)
	else:
		pos41 = ((abs(targ41)/0.6)*60 + 60)*(25/6)
	return int(round(pos41))


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
	a = 10*j
	r = range(a, a+3)
	for i in r:
		motor.setServoMode(i)
		if offsets[h]!=0:
			motor.setPositionOffset(i,offsets[h])
		h+=1


t=0
time = 100
while t<300:
	motor.move(12, int(servo12_sim2real(movement(a,b,c,t))), time)
	motor.move(11, int(servo11_sim2real(movement(a,b,c,t))), time)

	motor.move(32, int(servo32_sim2real(movement(a,b,c,t))), time)
	motor.move(31, int(servo31_sim2real(movement(a,b,c,t))), time)

	motor.move(22, int(servo22_sim2real(movement(a,b,c,t))), time)
	motor.move(21, int(servo21_sim2real(movement(a,b,c,t))), time)

	motor.move(42, int(servo42_sim2real(movement(a,b,c,t))), time)
	motor.move(41, int(servo41_sim2real(movement(a,b,c,t))), time)

	time.sleep(100)

	t+=1


