#!/usr/bin/env python3
import socket
import numpy as np
import pandas as pd
import math as m
import time
import sys

HOST = '192.168.1.29'   # Standard loopback interface address (localhost)
						# Mac - 192.168.1.29
PORT = 65432            # Port to listen on (non-privileged ports are > 1023)

# Functions for servo position conversion
def servo12(targ12):
	if targ12>=0:
		pos12 = (140 - (targ12/1.2)*65)*(25/6)
	else:
		pos12 = ((abs(targ12)/1)*25 + 140)*(25/6)
	return int(round(pos12))
def servo11(targ11):
	if targ11>=0:
		pos11 = ((targ11/1.5)*60 + 180)*(25/6)
	else:
		pos11 = (180 - (abs(targ11)/0.6)*40)*(25/6)
	return int(round(pos11))
def servo32(targ32):
	if targ32>=0:
		pos32 = (140 - (targ32/1.2)*65)*(25/6)
	else:
		pos32 = ((abs(targ32)/1)*25 + 140)*(25/6)
	return int(round(pos32))
def servo31(targ31):
	if targ31>=0:
		pos31 = ((targ31/1.5)*60 + 180)*(25/6)
	else:
		pos31 = (180 - (abs(targ31)/0.6)*40)*(25/6)
	return int(round(pos31))
def servo22(targ22):
	if targ22>=0:
		pos22 = ((targ22/1.2)*65 + 100)*(25/6)
	else:
		pos22 = (100 - (abs(targ22)/1)*25)*(25/6)
	return int(round(pos22))
def servo21(targ21):
	if targ21>=0:
		pos21 = (60 - (targ21/1.5)*60)*(25/6)
	else:
		pos21 = ((abs(targ21)/0.6)*60 + 60)*(25/6)
	return int(round(pos21))
def servo42(targ42):
	if targ42>=0:
		pos42 = ((targ42/1.2)*65 + 100)*(25/6)
	else:
		pos42 = (100 - (abs(targ42)/1)*25)*(25/6)
	return int(round(pos42))
def servo41(targ41):
	if targ41>=0:
		pos41 = (60 - (targ41/1.5)*60)*(25/6)
	else:
		pos41 = ((abs(targ41)/0.6)*60 + 60)*(25/6)
	return int(round(pos41))

version= "0.2.1"

# Read v values from those saved from simulation
df = pd.read_csv('V/Hardcoded_{}.csv'.format(version))
v = np.array(df['Best Values'], dtype=np.float32)
# Create positons array that will be calculated on each step
# and sent to client
pos = np.zeros(12, dtype=np.float32)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	# Create network connection
	s.bind((HOST, PORT))
	# Wait for client to connect
	s.listen()
	# Once client connects - get client's information
	conn, addr = s.accept()
	# What to do with 
	with conn:
		print('Connected by: ', addr)
		i = 0
		max_time = 400
		start = time.time()
		while i<max_time:
			# Receive connection from client
			data = conn.recv(1024)
			# Calculate servo positions
			#pos[0] = 0
			pos[1] = servo12(v[3] + v[4]*m.sin(i*v[36] + v[5]))
			pos[2] = servo11(v[6] + v[7]*m.sin(i*v[36] + v[8]))
			#pos[3] = 0
			pos[4] = servo22(v[12] + v[13]*m.sin(i*v[36] + v[14]))
			pos[5] = servo21(v[15] + v[16]*m.sin(i*v[36] + v[17]))
			#pos[6] = 0
			pos[7] = servo32(v[21] + v[22]*m.sin(i*v[36] + v[23]))
			pos[8] = servo31(v[24] + v[25]*m.sin(i*v[36] + v[26]))
			#pos[9] = 0
			pos[10] = servo42(v[30] + v[31]*m.sin(i*v[36] + v[32]))
			pos[11] = servo41(v[33] + v[34]*m.sin(i*v[36] + v[35]))
			# Prepare and send position data to client
			pos_data = pos.tobytes()
			conn.sendall(pos_data)
			# Calculate the actions/second
			sys.stdout.write(str(i)+' in: '+str(round(time.time()-start,3))+' Averaging: '+str(round(i/(time.time()-start),2))+' actions/s\r')
			i += 1
		print(str(i)+' in: '+str(round(time.time()-start,3))+' Averaging: '+str(round(i/(time.time()-start),2))+' actions/s')


