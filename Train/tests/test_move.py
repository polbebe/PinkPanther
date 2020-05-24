import pybullet as p
import math as m
import time
import pybullet_data
physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
p.setGravity(0,0,-10)
planeId = p.loadURDF("../plane/plane.urdf")
cubeStartPos = [0,0,1]
cubeStartOrientation = p.getQuaternionFromEuler([0,0,0])
boxId = p.loadURDF("../robot/Code/PinkPanther/urdf/SimpleShapes.urdf",cubeStartPos, cubeStartOrientation)
mode = p.POSITION_CONTROL
# print(p.getJointInfo(boxId, 0))
jointIndex = 0 # test different joints, starting at 0
for i in range (10000):
    p.stepSimulation()
    p.setJointMotorControl2(boxId, 0, controlMode=mode, targetPosition=0.9+0.8*m.sin(i*0.01+0.6))
    time.sleep(1./240.)
cubePos, cubeOrn = p.getBasePositionAndOrientation(boxId)
print(cubePos,cubeOrn)
p.disconnect()
