import numpy as np

a = 0.9
b = 0.1
c = 0.3

def movement(a, b, c, t):
	v = a * np.sin(t * b) + c
	return v


def servo_left_elbow_sim2real(targ11):
	if targ11>=0:
		pos11 = (721 + (targ11/1.2)*(1000-721))
	else:
		pos11 = (721 - (abs(targ11)/0.6)*(721-500))
	return int(round(pos11))

t=0
while t<300:
	print(int(servo_left_elbow_sim2real(movement(a,b,c,t))))
	t+=1