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

# Calculate speed
t_start = time.time()
for i in range (10):
    p.stepSimulation()
robotPos1, robotOrn1 = p.getBasePositionAndOrientation(robotId)

# Define version
version= "0.1.0"

# Read v values from those saved from simulation
df = pd.read_csv('Hardcoded_{}.csv'.format(version))
v = df['Best Values'].to_numpy()


v =[0.1, 0, 0, 
    -0.2, 0.1, 0, 
    0.3, 0.1, 1, 

    0.1, 0, 0, 
    -0.2, -0.1, 0, 
    0.3, -0.1, 1, 

    0.1, 0, 0, 
    -0.2, -0.2, 0, 
    0.3, -0.2, 0, 

    0.1, 0, 0, 
    -0.2, 0.2, 0, 
    0.3, 0.2, 0, 

    0.1]
    

for i in range (2000):
    p.stepSimulation()

    if(i<500):
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

    #elif(i<600):
    else:
        armpit_lf = v[0] + v[1]*m.sin(i*v[36] + v[2])
        p.setJointMotorControl2(robotId, 0, controlMode=mode, targetPosition=armpit_lf, force=maxForce)
        elbow_lf = v[3] + v[4]*m.sin(i*v[36] + v[5])
        p.setJointMotorControl2(robotId, 1, controlMode=mode, targetPosition=elbow_lf, force=maxForce)
        knee_lf = v[6] + v[7]*m.sin(i*v[36] + v[8])
        p.setJointMotorControl2(robotId, 2, controlMode=mode, targetPosition=knee_lf, force=maxForce)
        
        armpit_rf = v[9] + v[10]*m.sin(i*v[36] + v[11])
        p.setJointMotorControl2(robotId, 3, controlMode=mode, targetPosition=armpit_rf, force=maxForce)
        elbow_rf = v[12] + v[13]*m.sin(i*v[36] + v[14])
        p.setJointMotorControl2(robotId, 4, controlMode=mode, targetPosition=elbow_rf, force=maxForce)
        knee_rf = v[15] + v[16]*m.sin(i*v[36] + v[17])
        p.setJointMotorControl2(robotId, 5, controlMode=mode, targetPosition=knee_rf, force=maxForce)
        
        armpit_lb = v[18] + v[19]*m.sin(i*v[36] + v[20])
        p.setJointMotorControl2(robotId, 6, controlMode=mode, targetPosition=armpit_lb, force=maxForce)
        elbow_lb = v[21] + v[22]*m.sin(i*v[36] + v[23])
        p.setJointMotorControl2(robotId, 7, controlMode=mode, targetPosition=elbow_lb, force=maxForce)
        knee_lb = v[24] + v[25]*m.sin(i*v[36] + v[26])
        p.setJointMotorControl2(robotId, 8, controlMode=mode, targetPosition=knee_lb, force=maxForce)
        
        armpit_rb = v[27] + v[28]*m.sin(i*v[36] + v[29])
        p.setJointMotorControl2(robotId, 9, controlMode=mode, targetPosition=armpit_rb, force=maxForce)
        elbow_rb = v[30] + v[31]*m.sin(i*v[36] + v[32])
        p.setJointMotorControl2(robotId, 10, controlMode=mode, targetPosition=elbow_rb, force=maxForce)
        knee_rb = v[33] + v[34]*m.sin(i*v[36] + v[35])
        p.setJointMotorControl2(robotId, 11, controlMode=mode, targetPosition=knee_rb, force=maxForce)
        
        time.sleep(1./240.)

    #else:
        #time.sleep(1./240.)

t_finish = time.time()
robotPos2, robotOrn2 = p.getBasePositionAndOrientation(robotId)

# Calculate speed
x = robotPos2[0]-robotPos1[0]
y = robotPos2[1]-robotPos1[1]
dis = (x**2 + y**2)**0.5
t = t_finish - t_start
s = dis/t

print("Speed: ", s, "[m/s]")
print("Distance: ", dis, "[m]")

p.disconnect()
"""
# Save values for later simulating
# Save best values as csv for simulation
df = pd.DataFrame({"Best Values" : v})
df.to_csv("Hardcoded_{}.csv".format(version), index=[0])
"""