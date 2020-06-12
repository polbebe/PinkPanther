from lx16a import *
import math as m
import time

# Initialize the port that the controller board is connected to
LX16A.initialize("COM3")

# Instantiate servos
knee = LX16A(11)
elbow = LX16A(12)

# Movement limits
# knee.angleLimitWrite(20,240)
# elbow.angleLimitWrite(90,240)

# Test move
elbow.moveTimeWaitWrite(100,1000)
time.sleep(2)
elbow.moveStart()





