from lx16a import *
from math import sin, cos

# This is the port that the controller board is connected to
# This will be different for different computers
# On Windows, try the ports COM1, COM2, COM3, etc...
# On Raspbian, try each port in /dev/

# To test:
# import serial.tools.list_ports
# print(serial.tools.list_ports.comports())
LX16A.initialize("COM3")

# There should two servos connected, with IDs 1 and 2
servo1 = LX16A(11)
servo2 = LX16A(12)

t = 0

while True:
	# Two sine waves out of phase
	# The servos can rotate between 0 and 240 degrees,
	# So we adjust the waves to be in that range
	servo1.moveTimeWrite(sin(t) * 10 + 120)
	servo2.moveTimeWrite(cos(t) * 10 + 120)
	
	t += 0.01
