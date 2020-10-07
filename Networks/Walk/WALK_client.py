#!/usr/bin/env python3
import socket
import numpy as np
from lx16a import *
import math as m
import time

# The server's hostname or IP address
HOST = '192.168.1.29'
# The port used by the server
PORT = 65432
'''
# Initialize the port that the controller board is connected to
LX16A.initialize("/dev/ttyUSB0")
# Initialize Servo controls
# LEFT
# FRONT
s10 = LX16A(10)
s12 = LX16A(12)
s11 = LX16A(11)
# BACK
s30 = LX16A(30)
s32 = LX16A(32)
s31 = LX16A(31)
# RIGHT
# FRONT
s20 = LX16A(20)
s22 = LX16A(22)
s21 = LX16A(21)
# BACK
s40 = LX16A(40)
s42 = LX16A(42)
s41 = LX16A(41)
'''
# Initialize socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	# Connect to network
	s.connect((HOST, PORT))

	# Check message
	check = np.arange(1, dtype=np.float32)
	check_data = check.tobytes()

	# Start walking
	while True:
		s.sendall(check_data)
		# Get position data from server
		pos_data = s.recv(1024)
		pos = np.frombuffer(pos_data, dtype=np.float32)
		# If there's no more data break the loop
		if not pos_data:
			break
		# Move all servos to their corresponding position
		# LEFT FRONT
		# Move servo 12 (elbow)
		#s12.moveTimeWrite(pos[1])
		print(pos[1])
		# Move servo 11 (knee)
		#s11.moveTimeWrite(pos[2])
		print(pos[2])
		# LEFT BACK
		# Move servo 32 (elbow)
		#s32.moveTimeWrite(pos[7])
		print(pos[7])
		# Move servo 31 (knee)
		#s31.moveTimeWrite(pos[8])
		print(pos[8])
		# RIGHT FRONT
		# Move servo 22 (elbow)
		#s22.moveTimeWrite(pos[4])
		print(pos[4])
		# Move servo 21 (knee)
		#s21.moveTimeWrite(pos[5])
		print(pos[5])
		# RIGHT BACK
		# Move servo 42 (elbow)
		#s42.moveTimeWrite(pos[10]
		print(pos[10])
		# Move servo 41 (knee)
		#s41.moveTimeWrite(pos[11]
		print(pos[11])
		
		time.sleep(0.01)


time.sleep(0.1)

'''
# Slow plas
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
'''
