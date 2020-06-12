from lx16a import *
import math as m
import time

# Initialize the port that the controller board is connected to
LX16A.initialize("COM3")

# Initialize 2 servos
elbow = LX16A(12)
knee = LX16A(11)

# knee.angleLimitWrite(20,240)
# shoulder.angleLimitWrite(90,240)

i = 0

v = [0.09366486193742063, -0.3910298281777823, -0.38048775348185426,
	 0.3533151448874734, 0.40102390766150287, -0.48292162810047734,
	 -0.48226864217303356, 0.12424497460368811, -0.2594928275420473,
	 -0.4998096572544207, -0.3108416532536089, -0.4172196785824154]

while i<1000:
	
	el = (v[0]+v[1]*m.sin(i*0.1+v[2]))
	if el>=0:
		elbow_pos = (el/1.2)*54*1.5+159
	else:
		elbow_pos = 159-abs(el)*46*1.5

	elbow.moveTimeWrite(elbow_pos)


	kn = (v[6]+v[7]*m.sin(i*0.1+v[8]))
	if kn>=0:
		knee_pos = (kn/1.5)*71*2.2+83.8
	if kn<0:
		knee_pos = 83.8-(abs(kn)/0.6)*29*2.2

	knee.moveTimeWrite(knee_pos)
	
	time.sleep(1/240)
	print(i)
	i += 1