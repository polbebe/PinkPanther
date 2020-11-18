from lx16a import *
import math as m
import time

# Test with pyserial for ports
# python -m serial.tools.miniterm

# Initialize the port that the controller board is connected to
# LX16A.initialize("COM3")
LX16A.initialize("/dev/ttyUSB0")

s10 = LX16A(10)
s20 = LX16A(20)
s30 = LX16A(30)
s40 = LX16A(40)

s10.moveTimeWrite(120,0)
s20.moveTimeWrite(120,0)
s30.moveTimeWrite(120,0)
s40.moveTimeWrite(120,0)