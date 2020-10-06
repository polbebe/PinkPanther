#!/usr/bin/env python3

import socket
import numpy as np
HOST = '192.168.1.29'	# The server's hostname or IP address
PORT = 65432        	# The port used by the server
a = np.arange(5, dtype=np.float32)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    a_data = a.tobytes()
    s.sendall(a_data)
    
    data = s.recv(1024)
    a = np.frombuffer(data, dtype=np.float32)
    print(a)

