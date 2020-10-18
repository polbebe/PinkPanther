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
robotId = p.loadURDF("../../robot/PinkPanther_CML/urdf/PinkPanther_CML.urdf", robotStartPos, robotStartOrientation)
mode = p.POSITION_CONTROL
maxForce = 4

# Calculate speed
t_start = time.time()
for i in range (10):
    p.stepSimulation()
robotPos1, robotOrn1 = p.getBasePositionAndOrientation(robotId)


# Read csv and output simulation
version = "0.0.1"

df = pd.read_csv('GA_Tests/GA_Test_{}.csv'.format(version))
#v = df['Best Values'].to_numpy()
#v =[-0.2009856716799462, -0.42380313808994585, -0.20429331023107533, -0.0865320943872242, -0.4476510535960674, 0.07394548405412149, 0.15856378454551812, -0.20785706144575133, 0.23193770724432583, 0.23581638096935964, 0.19562933456450127, 0.4465649428748457, 0.07012919174528676, -0.47229568854048765, -0.21689597923406945, 0.00967153173745472, -0.019104394552737936, -0.2015382947426838, -0.07621998746776959, 0.3136788864241655, 0.39158932472182173, -0.34146025245310807, -0.4743226072899087, 0.1891213238996594, 0.43284614685821055, 0.3341928408201542, 0.037280493798719005, -0.19275752067351093, -0.0877730166289078, -0.33731421409508844, -0.2873460508513829, 0.2533766288416516, 0.051959094966924524, -0.2085325433354519, -0.031999403914061086, -0.22252218720271455, -0.325258712877482]

v = [0.400434475339851, -0.48012541892068883, -0.4366752039175952, 0.3948792597272651, -0.0005697132326367704, -0.31540692267358295, -0.4143320455608217, 0.41417634859739383, -0.27564781016453055, 0.15696859083215708, 0.12788423764217327, -0.2326626320108084, 0.41267866493933547, 0.193160759330408, -0.38827641806108615, 0.3290511552518858, 0.3436318673020017, 0.05818241872038321, 0.0854146809570806, -0.47816488273020274, 0.3512120255761688, 0.13657113531664755, -0.22831434503234171, 0.3647587902800764, -0.36683778323988925, 0.38348744247505195, -0.4622140695298874, 0.051531371432123385, 0.28345797552473795, -0.20606204975773235, 0.04628893393973221, -0.06797886675477893, 0.26292187839874337, -0.41576783454043054, -0.3675496856248778, -0.024666098682105564, -0.37336365036094965]

for i in range (1000):
    p.stepSimulation()

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

t_finish = time.time()
robotPos2, robotOrn2 = p.getBasePositionAndOrientation(robotId)

# Calculate speed
x = robotPos2[0]-robotPos1[0]
y = robotPos2[1]-robotPos1[1]
dis = (x**2 + y**2)**0.5
t = t_finish - t_start
s = dis/t

print("Speed: ", s, "[m/s]")

p.disconnect()
