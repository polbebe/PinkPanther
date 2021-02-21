# Detect Apriltag fiducials in Raspbery Pi camera image by iosoft.blog
# Object oriented implementation with threading by polbebe

import cv2
from apriltag import apriltag

import socket
import sys
import time

class CamData():
	# Constructor method
	def __init__(self):
		# Tag Family & Filter value for detection
		self.TAG        = "tag36h11"
		self.MIN_MARGIN = 10

		# Initialize counter and previous x,y location for delta pos calculations
		self.k = 0
		self.x0 = 0
		self.y0 = 0

		# Access camera and use apriltags library to detect the fiducial
		self.cam = cv2.VideoCapture(0)
		self.detector = apriltag(self.TAG)

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
					print('Start pos, x: {}, y: {}'.format(self.x0, self.y0))

				# Calculate delta pos
				deltax = det["center"][0] - self.x0
				deltay = det["center"][1] - self.y0

				# Keep track of previous pos
				self.x0 = det["center"][0]
				self.y0 = det["center"][1]

				k += 1
				return [deltax, deltay]


if __name__=='__main__':
	# Construct CAM object and allow use of methods
	i = CamData()

	# UNIT TEST
	# Count actions/second
	start = time.time()
	j = 0

	while True:
		# Get delta pos of robot at each frame
		a = i.frame()
		if a != None:
			print(a)
			# Print actions/second
			sys.stdout.write(str(j)+' in: '+str(round(time.time()-start,3))+' Averaging: '+str(round(j/(time.time()-start),2))+' actions/s\r')
		j += 1
