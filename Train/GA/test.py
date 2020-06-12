import pybullet as p
import time
import pybullet_data
import math as m
import numpy as np
import matplotlib.pyplot as plt

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-10)
planeId = p.loadURDF("../plane/plane.urdf")

robotStartPos = [0,0,0.2]
robotStartOrientation = p.getQuaternionFromEuler([0,0,0])
robotId = p.loadURDF("../../robot/PP/urdf/PP.urdf", robotStartPos, robotStartOrientation)
mode = p.POSITION_CONTROL

robotPos1, robotOrn1 = p.getBasePositionAndOrientation(robotId)

elbow_pos = []
knee_pos = []
i_s = []

t_start = time.time()

for i in range (500):
    p.stepSimulation()
    # Walks backwards quite quick
    robotPos, robotOrn = p.getBasePositionAndOrientation(robotId)
    print(p.getEulerFromQuaternion(robotOrn))
    # Let the robot fall to the ground before starting to walk
    if i==0:
        time.sleep(1)

    i_s.append(i)

    """armpits_one = 0.01*m.sin(i*0.1)
    p.setJointMotorControl2(robotId, 0, controlMode=mode, targetPosition=armpits_one)
    p.setJointMotorControl2(robotId, 9, controlMode=mode, targetPosition=armpits_one)

    armpits_two = -armpits_one
    p.setJointMotorControl2(robotId, 6, controlMode=mode, targetPosition=armpits_two)
    p.setJointMotorControl2(robotId, 3, controlMode=mode, targetPosition=armpits_two)"""

    shoulders_one = 0.2*m.sin(i*0.1)

    elbow_pos.append(shoulders_one)

    p.setJointMotorControl2(robotId, 1, controlMode=mode, targetPosition=shoulders_one)
    p.setJointMotorControl2(robotId, 10, controlMode=mode, targetPosition=shoulders_one)

    shoulders_two = -shoulders_one
    p.setJointMotorControl2(robotId, 7, controlMode=mode, targetPosition=shoulders_two)
    p.setJointMotorControl2(robotId, 4, controlMode=mode, targetPosition=shoulders_two)

    knees_one = 0.2*m.sin(i*0.1)

    knee_pos.append(knees_one)

    p.setJointMotorControl2(robotId, 2, controlMode=mode, targetPosition=knees_one)
    p.setJointMotorControl2(robotId, 11, controlMode=mode, targetPosition=knees_one)

    knees_two = -knees_one
    p.setJointMotorControl2(robotId, 8, controlMode=mode, targetPosition=knees_two)
    p.setJointMotorControl2(robotId, 5, controlMode=mode, targetPosition=knees_two)

    time.sleep(1./2400.)


t_finish = time.time()
robotPos2, robotOrn2 = p.getBasePositionAndOrientation(robotId)

x = robotPos2[0]-robotPos1[0]
y = robotPos2[1]-robotPos1[1]
dis = (x**2 + y**2)**0.5

print("X distance traveled: ", x, "Y distance traveled: ", y)

t = t_finish - t_start
s = dis/t

print("Speed: ", s, "[m/s]")

p.disconnect()

"""
# Plot elbow position
print("Max elbow pos:",np.max(elbow_pos),"Min elbow pos:",np.min(elbow_pos))
plt.plot(i_s, elbow_pos)
plt.title("elbow position over Time")
plt.ylabel("Position [rad]")
plt.xlabel("Time [s]")
plt.savefig("elbow_test.png")
plt.clf()

# Plot knee position
print("Max knee pos:",np.max(knee_pos),"Min knee pos:",np.min(knee_pos))
plt.plot(i_s, knee_pos)
plt.title("Knee position over Time")
plt.ylabel("Position [rad]")
plt.xlabel("Time [s]")
plt.savefig("knee_test.png")
plt.clf()
"""



