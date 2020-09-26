from lx16a import *
import math as m
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Initialize the port that the controller board is connected to
# LX16A.initialize("COM3")
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

version= "0.2.1"

# Read v values from those saved from simulation
df = pd.read_csv('V/Hardcoded_{}.csv'.format(version))
v = np.array(df['Best Values'])


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


# Start walking
i = 0

while i<400:
    
    s10.moveTimeWrite(130)
    
    # LEFT FRONT
    # Move servo 12 (elbow)
    s12.moveTimeWrite(servo12(v[3] + v[4]*m.sin(i*v[36] + v[5])))
    # Move servo 11 (knee)
    s11.moveTimeWrite(servo11(v[6] + v[7]*m.sin(i*v[36] + v[8])))

    # LEFT BACK
    # Move servo 32 (elbow)
    s32.moveTimeWrite(servo32(v[21] + v[22]*m.sin(i*v[36] + v[23])))
    # Move servo 31 (knee)
    s31.moveTimeWrite(servo31(v[24] + v[25]*m.sin(i*v[36] + v[26])))

    # RIGHT FRONT
    # Move servo 22 (elbow)
    s22.moveTimeWrite(servo22(v[12] + v[13]*m.sin(i*v[36] + v[14])))
    # Move servo 21 (knee)
    s21.moveTimeWrite(servo21(v[15] + v[16]*m.sin(i*v[36] + v[17])))

    # RIGHT BACK
    # Move servo 42 (elbow)
    s42.moveTimeWrite(servo42(v[30] + v[31]*m.sin(i*v[36] + v[32])))
    # Move servo 41 (knee)
    s41.moveTimeWrite(servo41(v[33] + v[34]*m.sin(i*v[36] + v[35])))
    
    i += 1


time.sleep(0.1)

s10.moveTimeWaitWrite(120, 1400)
s12.moveTimeWaitWrite(120, 1400)
s11.moveTimeWaitWrite(120, 1400)

s32.moveTimeWaitWrite(120, 1400)
s31.moveTimeWaitWrite(120, 1400)

s22.moveTimeWaitWrite(120, 1400)
s21.moveTimeWaitWrite(120, 1400)

s42.moveTimeWaitWrite(120, 1400)
s41.moveTimeWaitWrite(120, 1400)

LX16A.moveStartAll()