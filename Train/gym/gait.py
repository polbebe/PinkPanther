import pybullet as p
import time
import pybullet_data
import math as m

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.setGravity(0,0,-10)
planeId = p.loadURDF("../plane/plane.urdf")

robotStartPos = [0,0,0.17]
robotStartOrientation = p.getQuaternionFromEuler([0,0,0])
robotId = p.loadURDF("../../robot/PP/urdf/PP.urdf", robotStartPos, robotStartOrientation)
mode = p.POSITION_CONTROL

number_of_joints = p.getNumJoints(robotId)
print("Joints:", number_of_joints)

id_revolute_joints = [0, 3, 6, 9, 
                      1, 4, 7, 10, 
                      2, 5, 8, 11]

for i in range (1000):
    p.stepSimulation()
    
    a_i_armpit, a_i_elbow, a_i_knee, b_armpit, b_elbow, b_knee, c_i_armpit, c_i_elbow, c_i_knee, w_i = 0.384862158673826, 0.03440521089212785, 0.15273111817703294, 0.20806758273652906, 1.0304542528924263, 0.9415471616488548, 0.6060474178564257, 0.49639248087663834, 0.407814219572063, 0.08816940199045416
    armpit = a_i_armpit + b_armpit*m.sin(i*w_i + c_i_armpit)
    elbow = a_i_elbow + b_elbow*m.sin(i*w_i + c_i_elbow)
    knee = a_i_knee + b_knee*m.sin(i*w_i + c_i_knee)
    p.setJointMotorControlArray(robotId, id_revolute_joints, controlMode=mode, targetPositions=[-armpit, -armpit, armpit, armpit, elbow, -elbow, -elbow, elbow, knee, -knee, -knee, knee])


    time.sleep(1./1000.)

robotPos, robotOrn = p.getBasePositionAndOrientation(robot)
print(robotPos,robotOrn)
p.disconnect()
