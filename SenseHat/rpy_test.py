from sense_hat import SenseHat

sense = SenseHat()
sense.clear()

w = (255,255,255)
b = (0,0,0)
# Create screen
screen =[[b,b,b,b,b,b,b,b],
        [b,b,b,b,b,b,b,b],
        [b,b,b,b,b,b,b,b],
        [b,b,b,b,b,b,b,b],
        [b,b,b,b,b,b,b,b],
        [b,b,b,b,b,b,b,b],
        [b,b,b,b,b,b,b,b],
        [b,b,b,b,b,b,b,b]]

# Function that determines which way to move dot
def move_marble(pitch, roll, x, y):
	new_x = x
	new_y = y
	if 1 < pitch < 179 and x != 0:
		new_x -= 1
	elif 359 > pitch > 181 and x != 7:
		new_x += 1
	if 1 < roll < 179 and y != 7:
		new_y += 1
	elif 359 > roll > 181 and y != 0:
		new_y -= 1

while True:
	# Get Roll & Pitch from sense hat
	o = sense.get_orientation()
	pitch = o["pitch"]
	roll = o["roll"]
	x,y = move_marble(pitch,roll,x,y)
	# Add dot to screen
	screen[x][y] = w
	# Display screen
	sense.set_pixels(sum(screen,[]))


'''
while True:
	o = sense.get_orientation()
	pitch = o["pitch"]
	roll = o["roll"]
	yaw = o["yaw"]
	print("pitch {0} roll {1} yaw {2}".format(pitch, roll, yaw))
'''
