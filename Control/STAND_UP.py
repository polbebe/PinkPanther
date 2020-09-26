from lx16a import *
import math as m
import time

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

# MOVE #1
# LEFT
# FRONT
s10.moveTimeWaitWrite(120, 500)
s12.moveTimeWaitWrite(140, 500)
s11.moveTimeWaitWrite(150, 500)
# BACK
s30.moveTimeWaitWrite(120, 500)
s32.moveTimeWaitWrite(140, 500)
s31.moveTimeWaitWrite(150, 500)
# RIGHT
# FRONT
s20.moveTimeWaitWrite(120, 500)
s22.moveTimeWaitWrite(100, 500)
s21.moveTimeWaitWrite(90, 500)
# BACK
s40.moveTimeWaitWrite(120, 500)
s42.moveTimeWaitWrite(100, 500)
s41.moveTimeWaitWrite(90, 500)

LX16A.moveStartAll()

# MOVE #2
# LEFT
# FRONT
s10.moveTimeWaitWrite(120, 500)
s12.moveTimeWaitWrite(120, 500)
s11.moveTimeWaitWrite(150, 500)
# BACK
s30.moveTimeWaitWrite(120, 500)
s32.moveTimeWaitWrite(120, 500)
s31.moveTimeWaitWrite(150, 500)
# RIGHT
# FRONT
s20.moveTimeWaitWrite(120, 500)
s22.moveTimeWaitWrite(120, 500)
s21.moveTimeWaitWrite(90, 500)
# BACK
s40.moveTimeWaitWrite(120, 500)
s42.moveTimeWaitWrite(120, 500)
s41.moveTimeWaitWrite(90, 500)

LX16A.moveStartAll()

time.sleep(1.5)

# MOVE #3
# LEFT
# FRONT
s10.moveTimeWaitWrite(120, 500)
s12.moveTimeWaitWrite(140, 500)
s11.moveTimeWaitWrite(180, 500)
# BACK
s30.moveTimeWaitWrite(120, 200)
s32.moveTimeWaitWrite(140, 200)
s31.moveTimeWaitWrite(180, 200)
# RIGHT
# FRONT
s20.moveTimeWaitWrite(120, 500)
s22.moveTimeWaitWrite(100, 500)
s21.moveTimeWaitWrite(60, 500)
# BACK
s40.moveTimeWaitWrite(120, 200)
s42.moveTimeWaitWrite(100, 200)
s41.moveTimeWaitWrite(60, 200)

LX16A.moveStartAll()