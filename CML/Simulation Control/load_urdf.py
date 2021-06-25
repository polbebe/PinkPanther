import pybullet as p
import time
import pybullet_data
import math as m

# Start pybullet simulation
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-10)
planeId = p.loadURDF("plane/plane.urdf")
robotStartPos = [0,0,0.2]
robotStartOrientation = p.getQuaternionFromEuler([0,0,0])
robotId = p.loadURDF("PinkPanther_CML/urdf/pp_urdf_final.urdf", robotStartPos, robotStartOrientation)
mode = p.POSITION_CONTROL
maxForce = 10

print("Joint: {}".format(p.getJointInfo(robotId, 1)))

_link_name_to_index = {p.getBodyInfo(robotId)[0].decode('UTF-8'):-1,}
        
for _id in range(p.getNumJoints(robotId)):
    _name = p.getJointInfo(robotId, _id)[12].decode('UTF-8')
    _link_name_to_index[_name] = _id
    print("{} : {}".format(_id, _name))

p.changeDynamics(robotId, 2, lateralFriction=0.3)
p.changeDynamics(robotId, 5, lateralFriction=0.3)
p.changeDynamics(robotId, 8, lateralFriction=0.3)
p.changeDynamics(robotId, 11, lateralFriction=0.3)

# Calculate speed
t_start = time.time()
for i in range (10):
    p.stepSimulation()
robotPos1, robotOrn1 = p.getBasePositionAndOrientation(robotId)

for i in range (10000):
    p.stepSimulation()
    pos = 0.3*m.sin(i*0.01)
    #print(pos)
    for i in range(12):
        p.setJointMotorControl2(robotId, i, controlMode=mode, targetPosition=pos)
    time.sleep(1./240.)

p.disconnect()
