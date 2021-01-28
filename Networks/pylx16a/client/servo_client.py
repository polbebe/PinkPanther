from lx16a import *

import numpy as np

class ServoData():
    # Constructor method
    def __init__(self):
        # Servo position values that will be updated
        self.servo_values = np.zeros(12, dtype=np.float64)
        self.pos = None

        # Initialize the port that the controller board is connected to
        LX16A.initialize("/dev/ttyUSB0")

        # Initialize Servo control tags
        # LEFT FRONT
        self.s10 = LX16A(10)
        self.s12 = LX16A(12)
        self.s11 = LX16A(11)
        # LEFT BACK
        self.s30 = LX16A(30)
        self.s32 = LX16A(32)
        self.s31 = LX16A(31)
        # RIGHT FRONT
        self.s20 = LX16A(20)
        self.s22 = LX16A(22)
        self.s21 = LX16A(21)
        # RIGHT BACK
        self.s40 = LX16A(40)
        self.s42 = LX16A(42)
        self.s41 = LX16A(41)

    # Write new current SERVO Values
    def write(self, pos):
        
        # Move all servos to their corresponding position
        # LEFT FRONT
        self.s10.moveTimeWrite(130)
        self.s12.moveTimeWrite(pos[1]) #print(pos[1])
        self.s11.moveTimeWrite(pos[2]) #print(pos[2])
        # LEFT BACK
        self.s32.moveTimeWrite(pos[7]) #print(pos[7])
        self.s31.moveTimeWrite(pos[8]) #print(pos[8])
        # RIGHT FRONT
        self.s22.moveTimeWrite(pos[4]) #print(pos[4])
        self.s21.moveTimeWrite(pos[5]) #print(pos[5])
        # RIGHT BACK
        self.s42.moveTimeWrite(pos[10]) #print(pos[10])
        self.s41.moveTimeWrite(pos[11]) #print(pos[11])

    # Read and return SERVO Values
    def read(self):
        # Get the servo values from servos
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

        return self.servo_values

