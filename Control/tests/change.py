from lx16a import *
import math as m
import time

# Test with pyserial for ports
# python -m serial.tools.miniterm

# Initialize the port that the controller board is connected to
# LX16A.initialize("COM3")
LX16A.initialize("/dev/ttyUSB0")

# Initialize ALL servos
# Front Left
s10 = LX16A(10)
s12 = LX16A(12)
s11 = LX16A(11)

# Front Right
s20 = LX16A(20)
s22 = LX16A(22)
s21 = LX16A(21)

# Back Left
s30 = LX16A(30)
s32 = LX16A(32)
s31 = LX16A(31)

# Back Right
s40 = LX16A(40)
s42 = LX16A(42)
s41 = LX16A(41)

s10.moveTimeWaitWrite(125, 1000)


LX16A.moveStartAll()
# LX16A.moveStopAll()