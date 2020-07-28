from lx16a import *
import math as m
import time

# Initialize the port that the controller board is connected to
LX16A.initialize("COM3")

# Initialize 2 servos
elbow = LX16A(12)
knee = LX16A(11)

# knee.angleLimitWrite(20,240)
# elbow.angleLimitWrite(90,240)

i = 0

while i<1000:
	
	el = (0.2*m.sin(i*0.1))
	if el>=0:
		elbow_pos = (el/1.2)*54*1.5+159
	else:
		elbow_pos = 159-abs(el)*46*1.5

	elbow.moveTimeWrite(elbow_pos)


	kn = (0.2*m.sin(i*0.1))
	if kn>=0:
		knee_pos = (kn/1.5)*71*2.2+83.8
	if kn<0:
		knee_pos = 83.8-(abs(kn)/0.6)*29*2.2

	knee.moveTimeWrite(knee_pos)
	
	time.sleep(1/240)
	print(i)
	i += 1