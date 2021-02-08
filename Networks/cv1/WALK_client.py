#!/usr/bin/env python3
import socket
import numpy as np
from ServoMotor import *
import math as m
import time

# The server's hostname or IP address
HOST = '192.168.1.29'
# The port used by the server
PORT = 65432

filename = "/dev/ttyUSB0"
motor = ServoMotor(filename)

# Initialize USB Port
IO = motor.IO_Init()
if IO < 0:
    print('IO exit')
    sys.exit()

# Set servo mode to all servos
# LEFT front
motor.setServoMode(10)
motor.setServoMode(12)
motor.setServoMode(11)
# LEFT back
motor.setServoMode(30)
motor.setServoMode(32)
motor.setServoMode(31)
# RIGHT front
motor.setServoMode(20)
motor.setServoMode(22)
motor.setServoMode(21)
# RIGTH back
motor.setServoMode(40)
motor.setServoMode(42)
motor.setServoMode(41)

# Initialize socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Connect to network
    s.connect((HOST, PORT))

    # Check message
    check = np.arange(1, dtype=np.float32)
    check_data = check.tobytes()

    # Start walking
    while True:
        s.sendall(check_data)
        # Get position data from server
        pos_data = s.recv(1024)
        pos = np.frombuffer(pos_data, dtype=np.float32)
        # If there's no more data break the loop
        if not pos_data:
            break
        # Move all servos to their corresponding position
        # LEFT front
        #motor.move(10, pos[0], 100)
        motor.move(12, int(pos[1]), 100)
        motor.move(11, int(pos[2]), 100)
        # LEFT back
        #motor.move(30, pos[6], 100)
        motor.move(32, int(pos[7]), 100)
        motor.move(31, int(pos[8]), 100)
        # RIGHT front
        #motor.move(20, pos[3], 100)
        motor.move(22, int(pos[4]), 100)
        motor.move(21, int(pos[5]), 100)
        # RIGTH back
        #motor.move(40, pos[9], 100)
        motor.move(42, int(pos[10]), 100)
        motor.move(41, int(pos[11]), 100)

        time.sleep(0.005)


time.sleep(0.1)

