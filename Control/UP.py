from lx16a import *
import math as m
import time
import matplotlib.pyplot as plt

# Initialize the port that the controller board is connected to
# LX16A.initialize("COM3")
LX16A.initialize("/dev/ttyUSB0")

# Initialize ALL servos & write their angle limits (only once is enough)
# LEFT
# FRONT
s10 = LX16A(10)
s12 = LX16A(12)
s11 = LX16A(11)
#s10.angleLimitWrite(100,140)
#s12.angleLimitWrite(75, 165)
#s11.angleLimitWrite(120, 240)
# BACK
s30 = LX16A(30)
s32 = LX16A(32)
s31 = LX16A(31)
#s30.angleLimitWrite(100,140)
#s32.angleLimitWrite(75, 165)
#s31.angleLimitWrite(120, 240)

# RIGHT
# FRONT
s20 = LX16A(20)
s22 = LX16A(22)
s21 = LX16A(21)
#s20.angleLimitWrite(100,140)
#s22.angleLimitWrite(75, 165)
#s21.angleLimitWrite(0, 120)
# BACK
s40 = LX16A(40)
s42 = LX16A(42)
s41 = LX16A(41)
#s40.angleLimitWrite(100,140)
#s42.angleLimitWrite(75, 165)
#s41.angleLimitWrite(0, 120)


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



s12.moveTimeWaitWrite(servo12(-0.2), 400)
s11.moveTimeWaitWrite(servo11(0.3), 400)

s32.moveTimeWaitWrite(servo32(-0.2), 400)
s31.moveTimeWaitWrite(servo31(0.3), 400)

s22.moveTimeWaitWrite(servo22(-0.2), 400)
s21.moveTimeWaitWrite(servo21(0.3), 400)

s42.moveTimeWaitWrite(servo42(-0.2), 400)
s41.moveTimeWaitWrite(servo41(0.3), 400)

LX16A.moveStartAll()