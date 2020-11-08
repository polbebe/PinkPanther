from test_client import *
import numpy as np

test = ImuData()

robot_state = np.zeros(15, dtype=np.float32)

robot_state[:12] = test.read()


print(robot_state)