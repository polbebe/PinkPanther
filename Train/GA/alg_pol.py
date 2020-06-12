import pybullet as p
import time
import pybullet_data
import math as m
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import random
import scipy.stats as sp
import pandas as pd


def init_individual():
    return list(np.random.uniform(-0.5, 0.5, 37))


def init_population(n):
    return [init_individual() for i in range(n)]


def mutate(v, p):
    nv = []
    for i in range(len(v)):
        if np.random.uniform(0.0, 1.0) <= p:
            nv.append(np.random.uniform(-0.5, 0.5))
        else:
            nv.append(v[i])
    return nv


def crossover(v1, v2, p):
    if np.random.uniform(0.0, 1.0) <= p:
        i = random.choice(list(range(len(v1))))
        new = v1[0:i] + v2[i:len(v2)]
    else:
        new = v1
    return new


def evaluate_fitness(v, robotId, mode, r_pos1, r_orn1):

    #motor_labels = {0: "LEFT FRONT ARMPIT", 1: "LEFT FRONT SHOULDER", 2: "LEFT FRONT KNEE",
    #               3:"RIGHT FRONT ARMPIT", 4: "RIGHT FRONT SHOULDER", 5:"RIGHT FRONT KNEE",
    #               6:"LEFT BACK ARMPIT", 7:"LEFT BACK SHOULDER", 8:"LEFT BACK KNEE",
    #               9:"RIGHT BACK ARMPIT", 10:"RIGHT BACK SHOULDER", 11:"RIGHT BACK KNEE"}

    # Keep track of max z-value & y-value to penalize jumping & weird gaits
    maxz=0
    maxy=0

    # t_start = time.time()

    # Simulate using values given
    for i in range(1000):
        
        p.stepSimulation()

        armpit_lf = v[0] + v[1]*m.sin(i*v[36] + v[2])
        p.setJointMotorControl2(robotId, 0, controlMode=mode, targetPosition=armpit_lf)
        elbow_lf = v[3] + v[4]*m.sin(i*v[36] + v[5])
        p.setJointMotorControl2(robotId, 1, controlMode=mode, targetPosition=elbow_lf)
        knee_lf = v[6] + v[7]*m.sin(i*v[36] + v[8])
        p.setJointMotorControl2(robotId, 2, controlMode=mode, targetPosition=knee_lf)

        armpit_rf = v[9] + v[10]*m.sin(i*v[36] + v[11])
        p.setJointMotorControl2(robotId, 3, controlMode=mode, targetPosition=armpit_rf)
        elbow_rf = v[12] + v[13]*m.sin(i*v[36] + v[14])
        p.setJointMotorControl2(robotId, 4, controlMode=mode, targetPosition=elbow_rf)
        knee_rf = v[15] + v[16]*m.sin(i*v[36] + v[17])
        p.setJointMotorControl2(robotId, 5, controlMode=mode, targetPosition=knee_rf)

        armpit_lb = v[18] + v[19]*m.sin(i*v[36] + v[20])
        p.setJointMotorControl2(robotId, 6, controlMode=mode, targetPosition=armpit_lb)
        elbow_lb = v[21] + v[22]*m.sin(i*v[36] + v[23])
        p.setJointMotorControl2(robotId, 7, controlMode=mode, targetPosition=elbow_lb)
        knee_lb = v[24] + v[25]*m.sin(i*v[36] + v[26])
        p.setJointMotorControl2(robotId, 8, controlMode=mode, targetPosition=knee_lb)

        armpit_rb = v[27] + v[28]*m.sin(i*v[36] + v[29])
        p.setJointMotorControl2(robotId, 9, controlMode=mode, targetPosition=armpit_rb)
        elbow_rb = v[30] + v[31]*m.sin(i*v[36] + v[32])
        p.setJointMotorControl2(robotId, 10, controlMode=mode, targetPosition=elbow_rb)
        knee_rb = v[33] + v[34]*m.sin(i*v[36] + v[35])
        p.setJointMotorControl2(robotId, 11, controlMode=mode, targetPosition=knee_rb)

        # Update with highest z-value of simulation
        robotPos, robotOrn = p.getBasePositionAndOrientation(robotId)
        if robotPos[2] > maxz:
            maxz = robotPos[2]
        if abs(robotPos[1]) > maxy:
            maxy = abs(robotPos[1])

    # Calculate x-distance and y-distance traveled
    r_pos2, r_orn2 = p.getBasePositionAndOrientation(robotId)
    x = r_pos2[0]-r_pos1[0]
    y = r_pos2[1]-r_pos1[1]

    # Calculate score & penalize for high z-values and y-distance traveled
    # (We want the robot to walk straight and on the ground)
    score = np.linalg.norm(np.array([x, y]))/(maxz+maxy)

    # Calculate speed
    # t_finish = time.time()
    # speed = ((x**2 + y**2)**0.5)/(t_finish - t_start)

    # Move robot back to origin
    p.resetBasePositionAndOrientation(robotId, r_pos1, r_orn1)

    return score


def choose_fittest(pop):
    # Start simulation and get original position of robot
    physicsClient = p.connect(p.DIRECT)
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0,0,-10)
    planeId = p.loadURDF("../plane/plane.urdf")
    robotStartPos = [0,0,0.2]
    robotStartOrientation = p.getQuaternionFromEuler([0,0,0])
    robotId = p.loadURDF("../../robot/PP/urdf/PP.urdf", robotStartPos, robotStartOrientation)
    mode = p.POSITION_CONTROL
    for i in range (10):
        p.stepSimulation()
    r_pos1, r_orn1 = p.getBasePositionAndOrientation(robotId)    
    
    # List with all scores
    eval_list = []
    
    # max_speed = 0
    # Iterate through population and evaluate fitnesses of each offspring
    for i in tqdm(pop, desc="Population:"):
        score = evaluate_fitness(i, robotId, mode, r_pos1, r_orn1)
        eval_list.append((i, score))
        # if speed>max_speed:
        #    max_speed = speed

    # Sort eval list in inverse order (higher better)
    sl = [i for i in sorted(eval_list, key=lambda item: -item[1])]

    p.disconnect()

    # Return offsprings in decreasing score order
    return sl


def genetic(e, n, k):
    
    # Initialize population
    pop = init_population(n)

    # Instantiate tracker for best score & values
    best_score = 0
    best_values = None

    # speeds = []
    scores = []
    epochs = []
    standard_errors = []
    st_epochs = []
    st_scores = []

    # Iterate through epochs by performing genetic selection 
    for i in range(e):
        print("Iter {}/{}".format(i+1, e))

        fit = choose_fittest(pop)

        # Get values of offspring in population
        fit_pop = [j[0] for j in fit]

        # Get the scores of population
        fit_scores = [j[1] for j in fit]

        # Best score in epoch
        best_e_score = fit_scores[0]

        # Update best score and values
        if best_e_score > best_score:
            best_score = best_e_score
            best_values = fit_pop[0]
        
        # Print for tracking
        # print("Best Overall Values: {}".format(best_values))

        print("Average Epoch Score: {}".format(np.mean(fit_scores)))
        print("Best Epoch Score: {}".format(best_e_score))
        print("Best Overall Score: {}".format(best_score))
        # print("Best Epoch Speed: {} [m/s]".format(best_speed))

        print("Best Overall Values: {}".format(best_values))

        # Add values to list for plot
        # Keep track of epoch
        epochs.append(int(i+1))
        # Keep track of best score
        scores.append(best_score)

        # If the epoch is a multiple of 200 we calculate the standard error to display in the final plot
        if (i%100)==0:
            standard_errors.append(sp.sem(fit_scores))
            st_epochs.append(i+1)
            st_scores.append(best_score)

        # Create new population
        new_pop = []

        # Crossover
        crosses = []
        for j in range(90):
            x = random.randint(0, k-1)
            y = random.randint(0, k-1)
            crosses.append(crossover(fit_pop[x], fit_pop[y], p=0.6))

        # Populate with crossed k-best from previous population
        new_pop += crosses

        # Mutations
        for j in new_pop:
            j = mutate(j, p=0.001)

        # Add a few other random offspring to the population
        new_pop += init_population(n=10)

        # Update population
        pop = new_pop

        print("Population Reproduced ({})".format(len(new_pop)))

    return best_values, best_score, scores, epochs, standard_errors, st_epochs, st_scores


if __name__ == "__main__":

    # Call genetic algorithm and get best values & score as well as arrays to plot progress
    values, score, scores, epochs, standard_errors, st_epochs, st_scores = genetic(1000, 100, 10)

    # print("MAX SCORE WAS {}".format(score))

    # Keep track of version easily
    version = "0.0.3"

    # Plot - Graph, Errorbars & Labels
    plt.errorbar(st_epochs, st_scores, yerr=standard_errors, fmt='+', color = "red", capsize=2)
    plt.plot(epochs, scores, linewidth = 2.5, color = "green")
    # plt.plot(epochs, speeds, linewidth = 0.5, color = "blue")
    plt.title("Genetic Algorithm {} - Population 100, k-best 10, xo 0.6, mut 0.001".format(version))
    plt.ylabel("Fitness score")
    plt.xlabel("Epoch")

    # Save plot for reference
    plt.savefig("GA_Test_{}.png".format(version))
    plt.clf()

    # Save best values as csv for simulation
    df = pd.DataFrame({"Best Values" : values})
    df.to_csv("GA_Test_{}.csv".format(version), index=[0])


	