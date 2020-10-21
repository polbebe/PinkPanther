from sense_hat import SenseHat
from time import sleep

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
    elif 360 > pitch > 181 and x != 7:
        new_x += 1
    if 1 < roll < 179 and y != 7:
        new_y += 1
    elif 360 > roll > 181 and y != 0:
        new_y -= 1
    return new_x, new_y

# Set initial position of Dot
x = 3
y = 3

while True:
    # Get Roll & Pitch from sense hat
    o = sense.get_orientation()
    pitch = o["pitch"]
    roll = o["roll"]
    x,y = move_marble(pitch,roll,x,y)
    # Add dot to screen
    screen[y][x] = w
    # Display screen
    sense.set_pixels(sum(screen,[]))
    sleep(0.05)
    screen[y][x] = b
    # Print values in shell
    print('pitch: {}, roll: {}'.format(pitch, roll))
    


