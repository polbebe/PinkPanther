# Detect Apriltag fiducials in Raspbery Pi camera image by iosoft.blog
import cv2
from apriltag import apriltag

import socket

import time

class CamData():
    # Constructor method
    def __init__(self):
 
        self.TITLE      = "apriltag_view"  # Window title
        self.TAG        = "tag36h11"        # Tag family, tag16h5, tag36h11
        self.MIN_MARGIN = 10               # Filter value for tag detection
        self.FONT       = cv2.FONT_HERSHEY_SIMPLEX  # Font for ID value
        self.RED        = 0,0,255          # Colour of ident & frame (BGR)

        self.k = 0
        self.x0 = 0
        self.y0 = 0

        self.cam = cv2.VideoCapture(0)
        self.detector = apriltag(self.TAG)

    def frame(self):
        #cam = cv2.VideoCapture(0)
        #detector = apriltag(self.TAG)
        while True:
            ret, img = self.cam.read()
            greys = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            dets = self.detector.detect(greys)
            for det in dets:
                if det["margin"] >= self.MIN_MARGIN:
                    rect = det["lb-rb-rt-lt"].astype(int).reshape((-1,1,2))
                    cv2.polylines(img, [rect], True, self.RED, 2)
                    ident = str(det["id"])
                    pos = det["center"].astype(int) + (-10,10)
                    cv2.putText(img, ident, tuple(pos), self.FONT, 1, self.RED, 2)
                    if self.k == 0:
                        self.x0 = det["center"][0]
                        self.y0 = det["center"][1]
                        print('Start pos, x: {}, y: {}'.format(self.x0, self.y0))
                    deltax = det["center"][0] - self.x0
                    deltay = det["center"][1] - self.y0
                    print("Tag %s: x: %6.1f, y: %6.1f" % (det["id"], deltax, deltay))
                    self.k += 1
            cv2.imshow(self.TITLE, img)
        cv2.destroyAllWindows()

if __name__=='__main__':
    i = CamData()

    i.frame()