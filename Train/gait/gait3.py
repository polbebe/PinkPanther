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
for i in range (10000):
    p.stepSimulation()

    """armpits_one = 0.2*m.sin(i*0.1-0.2) - 0.2
    p.setJointMotorControl2(robotId, 0, controlMode=mode, targetPosition=armpits_one)
    p.setJointMotorControl2(robotId, 6, controlMode=mode, targetPosition=armpits_one)

    armpits_two = -armpits_one
    p.setJointMotorControl2(robotId, 9, controlMode=mode, targetPosition=armpits_two)
    p.setJointMotorControl2(robotId, 3, controlMode=mode, targetPosition=armpits_two)"""

    shoulders_one = 0.4*m.sin(i*0.1)+0.2
    p.setJointMotorControl2(robotId, 1, controlMode=mode, targetPosition=shoulders_one)
    p.setJointMotorControl2(robotId, 10, controlMode=mode, targetPosition=shoulders_one)

    shoulders_two = -shoulders_one
    p.setJointMotorControl2(robotId, 7, controlMode=mode, targetPosition=shoulders_two)
    p.setJointMotorControl2(robotId, 4, controlMode=mode, targetPosition=shoulders_two)

    knees_one = 0.5*m.sin(i*0.1-0.2)
    p.setJointMotorControl2(robotId, 2, controlMode=mode, targetPosition=knees_one)
    p.setJointMotorControl2(robotId, 11, controlMode=mode, targetPosition=knees_one)

    knees_two = -knees_one
    p.setJointMotorControl2(robotId, 8, controlMode=mode, targetPosition=knees_two)
    p.setJointMotorControl2(robotId, 5, controlMode=mode, targetPosition=knees_two)

    """TESTING

    armpits_one = 0.2*m.sin(i*0.01)
    p.setJointMotorControl2(robotId, 0, controlMode=mode, targetPosition=armpits_one)

    shoulders_one = 0.4*m.sin(i*0.01)
    p.setJointMotorControl2(robotId, 1, controlMode=mode, targetPosition=shoulders_one)

    knees_one = 0.3*m.sin(i*0.01)
    p.setJointMotorControl2(robotId, 2, controlMode=mode, targetPosition=knees_one)"""


    time.sleep(1./2400.)
robotPos, robotOrn = p.getBasePositionAndOrientation(robotId)
print(robotPos,robotOrn)
p.disconnect()
