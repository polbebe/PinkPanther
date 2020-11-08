from imu_client import *
from servo_client import *

import time
import socket

import numpy as np
import math

class Listener():
    def __init__(self):
        # Robot State values that will be updated
        self.robot_state = np.zeros(15, dtype=np.float32)

        # Initialize both IMU client and SERVO client
        self.imu = ImuData()
        self.servo = ServoData()
    
    # Read and return Robot state
    def read(self):
        # Read SERVO values and add them to Robot State
        self.robot_state[:12] = self.servo.read()

        # Read IMU values and add them to Robot State
        self.robot_state[12:] = self.imu.read()

        return self.robot_state

    def write(self, path=None):
        

if __name__ == '__main__':
    # Construct MAIN CLIENT object
    client = Listener()

    while True:
        print(client.read())
        time.sleep(1)



