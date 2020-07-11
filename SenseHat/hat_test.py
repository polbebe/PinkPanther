from sense_hat import SenseHat

sense = SenseHat()


for i in range(3):
    sense.show_message("Pink Panther", text_colour = (255,50,50), scroll_speed = 0.08)
    
sense.clear()
#sense.show_letter("X",(255,255,0))