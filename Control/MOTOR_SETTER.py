from lx16a import *
import math as m
import time

# Test with pyserial for ports
# python -m serial.tools.miniterm

# Initialize the port that the controller board is connected to
# LX16A.initialize("COM3")
LX16A.initialize("/dev/ttyUSB0")

s10 = LX16A(10)
s12 = LX16A(12)
s11 = LX16A(11)

s30 = LX16A(30)
s32 = LX16A(32)
s31 = LX16A(31)

s20 = LX16A(20)
s22 = LX16A(22)
s21 = LX16A(21)

s40 = LX16A(40)
s42 = LX16A(42)
s41 = LX16A(41)


s10.moveTimeWrite(120,100)
s12.moveTimeWrite(149,100)
s11.moveTimeWrite(173,100)

s30.moveTimeWrite(120,100)
s32.moveTimeWrite(149,100)
s31.moveTimeWrite(173,100)

s20.moveTimeWrite(120,100)
s22.moveTimeWrite(90,100)
s21.moveTimeWrite(67,100)

s40.moveTimeWrite(120,100)
s42.moveTimeWrite(90,100)
s41.moveTimeWrite(67,100)


