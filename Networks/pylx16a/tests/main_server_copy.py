import gym
import gym.spaces as spaces
import sys

import socket

import numpy as np
import pandas as pd
import math as m
import time

class NetEnv(gym.Env):

    def __init__(self):
        # Socket Conneciton
        # MAC find WiFi IP - ipconfig getifaddr en0
        HOST = '192.168.1.29'
        # Port to listen on (non-privileged ports are > 1023)
        PORT = 65432

        print('Connected')

        # Set up Socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((HOST, PORT))

        print('Waiting for connection[s]...')
        
        # Wait for client to join socket
        self.s.listen()
        self.conn, addr = self.s.accept()
        print('Connected by: ', addr)        

        # Robot State values that will be bounced with client
        self.robot_state = None
        # Servo positions that will be added to robot_state when sent to client
        self.servo_pos = np.zeros(12, dtype=np.float32)

        # Start counter for waling robot
        self.i = 0

        # Read chosen V values from simulation
        version= "0.2.1"
        df = pd.read_csv('V/Hardcoded_{}.csv'.format(version))
        self.v = np.array(df['Best Values'], dtype=np.float32)

    def reset(self):
        # Make robot stand up
        input('Press enter to begin episode: ')
        self.i = 0

        self.robot_state = None

        return self.robot_state


    def step(self):

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

        # Receive Robot State from client
        self.robot_state = np.frombuffer(self.conn.recv(1024), dtype=np.float32)

        # Calculate servo positions to send
        #self.servo_pos[0] = 0
        self.servo_pos[1] = servo12(self.v[3] + self.v[4]*m.sin(self.i*self.v[36] + self.v[5]))
        self.servo_pos[2] = servo11(self.v[6] + self.v[7]*m.sin(self.i*self.v[36] + self.v[8]))
        #self.servo_pos[3] = 0
        self.servo_pos[4] = servo22(self.v[12] + self.v[13]*m.sin(self.i*self.v[36] + self.v[14]))
        self.servo_pos[5] = servo21(self.v[15] + self.v[16]*m.sin(self.i*self.v[36] + self.v[17]))
        #self.servo_pos[6] = 0
        self.servo_pos[7] = servo32(self.v[21] + self.v[22]*m.sin(self.i*self.v[36] + self.v[23]))
        self.servo_pos[8] = servo31(self.v[24] + self.v[25]*m.sin(self.i*self.v[36] + self.v[26]))
        #self.servo_pos[9] = 0
        self.servo_pos[10] = servo42(self.v[30] + self.v[31]*m.sin(self.i*self.v[36] + self.v[32]))
        self.servo_pos[11] = servo41(self.v[33] + self.v[34]*m.sin(self.i*self.v[36] + self.v[35]))

        # Prepare and send position data to clients
        self.conn.sendall(self.servo_pos.tobytes())

        # Update counter
        self.i += 1

        return self.robot_state


if __name__ == '__main__':
    # Construct MAIN SERVER object
    env = NetEnv()

    # Reste environment
    r_state = env.reset()

    # Keep track of time for average actions/second calculation
    start = time.time()
    
    # Walk the robot
    for i in range(400):
        # Return current robot state on every loop
        r_state = env.step()
        # Print only every 10 loops
        if i%10 == 0:
            print(r_state)
        # Keep track of number of actions/second
        sys.stdout.write(str(i)+' in: '+str(round(time.time()-start,3))+' Averaging: '+str(round(i/(time.time()-start),2))+' actions/s\r')
    
    print('Done')

