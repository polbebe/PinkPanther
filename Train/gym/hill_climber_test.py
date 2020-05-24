import pybullet as p
import pybullet_data
import time

import math as m
import numpy as np
import matplotlib.pyplot as plt
import random as r

import gym


physicsClient = p.connect(p.GUI) #p.DIRECT for non-graphical
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-10)
planeId = p.loadURDF("../plane/plane.urdf")

robotStartPos = [0,0,0.2]
robotStartOrientation = p.getQuaternionFromEuler([0,0,0])

robotId = p.loadURDF("../../robot/PP/urdf/PP.urdf", robotStartPos, robotStartOrientation)
print("Robot:", robotId)
mode = p.POSITION_CONTROL

number_of_joints = p.getNumJoints(robotId)
print("Joints:", number_of_joints)

# for position plot
positions = []
angles = []
times = []

timediff = 1./2400.

# torque info based off of https://github.com/bulletphysics/bullet3/blob/master/examples/pybullet/examples/inverse_dynamics.py
id_revolute_joints = [0, 3, 6, 9, 
                      1, 4, 7, 10, 
                      2, 5, 8, 11]

motor_labels = {0: "LEFT FRONT ARMPIT", 1: "LEFT FRONT ELBOW", 2: "LEFT FRONT KNEE", 3:"RIGHT FRONT ARMPIT", 
                4: "RIGHT FRONT ELBOW", 5:"RIGHT FRONT KNEE", 6:"LEFT BACK ARMPIT", 7:"LEFT BACK ELBOW", 
                8:"LEFT BACK KNEE", 9:"RIGHT BACK ARMPIT", 10:"RIGHT BACK ELBOW", 11:"RIGHT BACK KNEE"}

label_list = [motor_labels[i] for i in id_revolute_joints]

joint_torques = [[] for i in range(len(id_revolute_joints))]
joint_positions = [[] for i in range(len(id_revolute_joints))]


# a = a_i + b_i*m.sin(i*w + c_i)

# Values for a_i in equation
a_i = r.randrange(-1,1,0.01)

# Values for b_i in equation
b_armpit = r.randrange(0, 0.6, 0.01)
b_elbow = r.randrange(0, 1.2, 0.01)
b_knee = r.randrange(0, 1, 0.01)

# Values for c_i in equation
c_i = r.randrange(-1,1,0.01)

# Values for w in equation
w_i = r.randrange(0,1,0.01)


for i in range (500):
    p.stepSimulation()
    time.sleep(timediff)

[robotPos1, robotOrn1] = p.getBasePositionAndOrientation(robot)



for i in range (10):

    for x in range (2):

        a_armpit = a_i + b_armpit*m.sin(x*w_i + c_i)
        a_elbow = a_i + b_elbow*m.sin(x*w_i + c_i)
        a_knee = a_i + b_knee*m.sin(x*w_i + c_i)

        p.setJointMotorControlArray(robotId, )



    shoulders_one = 0.4*m.sin(i*0.1)
    p.setJointMotorControlArray(robotId, 1, controlMode=mode, targetPosition=shoulders_one)
    p.setJointMotorControl2(robotId, 10, controlMode=mode, targetPosition=shoulders_one)

    shoulders_two = -0.4*m.sin(i*0.1)
    p.setJointMotorControl2(robotId, 7, controlMode=mode, targetPosition=shoulders_two)
    p.setJointMotorControl2(robotId, 4, controlMode=mode, targetPosition=shoulders_two)

    knees_one = 0.3*m.sin(i*0.1)
    p.setJointMotorControl2(robotId, 2, controlMode=mode, targetPosition=knees_one)
    p.setJointMotorControl2(robotId, 11, controlMode=mode, targetPosition=knees_one)

    knees_two = -0.3*m.sin(i*0.1)
    p.setJointMotorControl2(robotId, 8, controlMode=mode, targetPosition=knees_two)
    p.setJointMotorControl2(robotId, 5, controlMode=mode, targetPosition=knees_two)

    time.sleep(timediff)
    # time.sleep(1./1000.)

    robotPos, robotOrn = p.getBasePositionAndOrientation(robotId)

    # if i %100 == 0:
    positions.append(np.array(robotPos)) # append (x, y, z) position
    angles.append(p.getEulerFromQuaternion(robotOrn)[2]) # append just the yaw (roll, pitch, yaw)
    times.append(time.time())

    states = p.getJointStates(robotId, id_revolute_joints)
    for j in range(len(states)):
        sj = states[j]
        joint_torques[j].append(sj[3])
        joint_positions[j].append(sj[0])


pos_diffs = []
ang_diffs = []
time_diffs = []
speeds = []
## Calculate angle and position differences
for t in range(1, len(positions)):
    pos_diff = np.linalg.norm(positions[t]-positions[t-1])
    pos_diffs.append(pos_diff)
    time_diff = times[t]-times[t-1]
    time_diffs.append(time_diff)
    angle_diff = angles[t]-angles[t-1]
    ang_diffs.append(angle_diff)
    speed = pos_diff / time_diff
    speeds.append(speed)

## speed plot
print("Average Speed:", np.mean(speeds))
plt.plot(times[1:], speeds)
plt.title("Speed over Time")
plt.ylabel("Speed (m/s)")
plt.xlabel("Time (s)")
plt.savefig("speed.png")
plt.clf()

## joint torque plot
for y_arr, label in zip(joint_torques, label_list):
    plt.plot(times[:], y_arr, label=label)
plt.title("Joint Torque over Time")
plt.ylabel("Torque")
plt.xlabel("Time (s)")
plt.legend()
plt.savefig("joint-torque.png")
plt.clf()

## joint position plot
for y_arr, label in zip(joint_positions, label_list):
    plt.plot(times[:], y_arr, label=label)
plt.title("Joint Position over Time")
plt.ylabel("Position (rad)")
plt.xlabel("Time (s)")
plt.legend()
plt.savefig("joint-position.png")
plt.clf()

robotPos, robotOrn = p.getBasePositionAndOrientation(robot)

p.disconnect()
