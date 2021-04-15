#!/usr/bin/env python3
from ServoMotor import *
import time


filename = "/dev/ttyUSB0"
motor = ServoMotor(filename)

# Initialize USB Port
IO = motor.IO_Init()
if IO < 0:
    print('IO exit')
    sys.exit()

# Set servo mode to all servos
motor.setServoMode(10)
motor.setServoMode(12)
motor.setServoMode(11)
motor.setServoMode(30)
motor.setServoMode(32)
motor.setServoMode(31)
motor.setServoMode(20)
motor.setServoMode(22)
motor.setServoMode(21)
motor.setServoMode(40)
motor.setServoMode(42)
motor.setServoMode(41)

motor.setPositionOffset(10,30)
motor.setPositionOffset(12,64)
motor.setPositionOffset(22,50)
motor.setPositionOffset(21,70)
motor.setPositionOffset(30,26)
motor.setPositionOffset(32,55)
motor.setPositionOffset(40,80)
motor.setPositionOffset(42,35)
motor.setPositionOffset(41,90)


pos = [500, 650, 533, 500, 350, 467, 500, 650, 533, 500, 350, 467]
#pos = [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500]

motor.move(32,688,1000)
motor.move(12,688,1000)

motor.move(42,313,1000)
motor.move(22,313,1000)

time.sleep(1)

i = 688
j = 313
while i>240:
    motor.move(32,int(i),100)
    motor.move(12,int(i),100)
    motor.move(42,int(j),100)
    motor.move(22,int(j),100)
    i-=4
    j+=5
    
print('out')
time.sleep(5)
motor.move(32,500,1000)