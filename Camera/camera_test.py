# Never save a file as picamera.py

from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.rotation = 180

camera.start_preview(alpha=230)

#for i in range(3):
#    sleep(5)
#    camera.capture('/home/pi/Desktop/image{}.jpg'.format(i))
sleep(5)
camera.capture('/home/pi/Desktop/angle_18.jpg')
sleep(5)
camera.stop_preview()
