import numpy as np
import csv

def write_csv(data):
		with open('test_1.csv', 'a') as outfile:
			writer = csv.writer(outfile)
			writer.writerow(data)

a = -0.57472189
b = -0.97479314
c = 0.04835059


def movement(a, b, c, t):
	v = a * np.sin(t * b) + c
	return v


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

def nothing(targ):
	return 500

positive = [1, 10, 2, 11]
negative = [4, 7, 5, 8]
zero = [0, 3, 6, 9]
desired_p_sim = np.zeros(12)
desired_p_real = np.zeros(12)

fns = [	nothing, servo_left_elbow_sim2real, servo_left_shoulder_sim2real, nothing, servo_right_elbow_sim2real, servo_right_shoulder_sim2real,
		nothing, servo_left_elbow_sim2real, servo_left_shoulder_sim2real, nothing, servo_right_elbow_sim2real, servo_right_shoulder_sim2real	]

t=0
while t<200:
	
	desired_p_sim[positive] = movement(a,b,c,t)
	desired_p_sim[negative] = -movement(a,b,c,t)
	desired_p_sim[zero] = 0
	for i in range(12):
		desired_p_real[i] = fns[i](desired_p_sim[i])

	write_csv(desired_p_real)

	t+=1


