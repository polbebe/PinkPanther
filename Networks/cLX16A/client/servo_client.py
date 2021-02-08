from ServoMotor import *

import numpy as np
import sys
import time

class ServoData():
    # Constructor method
    def __init__(self):
        # Servo position values that will be updated
        self.servo_values = np.zeros(12, dtype=np.float64)
        self.pos = None

        # Initialize ServoMotor class
        filename = "/dev/ttyUSB0"
        self.motor = ServoMotor(filename)

        # Initialize USB Port
        self.IO = self.motor.IO_Init()
        if self.IO < 0:
            print('IO exit')
            sys.exit()

        # Set servo mode to all servos
        # LEFT front
        self.motor.setServoMode(10)
        self.motor.setServoMode(12)
        self.motor.setServoMode(11)
        # LEFT back
        self.motor.setServoMode(30)
        self.motor.setServoMode(32)
        self.motor.setServoMode(31)
        # RIGHT front
        self.motor.setServoMode(20)
        self.motor.setServoMode(22)
        self.motor.setServoMode(21)
        # RIGTH back
        self.motor.setServoMode(40)
        self.motor.setServoMode(42)
        self.motor.setServoMode(41)
        
    # Write new current SERVO Values
    def write(self, pos):
        
        # Move all servos to their corresponding position
        # LEFT front
        print(pos)
        #self.motor.move(10, pos[0], 100)
        self.motor.move(12, int(pos[1]), 0)
        self.motor.move(11, int(pos[2]), 0)
        # LEFT back
        #self.motor.move(30, pos[6], 100)
        self.motor.move(32, int(pos[7]), 0)
        self.motor.move(31, int(pos[8]), 300)
        # RIGHT front
        #self.motor.move(20, pos[3], 100)
        self.motor.move(22, int(pos[4]), 0)
        self.motor.move(21, int(pos[5]), 300)
        # RIGTH back
        #self.motor.move(40, pos[9], 100)
        self.motor.move(42, int(pos[10]), 0)
        self.motor.move(41, int(pos[11]), 0)
        
        time.sleep(0.01)

    # Read and return SERVO Values
    def read(self):
        # Get the servo values from servos
        self.servo_values[0] = 0
        self.servo_values[1] = self.motor.readPosition(12)
        self.servo_values[2] = self.motor.readPosition(11)
        self.servo_values[3] = 0
        self.servo_values[4] = self.motor.readPosition(22)
        self.servo_values[5] = self.motor.readPosition(21)
        self.servo_values[6] = 0
        self.servo_values[7] = self.motor.readPosition(32)
        self.servo_values[8] = self.motor.readPosition(31)
        self.servo_values[9] = 0
        self.servo_values[10] = self.motor.readPosition(42)
        self.servo_values[11] = self.motor.readPosition(41)

        return self.servo_values

if __name__ == '__main__':
    # Construct SERVO object and allow use of methods
    i = ServoData()
