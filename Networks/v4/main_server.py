import socket
import numpy as np
import pandas as pd
import math as m
import time
import gym
import gym.spaces as spaces
import sys
import torch
from _thread import *

class NetEnv(gym.Env):

    def __init__(self, port):
        HOST = '192.168.1.29'   # Standard loopback interface address (localhost)
                                # Mac - 192.168.1.29
        PORT = port             # Port to listen on (non-privileged ports are > 1023)

        # Master array with all robot inputs from clients
        self.robot_inputs = None
        self.robot_outputs = np.zeros(15, dtype=np.float32)

        print('Connected')

        # Set up Socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))

        print('Waiting for connection[s]...')
        
        self.s.listen(4)
        self.conn, addr = self.s.accept()
        print('Connected by: ', addr)

        self.i = 0

        # Read v values from those saved from simulation
        #version= "0.2.1"
        #df = pd.read_csv('V/Hardcoded_{}.csv'.format(version))
        #v = np.array(df['Best Values'], dtype=np.float32)


    def threaded_client(self):
        self.conn.send(str.encode('Welcome to the Server\n'))
        while True:
            data = self.conn.recv(2048)
            reply = 'Server Says: ' + data.decode('utf-8')
        if not data:
            break
            self.conn.sendall(str.encode(reply))
        self.conn.close()


    def reset(self):
        # Make robot stand up
        input('Press enter to begin episode: ')
        self.i = 0

        self.robot_inputs = None

        return self.robot_inputs


    def step(self, action):

        # Functions for servo position conversion
        def servo12(targ12):
            if targ12>=0:
                pos12 = 140 - (targ12/1.2)*65
            else:
                pos12 = (abs(targ12)/1)*25 + 140
            return pos12
        def servo11(targ11):
            if targ11>=0:
                pos11 = (targ11/1.5)*60 + 180
            else:
                pos11 = 180 - (abs(targ11)/0.6)*40
            return pos11
        def servo32(targ32):
            if targ32>=0:
                pos32 = 140 - (targ32/1.2)*65
            else:
                pos32 = (abs(targ32)/1)*25 + 140
            return pos32
        def servo31(targ31):
            if targ31>=0:
                pos31 = (targ31/1.5)*60 + 180
            else:
                pos31 = 180 - (abs(targ31)/0.6)*40
            return pos31
        def servo22(targ22):
            if targ22>=0:
                pos22 = (targ22/1.2)*65 + 100
            else:
                pos22 = 100 - (abs(targ22)/1)*25
            return pos22
        def servo21(targ21):
            if targ21>=0:
                pos21 = 60 - (targ21/1.5)*60
            else:
                pos21 = (abs(targ21)/0.6)*60 + 60
            return pos21
        def servo42(targ42):
            if targ42>=0:
                pos42 = (targ42/1.2)*65 + 100
            else:
                pos42 = 100 - (abs(targ42)/1)*25
            return pos42
        def servo41(targ41):
            if targ41>=0:
                pos41 = 60 - (targ41/1.5)*60
            else:
                pos41 = (abs(targ41)/0.6)*60 + 60
            return pos41

        # Receive motor positions
        robot_in = self.conn.recv(1024)
        self.robot_inputs = np.frombuffer(robot_in, dtype=np.float32)

        # Calculate servo positions
        #self.robot_outputs[0] = 0
        self.robot_outputs[1] = servo12(v[3] + v[4]*m.sin(self.i*v[36] + v[5]))
        self.robot_outputs[2] = servo11(v[6] + v[7]*m.sin(self.i*v[36] + v[8]))
        #self.robot_outputs[3] = 0
        self.robot_outputs[4] = servo22(v[12] + v[13]*m.sin(self.i*v[36] + v[14]))
        self.robot_outputs[5] = servo21(v[15] + v[16]*m.sin(self.i*v[36] + v[17]))
        #self.robot_outputs[6] = 0
        self.robot_outputs[7] = servo32(v[21] + v[22]*m.sin(self.i*v[36] + v[23]))
        self.robot_outputs[8] = servo31(v[24] + v[25]*m.sin(self.i*v[36] + v[26]))
        #self.robot_outputs[9] = 0
        self.robot_outputs[10] = servo42(v[30] + v[31]*m.sin(self.i*v[36] + v[32]))
        self.robot_outputs[11] = servo41(v[33] + v[34]*m.sin(self.i*v[36] + v[35]))

        # Prepare and send position data to clients
        self.conn.sendall(self.robot_outputs.tobytes())

        self.i += 1

        return self.robot_inputs


if __name__ == '__main__':
    env = NetEnv(65432)

    start = time.time()
    
    robot_inputs = env.reset()
    # print(motor_inputs)
    
    # Read v values from those saved from simulation
    version= "0.2.1"
    df = pd.read_csv('V/Hardcoded_{}.csv'.format(version))
    v = np.array(df['Best Values'], dtype=np.float32)
    
    # Walk
    for i in range(400):
        robot_inputs = env.step(v)
        #print(motor_inputs)
        sys.stdout.write(str(i)+' in: '+str(round(time.time()-start,3))+' Averaging: '+str(round(i/(time.time()-start),2))+' actions/s\r')
    
    print('Done')

