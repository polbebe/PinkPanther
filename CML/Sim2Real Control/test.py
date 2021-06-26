import numpy as np

# SIM 2 REAL
def servo_left_shoulder_sim2real(targ):
	if targ>=0:
		pos = (621 - (targ/1.2)*(621-290))
	else:
		pos = (621 + (abs(targ)/0.3)*(688-621))
	return int(round(pos))
def servo_left_elbow_sim2real(targ):
	if targ>=0:
		pos = (721 + (targ/1.2)*(1000-721))
	else:
		pos = (721 - (abs(targ)/0.9)*(721-500))
	return int(round(pos))

def servo_right_shoulder_sim2real(targ):
	if targ>=0:
		pos = (375 + (targ/1.2)*(700-375))
	else:
		pos = (375 - (abs(targ)/0.3)*(375-313))
	return int(round(pos))
def servo_right_elbow_sim2real(targ):
	if targ>=0:
		pos = (279 - (targ/1.2)*(279-0))
	else:
		pos = (279 + (abs(targ)/0.9)*(500-279))
	return int(round(pos))

# Call corresponding function to convert sim2real
def transformMotors(pos):
	null = lambda x: 0
	fns =	[null, servo_left_elbow_sim2real, servo_left_shoulder_sim2real, null, servo_right_elbow_sim2real, servo_right_shoulder_sim2real, 
			null, servo_left_elbow_sim2real, servo_left_shoulder_sim2real, null, servo_right_elbow_sim2real, servo_right_shoulder_sim2real]
	targ = np.zeros(12)
	for i in range(len(pos)):
		targ[i] = fns[i](pos[i])
	return targ

print(transformMotors([ 0., 0.00483506, 0.00483506, 0., -0.00483506, -0.00483506, 0., -0.00483506, -0.00483506, 0., 0.00483506, 0.00483506]))
print(servo_left_elbow_sim2real(0.00483506))



