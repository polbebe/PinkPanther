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

    servo_values = np.zeros(12, dtype=np.float32)

    # Start walking
    while True:
        # Get position data to be sent back
        servo_values[0] = 0#motor.readPosition(10)
        servo_values[1] = motor.readPosition(12)
        servo_values[2] = motor.readPosition(11)
        servo_values[3] = 0#motor.readPosition(20)
        servo_values[4] = motor.readPosition(22)
        servo_values[5] = motor.readPosition(21)
        servo_values[6] = 0#motor.readPosition(30)
        servo_values[7] = motor.readPosition(32)
        servo_values[8] = motor.readPosition(31)
        servo_values[9] = 0#motor.readPosition(40)
        servo_values[10] = motor.readPosition(42)
        servo_values[11] = motor.readPosition(41)
        # Send state
        s.sendall(servo_values.tobytes())
        # Get position data from server
        pos_data = s.recv(1024)
        pos = np.frombuffer(pos_data, dtype=np.float32)
        # If there's no more data break the loop
        if not pos_data:
            break
        # Move all servos to their corresponding position
        # LEFT front
        #motor.move(10, pos[0], 100)
        motor.move(12, int(pos[1]), 10)
        motor.move(11, int(pos[2]), 10)
        # LEFT back
        #motor.move(30, pos[6], 100)
        motor.move(32, int(pos[7]), 10)
        motor.move(31, int(pos[8]), 10)
        # RIGHT front
        #motor.move(20, pos[3], 100)
        motor.move(22, int(pos[4]), 10)
        motor.move(21, int(pos[5]), 10)
        # RIGTH back
        #motor.move(40, pos[9], 100)
        motor.move(42, int(pos[10]), 10)
        motor.move(41, int(pos[11]), 10)

        time.sleep(0.007)


time.sleep(0.1)

