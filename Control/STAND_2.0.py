from lx16a import *
import math as m
import time

# Initialize the port that the controller board is connected to
LX16A.initialize("COM3")

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








# LEFT
# BACK
s30.moveTimeWrite(120, 100)

targ32 = -0.2
if targ32>=0:
	pos32 = 140 - (targ32/1.2)*65
else:
	pos32 = (abs(targ32)/1)*25 + 140
s32.moveTimeWrite(pos32, 100)




# LEFT
# BACK
targ31 = 0.3
if targ31>=0:
	pos31 = (targ31/1.5)*60 + 180
else:
	pos31 = 180 - (abs(targ31)/0.6)*40
s31.moveTimeWrite(pos31)



# RIGHT
# BACK
s40.moveTimeWrite(120, 100)

targ42 = -0.2
if targ42>=0:
	pos42 = (targ42/1.2)*65 + 100
else:
	pos42 = 100 - (abs(targ42)/1)*25
s42.moveTimeWrite(pos42, 100)


# RIGHT
# BACK
targ41 = 0.3
if targ41>=0:
	pos41 = 60 - (targ41/1.5)*60
else:
	pos41 = (abs(targ41)/0.6)*60 + 60
s41.moveTimeWrite(pos41)


time.sleep(3)


# LEFT
# FRONT
s10.moveTimeWrite(120, 100)

targ12 = -0.2
if targ12>=0:
	pos12 = 140 - (targ12/1.2)*65
else:
	pos12 = (abs(targ12)/1)*25 + 140
s12.moveTimeWrite(pos12, 100)

# LEFT
# FRONT
targ11 = 0.3
if targ11>=0:
	pos11 = (targ11/1.5)*60 + 180
else:
	pos11 = 180 - (abs(targ11)/0.6)*40
s11.moveTimeWrite(pos11, 100)




# RIGHT
# FRONT
s20.moveTimeWrite(120, 100)

targ22 = -0.2
if targ22>=0:
	pos22 = (targ22/1.2)*65 + 100
else:
	pos22 = 100 - (abs(targ22)/1)*25
s22.moveTimeWrite(pos22, 100)


# RIGHT
# FRONT
targ21 = 0.3
if targ21>=0:
	pos21 = 60 - (targ21/1.5)*60
else:
	pos21 = (abs(targ21)/0.6)*60 + 60
s21.moveTimeWrite(pos21, 100)

# LEFT
# BACK
targ31 = 0.3
if targ31>=0:
	pos31 = (targ31/1.5)*60 + 180
else:
	pos31 = 180 - (abs(targ31)/0.6)*40
s31.moveTimeWrite(pos31)



# RIGHT
# BACK
s40.moveTimeWrite(120, 100)

targ42 = -0.2
if targ42>=0:
	pos42 = (targ42/1.2)*65 + 100
else:
	pos42 = 100 - (abs(targ42)/1)*25
s42.moveTimeWrite(pos42, 100)


# RIGHT
# BACK
targ41 = 0.3
if targ41>=0:
	pos41 = 60 - (targ41/1.5)*60
else:
	pos41 = (abs(targ41)/0.6)*60 + 60
s41.moveTimeWrite(pos41)