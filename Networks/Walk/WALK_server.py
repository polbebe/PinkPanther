#!/usr/bin/env python3

import socket
import numpy as np

HOST = '192.168.1.29'   # Standard loopback interface address (localhost)
                        # Mac - 192.168.1.29
PORT = 65432            # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            a = np.frombuffer(data, dtype=np.float32)
            print(a)
            if not data:
                break
            conn.sendall(data)

