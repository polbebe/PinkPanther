import pybullet as p
import time
import pybullet_data
import math as m
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import random

def init_individual():
    return list(np.random.uniform(-0.5, 0.5, 12))


def init_population(n=1000):
    return [init_individual() for i in range(n)]


def choose_fittest(pop, k=100):

    physicsClient = p.connect(p.DIRECT)

    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0,0,-10)
    planeId = p.loadURDF("../plane/plane.urdf")

    robotStartPos = [0,0,0.2]
    robotStartOrientation = p.getQuaternionFromEuler([0,0,0])
    robotId = p.loadURDF("../../robot/PP/urdf/PP.urdf", robotStartPos, robotStartOrientation)
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
            nv.append(np.random.uniform(-0.5, 0.5))
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

    robotStartPos = [0,0,0.2]
    robotStartOrientation = p.getQuaternionFromEuler([0,0,0])
    p.resetBasePositionAndOrientation(robotId, robotStartPos, robotStartOrientation)

    number_of_joints = p.getNumJoints(robotId)

    timediff = 1./2400.

    # torque info based off of https://github.com/bulletphysics/bullet3/blob/master/examples/pybullet/examples/inverse_dynamics.py
    # id_revolute_joints = [0, 9, 6, 3, 1, 10, 7, 4, 2, 11, 8, 5]
    id_revolute_joints = [1, 10, 7, 4, 2, 11, 8, 5]

    motor_labels = {0: "LEFT FRONT ARMPIT", 1: "LEFT FRONT SHOULDER", 2: "LEFT FRONT KNEE", 3:"RIGHT FRONT ARMPIT", 4: "RIGHT FRONT SHOULDER", 5:"RIGHT FRONT KNEE", 6:"LEFT BACK ARMPIT", 7:"LEFT BACK SHOULDER", 8:"LEFT BACK KNEE", 9:"RIGHT BACK ARMPIT", 10:"RIGHT BACK SHOULDER", 11:"RIGHT BACK KNEE"}

    maxz = 0

    for i in range (steps):
        p.stepSimulation()

        shoulders_one_1 = v[0] + v[1]*m.sin(i*0.1 + v[2])
        p.setJointMotorControl2(robotId, 1, controlMode=mode, targetPosition=shoulders_one_1)
        p.setJointMotorControl2(robotId, 10, controlMode=mode, targetPosition=shoulders_one_1)

        shoulders_two_1 = v[3] + v[4]*m.sin(i*0.1 + v[5])
        p.setJointMotorControl2(robotId, 7, controlMode=mode, targetPosition=shoulders_two_1)
        p.setJointMotorControl2(robotId, 4, controlMode=mode, targetPosition=shoulders_two_1)

        knees_one_1 = v[6] + v[7]*m.sin(i*0.1 + v[8])
        p.setJointMotorControl2(robotId, 2, controlMode=mode, targetPosition=knees_one_1)
        p.setJointMotorControl2(robotId, 11, controlMode=mode, targetPosition=knees_one_1)

        knees_two_1 = v[9] + v[10]*m.sin(i*0.1 + v[11])
        p.setJointMotorControl2(robotId, 8, controlMode=mode, targetPosition=knees_two_1)
        p.setJointMotorControl2(robotId, 5, controlMode=mode, targetPosition=knees_two_1)

        robotPos, robotOrn = p.getBasePositionAndOrientation(robotId)

        if robotPos[2] > maxz:
            maxz = robotPos[2]

        if gui:
            # time.sleep(1./1000.)
            time.sleep(timediff)
        else:
            pass

    robotPos, robotOrn = p.getBasePositionAndOrientation(robotId)
    score = np.linalg.norm(np.array([robotPos[0], robotPos[1]]))/maxz
    return score

if __name__ == "__main__":

    weights, score = genetic(e=10000, n=1000)

    # GUI SIMULATION

    physicsClient = p.connect(p.GUI)

    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0,0,-10)
    planeId = p.loadURDF("../plane/plane.urdf")

    robotStartPos = [0,0,0.2]
    robotStartOrientation = p.getQuaternionFromEuler([0,0,0])
    robotId = p.loadURDF("../../robot/PP/urdf/PP.urdf", robotStartPos, robotStartOrientation)
    mode = p.POSITION_CONTROL

    vars = {"pc": physicsClient,
            "plane": planeId,
            "rid": robotId,
            "mode": mode}

    score = evaluate_fitness(weights, vars, gui=True, steps=10000)

    p.disconnect()
