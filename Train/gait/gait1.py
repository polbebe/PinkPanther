import pybullet as p
import time
import pybullet_data
import math as m

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-10)
planeId = p.loadURDF("../plane/plane.urdf")

robotStartPos = [0,0,0.1]
robotStartOrientation = p.getQuaternionFromEuler([0,0,0])
robotId = p.loadURDF("../../robot/PinkPanther/urdf/PinkPanther.urdf", robotStartPos, robotStartOrientation)
mode = p.POSITION_CONTROL

number_of_joints = p.getNumJoints(robotId)
print("Joints:", number_of_joints)

for i in range (10000):
    p.stepSimulation()
    # Walks backwards quite quick

    #armpits_one = 0.2*m.sin(i*0.01)
    #p.setJointMotorControl2(robotId, 0, controlMode=mode, targetPosition=armpits_one)
    #p.setJointMotorControl2(robotId, 9, controlMode=mode, targetPosition=armpits_one)

    #p.setJointMotorControl2(robotId, 6, controlMode=mode, targetPosition=tarPosA)
    #p.setJointMotorControl2(robotId, 3, controlMode=mode, targetPosition=-tarPosA)

    shoulders_one = 0.2*m.sin(i*0.1)
    p.setJointMotorControl2(robotId, 1, controlMode=mode, targetPosition=shoulders_one)
    p.setJointMotorControl2(robotId, 10, controlMode=mode, targetPosition=shoulders_one)

    shoulders_two = -0.2*m.sin(i*0.1)
    p.setJointMotorControl2(robotId, 7, controlMode=mode, targetPosition=shoulders_two)
    p.setJointMotorControl2(robotId, 4, controlMode=mode, targetPosition=shoulders_two)

    knees_one = 0.2*m.sin(i*0.1)
    p.setJointMotorControl2(robotId, 2, controlMode=mode, targetPosition=knees_one)
    p.setJointMotorControl2(robotId, 11, controlMode=mode, targetPosition=knees_one)

    knees_two = -0.2*m.sin(i*0.1)
    p.setJointMotorControl2(robotId, 8, controlMode=mode, targetPosition=knees_two)
    p.setJointMotorControl2(robotId, 5, controlMode=mode, targetPosition=knees_two)

    # time.sleep(1./2400.)
    time.sleep(1./24.)

    # robotPos, robotOrn = p.getBasePositionAndOrientation(robot)
    # if i%100==0:
    #     print(robotPos,robotOrn)

robotPos, robotOrn = p.getBasePositionAndOrientation(robot)
print(robotPos,robotOrn)
p.disconnect()
