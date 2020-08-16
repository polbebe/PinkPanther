import pybullet as p
import time
import pybullet_data
import math as m
import pandas as pd

# Start pybullet simulation
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-10)
planeId = p.loadURDF("../plane/plane.urdf")
robotStartPos = [0,0,0.2]
robotStartOrientation = p.getQuaternionFromEuler([0,0,0])
robotId = p.loadURDF("../../robot/PP/urdf/PP.urdf", robotStartPos, robotStartOrientation)
mode = p.POSITION_CONTROL
maxForce = 4

for i in range (2000):
    p.stepSimulation()

    armpit_lf=0
    elbow_lf=-0.2
    knee_lf=0.3

    armpit_rf=0
    elbow_rf=-0.2
    knee_rf=0.3

    armpit_lb=0
    elbow_lb=-0.2
    knee_lb=0.3

    armpit_rb=0
    elbow_rb=-0.2
    knee_rb=0.3

    p.setJointMotorControl2(robotId, 0, controlMode=mode, targetPosition=armpit_lf, force=maxForce)
    p.setJointMotorControl2(robotId, 1, controlMode=mode, targetPosition=elbow_lf, force=maxForce)
    p.setJointMotorControl2(robotId, 2, controlMode=mode, targetPosition=knee_lf, force=maxForce)

    p.setJointMotorControl2(robotId, 3, controlMode=mode, targetPosition=armpit_rf, force=maxForce)
    p.setJointMotorControl2(robotId, 4, controlMode=mode, targetPosition=elbow_rf, force=maxForce)
    p.setJointMotorControl2(robotId, 5, controlMode=mode, targetPosition=knee_rf, force=maxForce)

    p.setJointMotorControl2(robotId, 6, controlMode=mode, targetPosition=armpit_lb, force=maxForce)
    p.setJointMotorControl2(robotId, 7, controlMode=mode, targetPosition=elbow_lb, force=maxForce)
    p.setJointMotorControl2(robotId, 8, controlMode=mode, targetPosition=knee_lb, force=maxForce)

    p.setJointMotorControl2(robotId, 9, controlMode=mode, targetPosition=armpit_rb, force=maxForce)
    p.setJointMotorControl2(robotId, 10, controlMode=mode, targetPosition=elbow_rb, force=maxForce)
    p.setJointMotorControl2(robotId, 11, controlMode=mode, targetPosition=knee_rb, force=maxForce)

    time.sleep(1./240.)

p.disconnect()
