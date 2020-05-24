import pybullet as p
import time
import pybullet_data
import math as m
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import random

def init_individual():
    return list(np.random.uniform(-1, 1, 40))


def init_population(n=1000):
    return [init_individual() for i in range(n)]


def choose_fittest(pop, k=100):

    physicsClient = p.connect(p.DIRECT)

    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0,0,-10)
    planeId = p.loadURDF("../plane/plane.urdf")

    robotStartPos = [0,0,0.1]
    robotStartOrientation = p.getQuaternionFromEuler([0,0,0])
    robotId = p.loadURDF("../../robot/PinkPanther/urdf/PinkPanther.urdf", robotStartPos, robotStartOrientation)
    mode = p.POSITION_CONTROL

    vars = {"pc": physicsClient,
            "plane": planeId,
            "rid": robotId,
            "mode": mode}

    eval_list = []
    for i in tqdm(pop, desc="calc fitness"):
        score = evaluate_fitness(i, vars, gui=False)
        eval_list.append((i, score))
    sl = [i for i in sorted(eval_list, key=lambda item: -item[1])] # sort in inverse order (higher better)

    p.disconnect()

    return sl[:k] # take k best of inversely sorted list


def mutate(v, p):
    nv = []
    for i in range(len(v)):
        if np.random.uniform(0, 1) <= p:
            nv.append(np.random.uniform(-1, 1))
        else:
            nv.append(v[i])
    return nv


def crossover(v1, v2):
    i = random.choice(list(range(len(v1))))
    new = v1[0:i] + v2[i:len(v2)]
    return new


def genetic(e=10, n=1000):

    pop = init_population(n=n)
    print("Population Initialized ({})".format(n))

    best_score = 0
    best_weights = None

    for i in range(e):
        print("Iter {}/{}".format(i+1, e))

        new_pop = []

        fit = choose_fittest(pop, k=20)

        fit_scores = [j[1] for j in fit]
        fit_pop = [j[0] for j in fit]

        best_e_score = fit_scores[0]





        if best_e_score > best_score:
            best_score = best_e_score
            best_weights = fit_pop[0]



        print("Best Epoch Weights: {}".format(fit_pop[0]))
        print("Best Overall Weights: {}".format(best_weights))

        print("Best Epoch Score: {}".format(best_e_score))

        print("Average Epoch Score: {}".format(sum(fit_scores)/len(fit_scores)))

        print("Best Overall Score: {}".format(best_score))

        new_pop += fit_pop

        # get crossovers
        crosses = []
        for j in range(len(fit_pop)):
            for k in range(len(fit_pop)):
                if j==k:
                    continue
                crosses.append(crossover(fit_pop[j], fit_pop[k]))

        # add mutations
        for j in crosses:
            new_pop.append(mutate(j, p=0.01))

        # add 100 extra randos
        new_pop += init_population(n=100)

        pop = new_pop

        print("Population Reproduced ({})".format(len(new_pop)))

    return best_weights, best_score



def evaluate_fitness(v, vars, gui=False, steps=1000):
    # if gui:
    #     physicsClient = p.connect(p.GUI)
    # else:
    #

    physicsClient = vars["pc"]
    planeId = vars["plane"]
    robotId = vars["rid"]
    mode = vars["mode"]

    robotStartPos = [0,0,0.1]
    robotStartOrientation = p.getQuaternionFromEuler([0,0,0])
    p.resetBasePositionAndOrientation(robotId, robotStartPos, robotStartOrientation)

    number_of_joints = p.getNumJoints(robotId)

    timediff = 1./2400.

    # torque info based off of https://github.com/bulletphysics/bullet3/blob/master/examples/pybullet/examples/inverse_dynamics.py
    # id_revolute_joints = [0, 9, 6, 3, 1, 10, 7, 4, 2, 11, 8, 5]
    id_revolute_joints = [1, 10, 7, 4, 2, 11, 8, 5]

    motor_labels = {0: "LEFT FRONT ARMPIT", 1: "LEFT FRONT SHOULDER", 2: "LEFT FRONT KNEE", 3:"RIGHT FRONT ARMPIT", 4: "RIGHT FRONT SHOULDER", 5:"RIGHT FRONT KNEE", 6:"LEFT BACK ARMPIT", 7:"LEFT BACK SHOULDER", 8:"LEFT BACK KNEE", 9:"RIGHT BACK ARMPIT", 10:"RIGHT BACK SHOULDER", 11:"RIGHT BACK KNEE"}

    for i in range (steps):
        p.stepSimulation()

        shoulders_one_1 = v[0] + v[1]*m.sin(i*0.1 + v[2]) + v[3]*m.sin(i*0.2 + v[4])
        p.setJointMotorControl2(robotId, 1, controlMode=mode, targetPosition=shoulders_one_1)
        shoulders_one_2 = v[5] + v[6]*m.sin(i*0.1 + v[7]) + v[8]*m.sin(i*0.2 + v[9])
        p.setJointMotorControl2(robotId, 10, controlMode=mode, targetPosition=shoulders_one_2)

        shoulders_two_1 = v[10] + v[11]*m.sin(i*0.1 + v[12]) + v[13]*m.sin(i*0.2 + v[14])
        p.setJointMotorControl2(robotId, 7, controlMode=mode, targetPosition=shoulders_two_1)
        shoulders_two_2 = v[15] + v[16]*m.sin(i*0.1 + v[17]) + v[18]*m.sin(i*0.2 + v[19])
        p.setJointMotorControl2(robotId, 4, controlMode=mode, targetPosition=shoulders_two_2)

        knees_one_1 = v[20] + v[21]*m.sin(i*0.1 + v[22]) + v[23]*m.sin(i*0.2 + v[24])
        p.setJointMotorControl2(robotId, 2, controlMode=mode, targetPosition=knees_one_1)
        knees_one_2 = v[25] + v[26]*m.sin(i*0.1 + v[27]) + v[28]*m.sin(i*0.2 + v[29])
        p.setJointMotorControl2(robotId, 11, controlMode=mode, targetPosition=knees_one_2)

        knees_two_1 = v[30] + v[31]*m.sin(i*0.1 + v[32]) + v[33]*m.sin(i*0.2 + v[34])
        p.setJointMotorControl2(robotId, 8, controlMode=mode, targetPosition=knees_two_1)
        knees_two_2 = v[35] + v[36]*m.sin(i*0.1 + v[37]) + v[38]*m.sin(i*0.2 + v[39])
        p.setJointMotorControl2(robotId, 5, controlMode=mode, targetPosition=knees_two_2)

        if gui:
            # time.sleep(1./1000.)
            time.sleep(timediff)
        else:
            pass
        robotPos, robotOrn = p.getBasePositionAndOrientation(robotId)
        print(robotPos)

    robotPos, robotOrn = p.getBasePositionAndOrientation(robotId)
    score = np.linalg.norm(np.array([robotPos[0], robotPos[1]]))
    return score

if __name__ == "__main__":

    # weights, score = genetic(e=10000, n=1000)


    # best epoch (before penalyzing maxz) jumps really high
    weights = [0.21040180087740823, -0.9446687643761467, 0.6641847208951179, 0.9609068069549522, -0.5656890421573919, 0.9470588682665568, -0.045420280197167706, 0.8563212436469194, -0.21451864597661663, -0.2167490963441836, 0.4789389516295679, 0.6889388284409201, -0.2560192272480497, 0.8620320224596283, 0.08577803745030388, 0.6464102759564538, -0.2800443765744476, 0.6205556908810481, 0.6225803161163128, -0.5879707256706455, 0.2289983831770086, -0.8612275465893886, 0.11426184663916583, -0.9757452987726039, 0.46322423390457823, 0.3677761519868825, -0.5791232335826517, -0.7668672706614506, -0.9907569967659855, 0.5796454879434205, 0.31386528482886655, 0.8624305602511, 0.7200357466979683, 0.6272602783873988, 0.9749397859851938, 0.9558253649875179, -0.45268533520895105, -0.4206185873898505, 0.3033222871000745, 0.1483235039633677]


    # best current maxz penal Epoch
    weights =  [0.8531354514420946, 0.7370159637573237, 0.4141953778367373, -0.7683682490615529, -0.6234201167829638, 0.8311013055266401, 0.7161368986543761, 0.6906418446465281, -0.5377314950125132, 0.18085927978201943, 0.7068202652476707, -0.5523905103544131, -0.9887657307605062, 0.28136906473877343, -0.8199039625421876, 0.871746493636945, -0.6184634065258607, 0.821224952873649, 0.4826159365755647, -0.23629629220062687, 0.38722974128683263, 0.8556459509951244, -0.9308715465567776, -0.09821329849550953, -0.20241759006160542, 0.49976961410040666, 0.676611826792324, -0.8528500217837018, -0.7027672489911352, 0.3626776811935659, -0.7981778633554923, -0.41575115994267287, -0.08245372808284301, 0.17443592160902566, -0.8253756582020013, -0.19956343220504547, -0.6649893145228676, 0.4240731115675811, 0.7907615985199805, -0.2460933655545896]

    # GUI SIMULATION

    physicsClient = p.connect(p.GUI)

    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0,0,-10)
    planeId = p.loadURDF("../plane/plane.urdf")

    robotStartPos = [0,0,0.1]
    robotStartOrientation = p.getQuaternionFromEuler([0,0,0])
    robotId = p.loadURDF("../../robot/PinkPanther/urdf/PinkPanther.urdf", robotStartPos, robotStartOrientation)
    mode = p.POSITION_CONTROL

    vars = {"pc": physicsClient,
            "plane": planeId,
            "rid": robotId,
            "mode": mode}

    score = evaluate_fitness(weights, vars, gui=True, steps=1000)

    p.disconnect()
