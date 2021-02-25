import time

from threading import Thread
import socket

import numpy as np

class Listener:
	def __init__(self):
		
		HOST = '192.168.1.29'
		PORT = 65432

		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.s.connect((HOST, PORT))
		except socket.error as e:
			print(str(e))

	def read(self):
		a = input('Say smth main bich:')
		return a


	def step(self):
		# Send current state of robot
		self.s.sendall(str.encode(self.read()))
		# Receive new servo positions to be taken
		p = self.s.recv(1024)
		p.decode('utf-8')
		# If there's no more data being received, break the loop
		if not p:
			print('CONNECTION BROKEN')

		return p
		

if __name__ == '__main__':
	i = Listener()
	while True:
		print(i.step())
