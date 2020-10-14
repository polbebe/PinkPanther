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

# Initialize socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	# Connect to network
	s.connect((HOST, PORT))

	# Motor Inputs array
	motor_inputs = np.zeros(12, dtype=np.float32)

	# Start walking
	while True:
		# Calculate motor_inputs
        #motor_inputs[0] = 0
        motor_inputs[1] = s12.getPhysicalPos() #- x.getVirtualPos()
        motor_inputs[2] = s11.getPhysicalPos() #- x.getVirtualPos()
        #motor_inputs[3] = 0
        motor_inputs[4] = s22.getPhysicalPos() #- x.getVirtualPos()
        motor_inputs[5] = s21.getPhysicalPos() #- x.getVirtualPos()
        #motor_inputs[6] = 0
        motor_inputs[7] = s32.getPhysicalPos() #- x.getVirtualPos()
        motor_inputs[8] = s31.getPhysicalPos() #- x.getVirtualPos()
        #motor_inputs[9] = 0
        motor_inputs[10] = s42.getPhysicalPos() #- x.getVirtualPos()
        motor_inputs[11] = s41.getPhysicalPos() #- x.getVirtualPos()
        # Send motor inputs to server
		s.sendall(motor_inputs.tobytes())
		
		# Get position data from server
		p = s.recv(1024)
		pos = np.frombuffer(p, dtype=np.float32)
		# If there's no more data break the loop
		if not pos:
			break
		# Move all servos to their corresponding position
		s10.moveTimeWrite(130)
		# LEFT FRONT
		# Move servo 12 (elbow)
		s12.moveTimeWrite(pos[1]) #print(pos[1])
		# Move servo 11 (knee)
		s11.moveTimeWrite(pos[2]) #print(pos[2])
		# LEFT BACK
		# Move servo 32 (elbow)
		s32.moveTimeWrite(pos[7]) #print(pos[7])
		# Move servo 31 (knee)
		s31.moveTimeWrite(pos[8]) #print(pos[8])
		# RIGHT FRONT
		# Move servo 22 (elbow)
		s22.moveTimeWrite(pos[4]) #print(pos[4])
		# Move servo 21 (knee)
		s21.moveTimeWrite(pos[5]) #print(pos[5])
		# RIGHT BACK
		# Move servo 42 (elbow)
		s42.moveTimeWrite(pos[10]) #print(pos[10])
		# Move servo 41 (knee)
		s41.moveTimeWrite(pos[11]) #print(pos[11])

		time.sleep(0.001)


time.sleep(0.1)


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

