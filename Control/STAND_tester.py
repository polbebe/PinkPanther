from lx16a import *
import math as m
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

armpit_lb=-0.6
elbow_lb=1.2
knee_lb=-0.6

armpit_rb=0.6
elbow_rb=1
knee_rb=-0.6


# Simulation 2 Reality converter functions
def servo12(targ12):
    if targ12>=0:
        pos12 = 140 - (targ12/1.2)*65
    else:
        pos12 = (abs(targ12)/1)*25 + 140
    return pos12

def servo11(targ11):
    if targ11>=0:
        pos11 = (targ11/1.5)*60 + 180
    else:
        pos11 = 180 - (abs(targ11)/0.6)*40
    return pos11

def servo32(targ32):
    if targ32>=0:
        pos32 = 140 - (targ32/1.2)*65
    else:
        pos32 = (abs(targ32)/1)*25 + 140
    return pos32

def servo31(targ31):
    if targ31>=0:
        pos31 = (targ31/1.5)*60 + 180
    else:
        pos31 = 180 - (abs(targ31)/0.6)*40
    return pos31

def servo22(targ22):
    if targ22>=0:
        pos22 = (targ22/1.2)*65 + 100
    else:
        pos22 = 100 - (abs(targ22)/1)*25
    return pos22

def servo21(targ21):
    if targ21>=0:
        pos21 = 60 - (targ21/1.5)*60
    else:
        pos21 = (abs(targ21)/0.6)*60 + 60
    return pos21

def servo42(targ42):
    if targ42>=0:
        pos42 = (targ42/1.2)*65 + 100
    else:
        pos42 = 100 - (abs(targ42)/1)*25
    return pos42

def servo41(targ41):
    if targ41>=0:
        pos41 = 60 - (targ41/1.5)*60
    else:
        pos41 = (abs(targ41)/0.6)*60 + 60
    return pos41


# LEFT FRONT
s10.moveTimeWaitWrite(120, 500)
s12.moveTimeWaitWrite(servo12(elbow_lf), 500)
s11.moveTimeWaitWrite(servo11(knee_lf), 500)
# LEFT BACK
s30.moveTimeWaitWrite(120, 200)
s32.moveTimeWaitWrite(servo32(elbow_lb), 200)
s31.moveTimeWaitWrite(servo31(knee_lb), 200)
# RIGHT FRONT
s20.moveTimeWaitWrite(120, 500)
s22.moveTimeWaitWrite(servo22(elbow_rf), 500)
s21.moveTimeWaitWrite(servo21(knee_rf), 500)
# RIGHT BACK
s40.moveTimeWaitWrite(120, 200)
s42.moveTimeWaitWrite(servo42(elbow_rb), 200)
s41.moveTimeWaitWrite(servo41(knee_rb), 200)

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