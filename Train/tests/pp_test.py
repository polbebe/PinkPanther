import pybullet as p
import time
import pybullet_data
import math as m
physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
p.setGravity(0,0,-10)
planeId = p.loadURDF("../plane/plane.urdf")
robotStartPos = [0,0,1]
robotStartOrientation = p.getQuaternionFromEuler([0,0,0])
<<<<<<< HEAD:__1.Code/tests/pp_test.py
robotId = p.loadURDF("../../__A.Robots/PinkPanther/urdf/PinkPanther.urdf", robotStartPos, robotStartOrientation)
#mode = p.POSITION_CONTROL
=======
robotId = p.loadURDF("../robot/PinkPanther/urdf/PinkPanther.urdf", robotStartPos, robotStartOrientation)
mode = p.POSITION_CONTROL
>>>>>>> 60e1ec426709e338e07621eacb475bec085154ed:code/tests/pp_test.py
# print(p.getJointInfo(robotId, 0))
#jointIndex = 5 # test different joints, starting at 0
for i in range (10000):
    p.stepSimulation()
    #tarPos = m.sin(i*0.1)
    #print(tarPos)
    #p.setJointMotorControl2(robotId, jointIndex, controlMode=mode, targetPosition=tarPos)
    time.sleep(1./240.)
robotPos, robotOrn = p.getBasePositionAndOrientation(robotId)
print(robotPos,robotOrn)
p.disconnect()
