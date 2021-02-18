# Detect Apriltag fiducials in Raspbery Pi camera image by iosoft.blog
import cv2
from apriltag import apriltag

import socket

import time

class CamData():
    # Constructor method
    def __init__(self, tag):
        
        self.TAG = tag
        self.MIN_MARGIN = 10

        self.k = 0
        self.xstart = 0
        self.ystart = 0
        self.currentx = 0
        self.currenty = 0

        self.cam = cv2.VideoCapture(0)
        self.detector = apriltag(TAG)

        self.ret, self.img = cam.read()
        self.greys = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.det = detector.detect(greys)
        self.rect = 0


    # Read next position in camera
    def read(self):

        if self.det["margin"] >= self.MIN_MARGIN:

            self.rect = self.det["lb-rb-rt-lt"].astype(int).reshape((-1,1,2))

            if self.k == 0:
                self.xstart = self.det["center"][0]
                self.ystart = self.det["center"][1]
                print('Start pos, x: {}, y: {}'.format(self.xstart, self.ystart))

            self.currentx = det["center"][0] - self.xstart
            self.currenty = det["center"][1] - self.ystart

            self.k += 1

            return [self.currentx, self.currenty]

if __name__ == '__main__':
    # Construct Cam object and allow use of methods
    i = CamData("tag36h11")

    while True:
        pos = i.read()
        print('x:{}, y:{}'.format(pos[0], pos[1]))