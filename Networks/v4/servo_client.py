import socket
import numpy as np
from lx16a import *
from threading import Thread

import math as m
import time


class ServoData:
    # Constructor method
    def __init__(self, host):
        # The server's hostname or IP address
        HOST = '192.168.1.29'
        # The port used by the server
        PORT = 65432

        # Set up socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

        # Servo position values that will be updated
        self.servo_values = np.zeros(12, dtype=np.float64)
        # Keep track whether stopped or not
        self.stopped = False

        # Initialize the port that the controller board is connected to
        LX16A.initialize("/dev/ttyUSB0")
        # Initialize Servo controls
        # LEFT
        # FRONT
        self.s10 = LX16A(10)
        self.s12 = LX16A(12)
        self.s11 = LX16A(11)
        # BACK
        self.s30 = LX16A(30)
        self.s32 = LX16A(32)
        self.s31 = LX16A(31)
        # RIGHT
        # FRONT
        self.s20 = LX16A(20)
        self.s22 = LX16A(22)
        self.s21 = LX16A(21)
        # BACK
        self.s40 = LX16A(40)
        self.s42 = LX16A(42)
        self.s41 = LX16A(41)

    # Start thread
    def start(self):
        # Thread which updates its rpy values
        t = Thread(target=self.update, args=())
        # Make it run in background
        t.daemon=True
        # Start the updating
        t.start()
        return self

    # Update imu values
    def update(self):
        while True:
            if self.stopped:
                break
            # Get the servo values from servos
            # Calculate servo_values
            #self.servo_values[0] = 0
            self.servo_values[1] = self.s12.getPhysicalPos() #- x.getVirtualPos()
            self.servo_values[2] = self.s11.getPhysicalPos() #- x.getVirtualPos()
            #self.servo_values[3] = 0
            self.servo_values[4] = self.s22.getPhysicalPos() #- x.getVirtualPos()
            self.servo_values[5] = self.s21.getPhysicalPos() #- x.getVirtualPos()
            #self.servo_values[6] = 0
            self.servo_values[7] = self.s32.getPhysicalPos() #- x.getVirtualPos()
            self.servo_values[8] = self.s31.getPhysicalPos() #- x.getVirtualPos()
            #self.servo_values[9] = 0
            self.servo_values[10] = self.s42.getPhysicalPos() #- x.getVirtualPos()
            self.servo_values[11] = self.s41.getPhysicalPos() #- x.getVirtualPos()

            # Send values back to server
            self.s.sendall(self.servo_values.tobytes())
        
            # Get position data from server
            p = self.s.recv(1024)
            pos = np.frombuffer(p, dtype=np.float32)
            # If there's no more data break the loop
            if not p:
                break
            # Move all servos to their corresponding position
            self.s10.moveTimeWrite(130)
            # LEFT FRONT
            # Move servo 12 (elbow)
            self.s12.moveTimeWrite(pos[1]) #print(pos[1])
            # Move servo 11 (knee)
            self.s11.moveTimeWrite(pos[2]) #print(pos[2])
            # LEFT BACK
            # Move servo 32 (elbow)
            self.s32.moveTimeWrite(pos[7]) #print(pos[7])
            # Move servo 31 (knee)
            self.s31.moveTimeWrite(pos[8]) #print(pos[8])
            # RIGHT FRONT
            # Move servo 22 (elbow)
            self.s22.moveTimeWrite(pos[4]) #print(pos[4])
            # Move servo 21 (knee)
            self.s21.moveTimeWrite(pos[5]) #print(pos[5])
            # RIGHT BACK
            # Move servo 42 (elbow)
            self.s42.moveTimeWrite(pos[10]) #print(pos[10])
            # Move servo 41 (knee)
            s41.moveTimeWrite(pos[11]) #print(pos[11])
            time.sleep(0.0001)

    def read(self):
        return self.servo_values

    def stop(self):
        self.stopped = True



if __name__ == '__main__':
    # Construct object and start
    i = ServoData()
    i.start()
