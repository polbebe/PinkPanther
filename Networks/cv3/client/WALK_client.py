#!/usr/bin/env python3
import socket
import numpy as np
from ServoMotor import *
import math as m
import time
import random

# The server's hostname or IP address
HOST = '192.168.1.29'
# The port used by the server
PORT = 65432

# Initialize C-types pylx16a
filename = "/dev/ttyUSB0"
motor = ServoMotor(filename)
IO = motor.IO_Init()
if IO < 0:
    print('IO exit')
    sys.exit()

# Set servo mode to all servos
for j in range(1,5):
    a = 10*j
    r = range(a, a+3)
    for i in r:
        motor.setServoMode(i)

# Initialize socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Connect to network
    s.connect((HOST, PORT))

    # Initialize
    delta_pos = 25
    pos_read = np.zeros(12, dtype=np.float32)
    start = time.time()
    
    # WALK
    while True:
        # Get current position of motors
        z = 0
        for k in range(1,5):
            a = 10*k
            r = range(a, a+3)
            for l in r:
                pos_read[z] = motor.readPosition(l)
                z += 1

        # Send state
        s.sendall(servo_values.tobytes())

        # Get position data from server
        pos_data = s.recv(1024)
        pos = np.frombuffer(pos_data, dtype=np.float32)

        # If there's no more data break the loop
        if not pos_data:
            print('Connection broken')
            break

        # Move motors to current position plus RANDOM delta_pos
        z = 0
        for k in range(1,5):
            a = 10*k
            r = range(a, a+3)
            for l in r:
                if l%10 == 0:
                    motor.move(l, int(pos[z]), 100)
                else:
                    if random.getrandbits(1) > 0:
                        motor.move(l, int(pos[z] + delta_pos), 100)
                    else:
                        motor.move(l, int(pos[z] - delta_pos), 100)
                z += 1

        time.sleep(0.1)



