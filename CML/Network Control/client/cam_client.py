# Detect Apriltag fiducials in Raspbery Pi camera image by iosoft.blog
# Object oriented implementation with multi-socket threading by polbebe

import cv2
from apriltag import apriltag

import socket

import sys
import time
import numpy as np
import math as m

class CamData():
	# Constructor method
	def __init__(self):
		# Tag Family & Filter value for detection
		self.TAG        = "tag36h11"
		self.MIN_MARGIN = 10
		# Socket Conneciton
		HOST = '192.168.1.29'
		PORT = 65432
		self.socket = True

		# Initialize counter and previous x,y location for delta pos calculations
		self.k = 0
		self.x0 = 0
		self.y0 = 0

		# Access camera and use apriltags library to detect the fiducial
		self.cam = cv2.VideoCapture(0)
		self.detector = apriltag(self.TAG)

		# Connect to Socket set up by server
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.s.connect((HOST, PORT))
		except socket.error as e:
			print(str(e))

	# Analysis of one frame
	def frame(self):
		# Read frame and detect apriltag
		
		ret, img = self.cam.read()
		greys = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		dets = self.detector.detect(greys)

		# For all detected apriltags
		for det in dets:
			# If filtered for detection
			if det["margin"] >= self.MIN_MARGIN:
				# Calculate x,y
				rect = det["lb-rb-rt-lt"].astype(int).reshape((-1,1,2))
				pos = det["center"].astype(int) + (-10,10)

				# Initial position
				if self.k == 0:
					self.x0 = det["center"][0]
					self.y0 = det["center"][1]

				# Calculate delta pos
				deltax = det["center"][0] - self.x0
				deltay = det["center"][1] - self.y0

				# Keep track of previous pos
				self.x0 = det["center"][0]
				self.y0 = det["center"][1]

				self.k += 1

				print([deltax, deltay])
				
				return [deltax, deltay]

	# Step
	def step(self):
		# Receive new servo positions to be taken
		
		p = self.s.recv(1024)
		# If there's no more data being received, break the loop
		if not p:
			print('CONNECTION BROKEN')
			self.socket = False
		# Get current state of robot
		f = self.frame()
		# Break connection by sending NaN if apriltag is not discoverable
		if f == None:
			self.socket = False
			f = m.nan
		# Send current state of robot
		self.s.sendall(np.array(f, dtype=np.float32).tobytes())

	# Check whether socket should still be running
	def is_true(self):
		return self.socket


if __name__=='__main__':
	# Construct CAM object and allow use of methods
	client = CamData()

	while client.is_true() == True:
		# Get next frame
		client.step()

