# Detect Apriltag fiducials in Raspbery Pi camera image by iosoft.blog
import cv2
from apriltag import apriltag

import socket

import time

class CamData():
    # Constructor method
    def __init__(self):
        
        self.TAG = "tag36h11"
        self.MIN_MARGIN = 10

        self.k = 0
        self.xstart = 0
        self.ystart = 0
        self.currentx = 0
        self.currenty = 0

        self.cam = cv2.VideoCapture(0)
        self.detector = apriltag(self.TAG)

        self.ret, self.img = self.cam.read()
        self.greys = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.dets = self.detector.detect(self.greys)
        self.rect = 0


    # Read next position in camera
    def read(self):
        for det in self.dets:
            if det["margin"] >= self.MIN_MARGIN:

                self.rect = det["lb-rb-rt-lt"].astype(int).reshape((-1,1,2))

                if self.k == 0:
                    self.xstart = det["center"][0]
                    self.ystart = det["center"][1]
                    print('Start pos, x: {}, y: {}'.format(self.xstart, self.ystart))

                self.currentx = det["center"][0] - self.xstart
                self.currenty = det["center"][1] - self.ystart

                self.k += 1

                return [self.currentx, self.currenty]

if __name__ == '__main__':
    # Construct Cam object and allow use of methods
    i = CamData()

    while True:
        pos = i.read()
        #print(pos)