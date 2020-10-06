from lx16a import *
import math as m
import time

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


# Start walking

i = 0

while i<1000:
    
    # LEFT FRONT
    # Move servo 12 (elbow)
    targ12 = (0.2*m.sin(i*0.1))
    if targ12>=0:
        pos12 = (targ12/1.2)*54*0.9+116.4
    else:
        pos12 = 116.4-(abs(targ12)/1)*46*0.9
    s12.moveTimeWrite(pos12)
    # Move servo 11 (knee)
    targ11 = (0.2*m.sin(i*0.1))
    if targ11>=0:
        pos11 = (targ11/1.5)*71*1.2+154.8
    if targ11<0:
        pos11 = 154.8-(abs(targ11)/0.6)*29*1.2
    s11.moveTimeWrite(pos11)

    # LEFT BACK
    # Move servo 32 (elbow)
    targ32 = -(0.2*m.sin(i*0.1))
    if targ32>=0:
        pos32 = (targ32/1.2)*54*0.9+116.4
    else:
        pos32 = 116.4-(abs(targ32)/1)*46*0.9
    s32.moveTimeWrite(pos32)
    # Move servo 31 (knee)
    targ31 = -(0.2*m.sin(i*0.1))
    if targ31>=0:
        pos31 = (targ31/1.5)*71*1.2+154.8
    else:
        pos31 = 154.8-(abs(targ31)/0.6)*29*1.2
    s31.moveTimeWrite(pos31)


    #!!! Different from LEFT !!!#

    # RIGHT FRONT
    # Move servo 22 (elbow)
    targ22 = (0.2*m.sin(i*0.1))
    if targ22<0:
        pos22 = (targ22/1.2)*54*0.9+116.4
    else:
        pos22 = 116.4-(abs(targ22)/1)*46*0.9
    s22.moveTimeWrite(pos22)
    # Move servo 21 (knee)
    targ21 = (0.2*m.sin(i*0.1))
    if targ21>=0:
        pos21 = (targ21/1.5)*71*1.2+85.2
    else:
        pos21 = 85.2-(abs(targ21)/0.6)*29*1.2
    s21.moveTimeWrite(pos21)

    # RIGHT BACK
    # Move servo 42 (elbow)
    targ42 = -(0.2*m.sin(i*0.1))
    if targ42<0:
        pos42 = (targ42/1.2)*54*0.9+116.4
    else:
        pos42 = 116.4-(abs(targ42)/1)*46*0.9
    s42.moveTimeWrite(pos42)
    # Move servo 41 (knee)
    targ41 = -(0.2*m.sin(i*0.1))
    if targ41>=0:
        pos41 = (targ41/1.5)*71*1.2+85.2
    else:
        pos41 = 85.2-(abs(targ41)/0.6)*29*1.2
    s41.moveTimeWrite(pos41)
    
    time.sleep(1/240)
    print(i)
    i += 1
