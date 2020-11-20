from lx16a import *
import time
import numpy

# Initialize the port that the controller board is connected to
# LX16A.initialize("COM3")
LX16A.initialize("/dev/ttyUSB0")

# Initialize ALL servos
# Front Left
s10 = LX16A(10)
s12 = LX16A(12)
s11 = LX16A(11)
# Front Right
s20 = LX16A(20)
s22 = LX16A(22)
s21 = LX16A(21)
# Back Left
s30 = LX16A(30)
s32 = LX16A(32)
s31 = LX16A(31)
# Back Right
s40 = LX16A(40)
s42 = LX16A(42)
s41 = LX16A(41)

# Simulation Targets
armpit_lf=0
elbow_lf=0
knee_lf=0

armpit_rf=0
elbow_rf=0
knee_rf=0

armpit_lb=0
elbow_lb=0
knee_lb=0

armpit_rb=0
elbow_rb=0
knee_rb=0


# Simulation 2 Reality converter functions
# FRONT LEFT
def servo10(targ):
	if targ>=0:
		pos = 120 - (targ/0.3)*20
	else:
		pos = 120 + abs(targ/0.3)*20
	return pos

def servo12(targ):
	if targ>=0.45:
		pos = 125 - ((targ-0.45)/0.75)*40
	elif targ<0.45 and targ>0:
		pos = 125 + ((0.45-targ)/0.45)*24
	elif targ<=0:
		pos = 149 + abs(targ/0.3)*16
	return pos

def servo11(targ):
	if targ>=0.3:
		pos = 190 + ((targ-0.3)/0.9)*50
	elif targ<0.3 and targ>0:
		pos = 190 - ((0.3-targ)/0.3)*(50/3)
	elif targ<=0:
		pos = (520/3) - abs(targ/0.6)*(100/3)
	return pos

# BACK LEFT
def servo30(targ):
	if targ>=0:
		pos = 120 + (targ/0.3)*20
	else:
		pos = 120 - abs(targ/0.3)*20
	return pos

def servo32(targ):
	if targ>=0.45:
		pos = 125 - ((targ-0.45)/0.75)*40
	elif targ<0.45 and targ>0:
		pos = 125 + ((0.45-targ)/0.45)*24
	elif targ<=0:
		pos = 149 + abs(targ/0.3)*16
	return pos

def servo31(targ):
	if targ>=0.3:
		pos = 190 + ((targ-0.3)/0.9)*50
	elif targ<0.3 and targ>0:
		pos = 190 - ((0.3-targ)/0.3)*(50/3)
	elif targ<=0:
		pos = (520/3) - abs(targ/0.6)*(100/3)
	return pos

# FRONT RIGHT
def servo20(targ):
	if targ>=0:
		pos = 120 - (targ/0.3)*20
	else:
		pos = 120 + abs(targ/0.3)*20
	return pos

def servo22(targ):
	if targ>=0.45:
		pos = 112.5 + ((targ-0.45)/0.75)*37.5
	elif targ<0.45 and targ>0:
		pos = 112.5 - ((0.45-targ)/0.45)*22.5
	elif targ<=0:
		pos = 90 - abs(targ/0.3)*15
	return pos

def servo21(targ):
	if targ>=0.3:
		pos = 50 - ((targ-0.3)/0.9)*50
	elif targ<0.3 and targ>0:
		pos = 50 + ((0.3-targ)/0.3)*(50/3)
	elif targ<=0:
		pos = (200/3) + abs(targ/0.6)*(100/3)
	return pos

# BACK RIGHT
def servo40(targ):
	if targ>=0:
		pos = 120 - (targ/0.3)*20
	else:
		pos = 120 + abs(targ/0.3)*20
	return pos

def servo42(targ):
	if targ>=0.45:
		pos = 112.5 + ((targ-0.45)/0.75)*37.5
	elif targ<0.45 and targ>0:
		pos = 112.5 - ((0.45-targ)/0.45)*22.5
	elif targ<=0:
		pos = 90 - abs(targ/0.3)*15
	return pos

def servo41(targ):
	if targ>=0.3:
		pos = 50 - ((targ-0.3)/0.9)*50
	elif targ<0.3 and targ>0:
		pos = 50 + ((0.3-targ)/0.3)*(50/3)
	elif targ<=0:
		pos = (200/3) + abs(targ/0.6)*(100/3)
	return pos


# LEFT FRONT
s10.moveTimeWaitWrite(servo10(armpit_lf), 500)
s12.moveTimeWaitWrite(servo12(elbow_lf), 500)
s11.moveTimeWaitWrite(servo11(knee_lf), 500)
# LEFT BACK
s30.moveTimeWaitWrite(servo20(armpit_lb), 500)
s32.moveTimeWaitWrite(servo32(elbow_lb), 500)
s31.moveTimeWaitWrite(servo31(knee_lb), 500)
# RIGHT FRONT
s20.moveTimeWaitWrite(servo20(armpit_rf), 500)
s22.moveTimeWaitWrite(servo22(elbow_rf), 500)
s21.moveTimeWaitWrite(servo21(knee_rf), 500)
# RIGHT BACK
s40.moveTimeWaitWrite(servo40(armpit_rb), 500)
s42.moveTimeWaitWrite(servo42(elbow_rb), 500)
s41.moveTimeWaitWrite(servo41(knee_rb), 500)

LX16A.moveStartAll()

time.sleep(3)

print("Servo 10: {}".format(s10.getPhysicalPos()))
print("Servo 12: {}".format(s12.getPhysicalPos()))
print("Servo 11: {}".format(s11.getPhysicalPos()))

print("Servo 30: {}".format(s30.getPhysicalPos()))
print("Servo 32: {}".format(s32.getPhysicalPos()))
print("Servo 31: {}".format(s31.getPhysicalPos()))

print("Servo 20: {}".format(s20.getPhysicalPos()))
print("Servo 22: {}".format(s22.getPhysicalPos()))
print("Servo 21: {}".format(s21.getPhysicalPos()))

print("Servo 40: {}".format(s40.getPhysicalPos()))
print("Servo 42: {}".format(s42.getPhysicalPos()))
print("Servo 41: {}".format(s41.getPhysicalPos()))