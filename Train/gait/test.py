import pybullet as p
import time
import pybullet_data
import math as m

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-10)
planeId = p.loadURDF("../plane/plane.urdf")

robotStartPos = [0,0,1]
robotStartOrientation = p.getQuaternionFromEuler([0,0,0])
robotId = p.loadURDF("../../robot/PP/urdf/PP.urdf", robotStartPos, robotStartOrientation)
mode = p.POSITION_CONTROL

number_of_joints = p.getNumJoints(robotId)
print("Joints:", number_of_joints)

for i in range (10000):
    p.stepSimulation()

    knees_one = 0.6*m.sin(i*0.01)
    p.setJointMotorControl2(robotId, 2, controlMode=mode, targetPosition=knees_one)
    p.setJointMotorControl2(robotId, 11, controlMode=mode, targetPosition=knees_one)

    knees_two = -0.6*m.sin(i*0.01)
    p.setJointMotorControl2(robotId, 8, controlMode=mode, targetPosition=knees_two)
    p.setJointMotorControl2(robotId, 5, controlMode=mode, targetPosition=knees_two)

    time.sleep(1./1000.)


robotPos, robotOrn = p.getBasePositionAndOrientation(robot)
print(robotPos,robotOrn)
p.disconnect()
