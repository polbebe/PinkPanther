import numpy as np
import matplotlib.pyplot as plt


data = np.genfromtxt("commanded_pos.csv", delimiter=",", names=["10", "11", "12", "20", "21", "22", "30", "31", "32", "40", "41", "42"])

x = np.linspace(0,200,200)
upper_lim = 700
upper_lims = np.zeros(len(x))
for i in range(len(upper_lims)):
	upper_lims[i] = upper_lim

lower_lim = 313
lower_lims = np.zeros(len(x))
for i in range(len(lower_lims)):
	lower_lims[i] = lower_lim

i = 42

plt.plot(x, upper_lims)
plt.plot(x, data['{}'.format(i)])
plt.plot(x, lower_lims)
plt.title('Servo {}'.format(i))
plt.savefig('movement_servo{}.png'.format(i))
plt.show()