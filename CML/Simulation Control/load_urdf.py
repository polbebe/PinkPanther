import pybullet as p
import time
import pybullet_data
import math as m
import numpy as np
from fns import *

# Start pybullet simulation
physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-9.81)
planeId = p.loadURDF("plane/plane.urdf")
robotStartPos = [0,0,0.2]
robotStartOrientation = p.getQuaternionFromEuler([0,0,0])
robotId = p.loadURDF("PinkPanther_CML/urdf/pp_urdf_final.urdf", robotStartPos, robotStartOrientation)
mode = p.POSITION_CONTROL
maxForce = 1.667
maxVel = 6.545
APS = 15
n_sim_steps = int(240/APS)

# Call corresponding function to convert sim2real/real2sim
def convFns(pos, convType):
    conv =  [left_armpit, left_shoulder, left_elbow, right_armpit, right_shoulder, right_elbow,
            left_armpit, left_shoulder, left_elbow, right_armpit, right_shoulder, right_elbow]
    targ = np.zeros(12)
    for i in range(len(pos)):
        if i==0:
            targ[i] = conv[i](pos[i], convType, "front")
        elif i==6:
            targ[i] = conv[i](pos[i], convType, "back")
        else:
            targ[i] = conv[i](pos[i], convType)
    return targ

'''
print("Joint: {}".format(p.getJointInfo(robotId, 1)))

_link_name_to_index = {p.getBodyInfo(robotId)[0].decode('UTF-8'):-1,}
        
for _id in range(p.getNumJoints(robotId)):
    _name = p.getJointInfo(robotId, _id)[12].decode('UTF-8')
    _link_name_to_index[_name] = _id
    print("{} : {}".format(_id, _name))

# Calculate speed
t_start = time.time()
for i in range (10):
    p.stepSimulation()
robotPos1, robotOrn1 = p.getBasePositionAndOrientation(robotId)

val=0.1
p.changeDynamics(robotId, 2, lateralFriction=val)
p.changeDynamics(robotId, 5, lateralFriction=val)
p.changeDynamics(robotId, 8, lateralFriction=val, rollingFriction=val-val, spinningFriction=val)
p.changeDynamics(robotId, 11, lateralFriction=val, rollingFriction=val-val, spinningFriction=val)

# Reset down
for j in range(20):
    for i in range(n_sim_steps):
        p.stepSimulation()
    pos = convFns([500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500], "real2sim")
    for i in range(12):
        p.setJointMotorControl2(robotId, i, controlMode=mode, targetPosition=pos[i], force=maxForce, maxVelocity=maxVel/4)
    time.sleep(1./APS)

# Reset up
for j in range(20):
    for i in range(n_sim_steps):
        p.stepSimulation()
    vel = [1000, 1000, 1000, 1000, 1000, 1000, 700, 700, 700, 700, 700, 700]
    for x in range(len(vel)):
        vel[x] = vel[x]/250
    for i in range(12):
        p.setJointMotorControl2(robotId, i, controlMode=mode, targetPosition=0, force=maxForce, maxVelocity=maxVel/vel[i])
    time.sleep(1./APS)

# Reset down
for j in range(20):
    for i in range(n_sim_steps):
        p.stepSimulation()
    pos = convFns([500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500], "real2sim")
    for i in range(12):
        p.setJointMotorControl2(robotId, i, controlMode=mode, targetPosition=pos[i], force=maxForce, maxVelocity=maxVel/4)
    time.sleep(1./APS)

# Reset up
for j in range(20):
    for i in range(n_sim_steps):
        p.stepSimulation()
    vel = [1000, 1000, 1000, 1000, 1000, 1000, 700, 700, 700, 700, 700, 700]
    for x in range(len(vel)):
        vel[x] = vel[x]/250
    for i in range(12):
        p.setJointMotorControl2(robotId, i, controlMode=mode, targetPosition=0, force=maxForce, maxVelocity=maxVel/vel[i])
    time.sleep(1./APS)
'''
step = 3

for j in np.arange(0,10000,step):
    for i in range(n_sim_steps):
        p.stepSimulation()
    pos = 0.3*m.sin(j*0.1)
    #print(pos)
    for i in range(12):
        p.setJointMotorControl2(robotId, i, controlMode=mode, targetPosition=pos, force=maxForce, maxVelocity=maxVel)
    time.sleep(1./APS)

print("GOODBYE")
p.disconnect()
