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
        
        #
        self.TITLE = "apriltag_view"
        self.FONT = cv2.FONT_HERSHEY_SIMPLEX
        self.RED = 0,0,255
        #

        self.cam = cv2.VideoCapture(0)
        self.detector = apriltag(self.TAG)

        self.k = 0
        self.x0 = 0
        self.y0 = 0

        self.ret, self.img = self.cam.read()
        self.greys = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.dets = self.detector.detect(self.greys)

    # Read next position in camera
    def read(self):

        for det in self.dets:
            if det["margin"] >= self.MIN_MARGIN:

                rect = det["lb-rb-rt-lt"].astype(int).reshape((-1,1,2))
                cv2.polylines(self.img, [rect], True, RED, 2)
                ident = str(det["id"])
                pos = det["center"].astype(int) + (-10,10)
                cv2.putText(self.img, ident, tuple(pos), self.FONT, 1, self.RED, 2)

                if self.k == 0:
                    self.x0 = det["center"][0]
                    self.y0 = det["center"][1]
                    print('Start pos, x: {}, y: {}'.format(self.x0, self.y0))

                deltax = det["center"][0] - self.x0
                deltay = det["center"][1] - self.y0

                self.k += 1

                return [deltax, deltay]

if __name__ == '__main__':
    # Construct Cam object and allow use of methods
    i = CamData()
    print('Started...')

    while True:
        pos = i.read()
        print(pos)