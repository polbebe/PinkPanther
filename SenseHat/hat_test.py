from sense_hat import SenseHat

sense = SenseHat()

# PRINT THINGS ON THE LED PANEL
#for i in range(3):
#    sense.show_message("Pink Panther", text_colour = (255,50,50), scroll_speed = 0.08)
#sense.show_letter("X",(255,255,0))
sense.clear()

# GET PRESSURE
pressure = sense.get_pressure()
print(pressure)

# GET TEMPERATURE (CAN GET IT FROM PRESSURE SENSOR (get_temperature_from_pressure) &
# HUMIDITY SENSOR (get_temperature_from_humidity) - default is humidity)
temperature = sense.get_temperature()
print(temperature)
