import pybullet as p
import time
import pybullet_data
import math as m
import random as r
import pandas as pd

physicsClient = p.connect(p.DIRECT)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-10)
planeId = p.loadURDF("../plane/plane.urdf")

robotStartPos = [0,0,0.2]
robotStartOrientation = p.getQuaternionFromEuler([0,0,0])
robotId = p.loadURDF("../../robot/PP/urdf/PP.urdf", robotStartPos, robotStartOrientation)
mode = p.POSITION_CONTROL

number_of_joints = p.getNumJoints(robotId)
print("Running...")

for i in range (100):
    p.stepSimulation()

robotPos1, robotOrn1 = p.getBasePositionAndOrientation(robotId)

id_revolute_joints = [0, 3, 6, 9, 
                      1, 4, 7, 10, 
                      2, 5, 8, 11]

best_speeds = []
speeds = []
evals = []
s_max = 0
time_diff, t_0, t = 0, 0, 0

# a = a_i + b_i*m.sin(i*w + c_i)
a_i_armpit, a_i_elbow, a_i_knee = r.uniform(0.01,0.4), r.uniform(0.01,0.4), r.uniform(0.01,0.4)
b_armpit = r.uniform(0.01, 0.6)
b_elbow = r.uniform(0.01, 1.2)
b_knee = r.uniform(0.01, 1)
c_i_armpit, c_i_elbow, c_i_knee = r.uniform(0.01,1), r.uniform(0.01,1), r.uniform(0.01,1)
w_i = r.uniform(0.001,0.1)
#a_i_armpit, a_i_elbow, a_i_knee, b_armpit, b_elbow, b_knee, c_i_armpit, c_i_elbow, c_i_knee, w_i = 0.1909144863915157, 0.1263090150475257, 0.1026499531813916, 0.15782720238573084, 0.9266967189637338, 0.09913127680073877, 0.3692896172772866, 0.874847218866104, 0.37648274099281526, 0.07540533055525535
a_i_a, a_i_e, a_i_k, b_a, b_e, b_k, c_i_a, c_i_e, c_i_k, w = a_i_armpit, a_i_elbow, a_i_knee, b_armpit, b_elbow, b_knee, c_i_armpit, c_i_elbow, c_i_knee, w_i

count = 0


for i in range(1000):

    for x in range(1000):
        p.stepSimulation()

        armpit = a_i_armpit + b_armpit*m.sin(x*w_i + c_i_armpit)
        elbow = a_i_elbow + b_elbow*m.sin(x*w_i + c_i_elbow)
        knee = a_i_knee + b_knee*m.sin(x*w_i + c_i_knee)
        p.setJointMotorControlArray(robotId, id_revolute_joints, controlMode=mode, targetPositions=[-armpit, -armpit, armpit, armpit, elbow, -elbow, -elbow, elbow, knee, -knee, -knee, knee])

        if (x==0):
            t_0 = time.time()
        if (x==999):
            t = time.time()

    robotPos2, robotOrn2 = p.getBasePositionAndOrientation(robotId)

    # Calculate distance travelled
    x = robotPos2[0]-robotPos1[0]
    y = robotPos2[1]-robotPos1[1]
    dis = (x**2 + y**2)**0.5
    # Calculate time passed
    time_diff = t-t_0
    # Calculate speed
    s = dis/time_diff

    print(s)

    if (s>s_max):
        count = 0

        s_max = s
        best_speeds.append(s_max)
        speeds.append(s)
        evals.append(i)
        print(a_i_armpit, a_i_elbow, a_i_knee, b_armpit, b_elbow, b_knee, c_i_armpit, c_i_elbow, c_i_knee, w_i)
        a_i_a, a_i_e, a_i_k, b_a, b_e, b_k, c_i_a, c_i_e, c_i_k, w = a_i_armpit, a_i_elbow, a_i_knee, b_armpit, b_elbow, b_knee, c_i_armpit, c_i_elbow, c_i_knee, w_i
        a = r.randint(1,10)
        b = r.randint(0,1)
        
        if a==1:
            if b==0:
                a_i_armpit += 0.01
            if b==1:
                a_i_armpit -= 0.01
        elif a==2:
            if b==0:
                a_i_elbow += 0.01
            if b==1:
                a_i_elbow -= 0.01
        elif a==3:
            if b==0:
                a_i_knee += 0.01
            if b==1:
                a_i_knee -= 0.01
        elif a==4:
            if b==0:
                b_armpit += 0.01
            if b==1:
                b_armpit -= 0.01
        elif a==5:
            if b==0:
                b_elbow += 0.01
            if b==1:
                b_elbow -= 0.01
        elif a==6:
            if b==0:
                b_knee += 0.01
            if b==1:
                b_knee -= 0.01
        elif a==7:
            if b==0:
                c_i_armpit += 0.01
            if b==1:
                c_i_armpit -= 0.01
        elif a==8:
            if b==0:
                c_i_elbow += 0.01
            if b==1:
                c_i_elbow -= 0.01
        elif a==9:
            if b==0:
                c_i_knee += 0.01
            if b==1:
                c_i_knee -= 0.01
        else:
            if b==0:
                w_i += 0.01
            if b==1:
                w_i -= 0.01

    else:
        count+=1
        a_i_armpit, a_i_elbow, a_i_knee, b_armpit, b_elbow, b_knee, c_i_armpit, c_i_elbow, c_i_knee, w_i = a_i_a, a_i_e, a_i_k, b_a, b_e, b_k, c_i_a, c_i_e, c_i_k, w
        best_speeds.append(s_max)
        speeds.append(s)
        evals.append(i)

        if count>100:
            a_i_armpit, a_i_elbow, a_i_knee = r.uniform(0.01,0.4), r.uniform(0.01,0.4), r.uniform(0.01,0.4)
            b_armpit = r.uniform(0.01, 0.6)
            b_elbow = r.uniform(0.01, 1.2)
            b_knee = r.uniform(0.01, 1)
            c_i_armpit, c_i_elbow, c_i_knee = r.uniform(0.01,1), r.uniform(0.01,1), r.uniform(0.01,1)
            w_i = r.uniform(0.001,0.1)



    p.resetBasePositionAndOrientation(robotId, robotPos1, robotOrn1)
        

df = pd.DataFrame({"Best Overall Speed" : best_speeds, "Speeds" : speeds, "Number of Evaluations" : evals})
df.to_csv("HillClimber_1000.csv", index=False)



p.disconnect()

"""
        """
