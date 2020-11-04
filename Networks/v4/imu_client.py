import socket
import numpy as np
from sense_hat import SenseHat
from threading import Thread


class ImuData:
	# Constructor method
	def __init__(self, host):
		# The server's hostname or IP address
		HOST = '192.168.1.29'
		# The port used by the server
		PORT = 65431

		# Set up socket
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))

		# Imu values that will be updated
		self.imu_values = None
		# Keep track whether stopped or not
		self.stopped = False

		# Set up sense hat
		self.sense = SenseHat()
		self.sense.clear()

	# Start thread
	def start(self):
		# Thread which updates its rpy values
		t = Thread(target=self.update, args=())
		# Make it run in background
		t.daemon=True
		# Start the updating
		t.start()
		return self

	# Update imu values
	def update(self):
		while True:
			if self.stopped:
				break
			# Get the roll-pitch-yaw values from sense hat
			o = self.sense.get_orientation()
			roll = o["roll"]
			pitch = o["pitch"]
			yaw = o["yaw"]
			# Update imu values
			self.imu_values = [roll, pitch, yaw]

    def read(self):
    	return self.imu_values


    def stop(self):
    	self.stopped = True



if __name__ == '__main__':
	# Construct object and start
	i = ImuData()
	i.start()
