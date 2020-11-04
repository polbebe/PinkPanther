from imu_client import *
from servo_client import *

import time
import numpy as np
import math
import pickle
from threading import Thread

class Listener:
    def __init__(self, host):

        HOST = '192.168.1.29'   # Standard loopback interface address (localhost)
                                # Mac - 192.168.1.29
        PORT = port             # Port to listen on (non-privileged ports are > 1023)


        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((HOST, PORT))


        self.robot_inputs = np.zeros(12, dtype=np.float32)

        self.imu = ImuData(host)
        self.servo = ServoData(host)
        # pos = PositionData()

        self.last_v = np.zeros(3)
        self.last_pos = np.zeros(3)
        self.last_time = time.time()


        self.imu.start()
        self.servo.start()

        self.last_state = None
        self.last_act = None
        self.last_img = None
        self.data = []
    
    def listen(self, path='/data/robot_self_image', fps=100):
        start = time.time()
        last = time.time()
        i = 0
        while True:
            # while time.time()-last < 1/float(fps): pass
            act, state, img = self.get_state(path)
            #if act is not None and state is not None and img is not None:
            #    self.save_data(act, state, img)

    def get_state(self, path=None):
        action = self.act.read()
        image = self.img.read()
        imu_raw = self.imu.read()
        speeds, positions = self.servo.read()
        if action is None or \
            image is None or \
            imu_raw is None or \
            speeds is None or \
            positions is None:
                print('Act: '+str(action is None))
                print('Img: '+str(image is None))
                print('IMU: '+str(imu_raw is None))
                print('Spd: '+str(speeds is None))
                print('Pos: '+str(positions is None))
                print('')
                self.last_img = None
                self.last_state = None
                self.last_act = None
        else:
            rpy = self.quat_to_rpy(imu_raw[-4:])
            # lock here
            self.last_img = image
            self.last_state = np.concatenate([self.last_v, rpy, positions, speeds])
            self.last_act = action
            if path is not None:
                # untested, not sure if passing args like this is threadsafe
                # if not can have a mutex lock above and an unlock in save_data
                print('Forking')
                t = Thread(target=self.update, args=(path, self.last_act, self.last_state, self.last_img))
                t.daemon = True
                t.start()
                #self.save_data(self.last_act, self.last_state, self.last_img)

        #print(self.last_act)
        #print(self.last_state)
        #print('---------------------------------------')

        return self.last_act, self.last_state, self.last_img

            #data_point = [self.last_state, self.last_act]

if __name__ == '__main__':
    l = Listener('192.168.0.125')
    print('Listening...')
    l.listen('/data/tmp')
