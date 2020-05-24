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
robotId = p.loadURDF("../../Robot/PinkPanther/urdf/PinkPanther.urdf", robotStartPos, robotStartOrientation)
mode = p.POSITION_CONTROL
for i in range (10000):
    p.stepSimulation()


    # FRONT LEGS

    if i <= m.pi*50:
        shoulders_one = 0.5*m.sin(i*0.01)
    elif i <= m.pi*60:
        shoulders_one = 1.5*m.sin(i*0.02)
    else:
        shoulders_one = 0

    p.setJointMotorControl2(robotId, 1, controlMode=mode, targetPosition=shoulders_one)
    p.setJointMotorControl2(robotId, 4, controlMode=mode, targetPosition=shoulders_one)

    
    if i <= m.pi*50:
        knees_one = -0.3*m.sin(i*0.01)
    elif i <= m.pi*60:
        knees_one = -1.5*m.sin(i*0.02)
    else:
        knees_one = 0

    p.setJointMotorControl2(robotId, 2, controlMode=mode, targetPosition=knees_one)
    p.setJointMotorControl2(robotId, 5, controlMode=mode, targetPosition=knees_one)

    #print(knees_one)


    # BACK LEGS

    if i <= m.pi*50:
        shoulders_two = 0.5*m.sin(i*0.01)
    elif i <= m.pi*70:
        shoulders_two = 3*m.sin(i*0.02)
    else:
        shoulders_two = 0


    p.setJointMotorControl2(robotId, 7, controlMode=mode, targetPosition=shoulders_two)
    p.setJointMotorControl2(robotId, 10, controlMode=mode, targetPosition=shoulders_two)

    if i <= m.pi*50:
        knees_two = -0.3*m.sin(i*0.01)
    elif i <= m.pi*70:
        knees_two = -3*m.sin(i*0.02)
    else:
        knees_two = 0

    p.setJointMotorControl2(robotId, 8, controlMode=mode, targetPosition=knees_two)
    p.setJointMotorControl2(robotId, 11, controlMode=mode, targetPosition=knees_two)
    

    time.sleep(1./2400.)
robotPos, robotOrn = p.getBasePositionAndOrientation(robotId)
print(robotPos,robotOrn)
p.disconnect()
