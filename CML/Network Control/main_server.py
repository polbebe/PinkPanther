import gym
import gym.spaces as spaces
import sys

import socket

from _thread import *
import os

import csv

import numpy as np
import pandas as pd
import math as m
import time
import random

class Interface:
    def __init__(self, host='128.59.145.148', port=8123, act_dim=1, state_dim=1):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        msg = self.s.recv(1024)
        d = np.array([state_dim, act_dim], dtype=np.int)
        if msg == b'Init':
            print(d)
            self.s.sendall(d.tobytes())

    def get_action(self, obs, r, done):
        self.update(obs, r, done)
        action = np.frombuffer(self.s.recv(1024), dtype=np.float32)
        return action

    def update(self, obs, r, done):
        state = np.zeros(len(obs)+2, dtype=np.float32)
        state[:-2] = obs
        state[-2] = r
        if done:
            state[-1] = 1
        self.s.sendall(state.tobytes())

class Agent:
    def __init__(self, act_dim, state_dim, interface=None):
        self.act_dim, self.state_dim = act_dim, state_dim
        self.interface = interface

    def policy(self, state, train=True):
        if train:
            return np.random.uniform(-1, 1, self.act_dim)
        else:
            return self.interface.get_action(state)

class NetEnv(gym.Env):
    def __init__(self):
        # Servo positions that will be sent to client
        self.servo_pos = np.array([500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500], dtype=np.float32)
        self.servo_pos_0 = np.array([510, 750, 583, 500, 250, 417, 500, 750, 583, 500, 250, 417], dtype=np.float32)
        # abs(Value) of random change between robot positions
        self.delta_pos = 25
        self.act_dim = 12
        self.state_dim = 17
        self.ep_len = 200

        # Robot State values that will be bounced with client
        self.robot_state = np.zeros(self.state_dim, dtype=np.float32)

        # Socket Conneciton
        # MAC find WiFi IP - ipconfig getifaddr en0
        HOST = '192.168.1.29'
        # Port to listen on (non-privileged ports are > 1023)
        PORT = 65432
        print('Connected')

        # Set up Socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((HOST, PORT))
        except socket.error as e:
            print(str(e))

        print('Waiting for connection[s]...')

        self.s.listen()

        # Wait for client[s] to join socket
        self.conn1, addr1 = self.s.accept()
        print('Connected by: ', addr1)
        start_new_thread(self.main_client_thread, (self.conn1,))

        self.conn2, addr2 = self.s.accept()
        print('Connected by: ', addr2)
        start_new_thread(self.cam_client_thread, (self.conn2,))

    def main_client_thread(self, conn):
        # Send motor position to main client
        conn.sendall(self.servo_pos.tobytes())
        # Receive Robot State from main client
        pp_state = np.frombuffer(conn.recv(1024), dtype=np.float32)
        for i in range(15):
            self.robot_state[i] = pp_state[i]

    def cam_client_thread(self, conn):
        # Send connection test to cam client
        conn.sendall(str.encode('i'))
        # Receive xy state from cam client & append to Robot State
        cam_state = np.frombuffer(conn.recv(1024), dtype=np.float32)
        if m.isnan(cam_state[0]) != True:
            self.robot_state[15] = cam_state[0]
            self.robot_state[16] = cam_state[1]

    def reset(self):
        # Set robot to position
        # Stand down
        self.servo_pos = np.array([500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500], dtype=np.float32)
        self.main_client_thread(self.conn1)
        time.sleep(1)
        # Stand up
        self.servo_pos = np.array([510, 750, 583, 500, 250, 417, 500, 750, 583, 500, 250, 417], dtype=np.float32)
        self.main_client_thread(self.conn1)
        self.i = 0

    def step(self, action):
        self.i += 1
        # MAIN CLIENT
        # Move motors to current position plus RANDOM delta_pos
        self.servo_pos += self.delta_pos * action

        self.servo_pos_0 = self.servo_pos
        self.write_csv_theory(self.servo_pos_0)

        # Send new position data to clients
        self.main_client_thread(self.conn1)

        # CAM CLIENT
        # Get xy position from camera
        self.cam_client_thread(self.conn2)
        done = self.i >= self.ep_len
        r = self.robot_state[-1] # the y position of the robot state serves as the reward

        return self.robot_state, r, done, {}

    def write_csv_theory(self, data):
        with open('theory.csv', 'a') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(data)


if __name__ == '__main__':
    # A parameter to determine if we read actions from the server or select them randomly
    train = True

    # Construct MAIN SERVER object
    env = NetEnv()

    # Setting up the interface if we are in test mode
    if train:
        interface = None
    else:
        interface = Interface(act_dim=env.act_dim, state_dim=env.state_dim)

    # Construct Agent object
    agent = Agent(env.act_dim, env.state_dim, interface)

    # Reset environment
    obs = env.reset()

    # Get input from user
    input('Press any key to begin episode: ')


    def write_csv_real(data):
        with open('real.csv', 'a') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(data)


    # Keep track of time for average actions/second calculation
    start = time.time()
    j = 0
    # WALK
    for i in range(200):
        # Return current robot state on every loop
        action = agent.policy(obs)
        # if we want every 3rd to be frozen
        action[0::3] = 0

        obs = env.step(action)
        # Print only every 10 loops
        # if i%10 == 0:
        # print(r_state)
        write_csv_real(obs)
        j += 1
        # Keep track of number of actions/second
        sys.stdout.write(str(i) + ' in: ' + str(round(time.time() - start, 3)) + ' Averaging: ' + str(
            round(j / (time.time() - start), 2)) + ' actions/s\r')

    print('Done')
