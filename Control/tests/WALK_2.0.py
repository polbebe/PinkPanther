from lx16a import *
import math as m
import time
# import pandas as pd
# import matplotlib.pyplot as plt

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

version= "0.1.0"

# Read v values from those saved from simulation
# df = pd.read_csv('V/Hardcoded_{}.csv'.format(version))
# v = df['Best Values'].to_numpy()

v = [0.1, 0, 0,
-0.2, 0.1, 0,
0.3, 0.1, 1,
0.1, 0, 0,
-0.2, -0.1, 0,
0.3, -0.1, 1,
0.1, 0, 0,
-0.2, -0.2, 0,
0.3, -0.2, 0,
0.1, 0, 0,
-0.2, 0.2, 0,
0.3, 0.2, 0,
0.1]


# Start walking
i = 0

s10.moveTimeWrite(120)
s30.moveTimeWrite(120)

s20.moveTimeWrite(120)
s40.moveTimeWrite(120)

while i<1000:
    
    # LEFT FRONT
    # Move servo 12 (elbow)
    targ12 = v[3] + v[4]*m.sin(i*v[36] + v[5])
    if targ12>=0:
        pos12 = 140 - (targ12/1.2)*65
    else:
        pos12 = (abs(targ12)/1)*25 + 140
    s12.moveTimeWrite(pos12)
    # Move servo 11 (knee)
    targ11 = v[6] + v[7]*m.sin(i*v[36] + v[8])
    if targ11>=0:
        pos11 = (targ11/1.5)*60 + 180
    else:
        pos11 = 180 - (abs(targ11)/0.6)*40
    s11.moveTimeWrite(pos11)

    # LEFT BACK
    # Move servo 32 (elbow)
    targ32 = v[21] + v[22]*m.sin(i*v[36] + v[23])
    if targ32>=0:
        pos32 = 140 - (targ32/1.2)*65
    else:
        pos32 = (abs(targ32)/1)*25 + 140
    s32.moveTimeWrite(pos32)
    # Move servo 31 (knee)
    targ31 = v[24] + v[25]*m.sin(i*v[36] + v[26])
    if targ31>=0:
        pos31 = (targ31/1.5)*60 + 180
    else:
        pos31 = 180 - (abs(targ31)/0.6)*40
    s31.moveTimeWrite(pos31)



    # RIGHT FRONT
    # Move servo 22 (elbow)
    targ22 = v[12] + v[13]*m.sin(i*v[36] + v[14])
    if targ22>=0:
        pos22 = (targ22/1.2)*65 + 100
    else:
        pos22 = 100 - (abs(targ22)/1)*25
    s22.moveTimeWrite(pos22)
    # Move servo 21 (knee)
    targ21 = v[15] + v[16]*m.sin(i*v[36] + v[17])
    if targ21>=0:
        pos21 = 60 - (targ21/1.5)*60
    else:
        pos21 = (abs(targ21)/0.6)*60 + 60
    s21.moveTimeWrite(pos21)

    # RIGHT BACK
    # Move servo 42 (elbow)
    targ42 = v[30] + v[31]*m.sin(i*v[36] + v[32])
    if targ42>=0:
        pos42 = (targ42/1.2)*65 + 100
    else:
        pos42 = 100 - (abs(targ42)/1)*25
    s42.moveTimeWrite(pos42)
    # Move servo 41 (knee)
    targ41 = v[33] + v[34]*m.sin(i*v[36] + v[35])
    if targ41>=0:
        pos41 = 60 - (targ41/1.5)*60
    else:
        pos41 = (abs(targ41)/0.6)*60 + 60
    s41.moveTimeWrite(pos41)
    
    time.sleep(1/240)

    i += 1
