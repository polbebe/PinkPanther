from lx16a import *
import math as m
import time
import numpy

# Initialize the port that the controller board is connected to
# LX16A.initialize("COM3")
LX16A.initialize("/dev/ttyUSB0")


s = LX16A(30)

s.angleLimitWrite(100, 140)


s.moveTimeWrite(140, 500)

time.sleep(3)

print("Servo 30: {}".format(s.getPhysicalPos()))