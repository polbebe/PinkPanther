#!/usr/bin/env python3
import socket
import numpy as np
from lx16a import *
import math as m
import time
from sense_hat import SenseHat
import threading

# Global variable
robot_inputs = np.zeros(15, dtype=np.float32)

# Initialize the port that the controller board is connected to
LX16A.initialize("/dev/ttyUSB0")
# Initialize Servo controls
# LEFT
# FRONT
s10 = LX16A(10)
s12 = LX16A(12)
s11 = LX16A(11)
# BACK
s30 = LX16A(30)
s32 = LX16A(32)
s31 = LX16A(31)
# RIGHT
# FRONT
s20 = LX16A(20)
s22 = LX16A(22)
s21 = LX16A(21)
# BACK
s40 = LX16A(40)
s42 = LX16A(42)
s41 = LX16A(41)


def servos(lock):

    global robot_inputs, s10, s11, s12, s20, s21, s22, s30, s31, s32, s40, s41, s42

    # Start walking
    while True:
        lock.acquire()
        # Calculate robot_inputs
        #robot_inputs[0] = 0
        robot_inputs[1] = s12.getPhysicalPos() #- x.getVirtualPos()
        robot_inputs[2] = s11.getPhysicalPos() #- x.getVirtualPos()
        #robot_inputs[3] = 0
        robot_inputs[4] = s22.getPhysicalPos() #- x.getVirtualPos()
        robot_inputs[5] = s21.getPhysicalPos() #- x.getVirtualPos()
        #robot_inputs[6] = 0
        robot_inputs[7] = s32.getPhysicalPos() #- x.getVirtualPos()
        robot_inputs[8] = s31.getPhysicalPos() #- x.getVirtualPos()
        #robot_inputs[9] = 0
        robot_inputs[10] = s42.getPhysicalPos() #- x.getVirtualPos()
        robot_inputs[11] = s41.getPhysicalPos() #- x.getVirtualPos()
        lock.release()




def imus():

    global robot_inputs

    # Initialize sense hat connection
    sense = SenseHat()
    sense.clear()

    while True:
        o = sense.get_orientation()
        # Roll
        robot_inputs[12] = o["roll"]
        # Pitch
        robot_inputs[13] = o["pitch"]
        # Yaw
        robot_inputs[14] = o["yaw"]


def main_task():

    global robot_inputs

    # Threading
    lock = threading.Lock()
    servo = threading.Thread(target=servos, args=(lock,))
    imu = threading.Thread(target=imus, args=(lock,))

    servo.start()
    imu.start()

    servo.join()
    imu.join()


if __name__ == "__main__":
    # The server's hostname or IP address
    HOST = '192.168.1.201'
    # The port used by the server
    PORT = 65432

    # Initialize socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Connect to network
        s.connect((HOST, PORT))

        # Start walking
        while True:
        
            main_task()

            # Send motor inputs to server
            s.sendall(robot_inputs.tobytes())
        
            # Get position data from server
            p = s.recv(1024)
            pos = np.frombuffer(p, dtype=np.float32)
            # If there's no more data break the loop
            if not p:
                break
            # Move all servos to their corresponding position
            s10.moveTimeWrite(130)
            # LEFT FRONT
            # Move servo 12 (elbow)
            s12.moveTimeWrite(pos[1]) #print(pos[1])
            # Move servo 11 (knee)
            s11.moveTimeWrite(pos[2]) #print(pos[2])
            # LEFT BACK
            # Move servo 32 (elbow)
            s32.moveTimeWrite(pos[7]) #print(pos[7])
            # Move servo 31 (knee)
            s31.moveTimeWrite(pos[8]) #print(pos[8])
            # RIGHT FRONT
            # Move servo 22 (elbow)
            s22.moveTimeWrite(pos[4]) #print(pos[4])
            # Move servo 21 (knee)
            s21.moveTimeWrite(pos[5]) #print(pos[5])
            # RIGHT BACK
            # Move servo 42 (elbow)
            s42.moveTimeWrite(pos[10]) #print(pos[10])
            # Move servo 41 (knee)
            s41.moveTimeWrite(pos[11]) #print(pos[11])
            time.sleep(0.0001)

