import numpy as np
import matplotlib.pyplot as plt


data = np.genfromtxt("gait_v1_check_data.csv", delimiter=",", names=["10", "12", "11", "20", "22", "21", "30", "32", "31", "40", "42", "41"])

x = np.linspace(0,399,400)

plt.plot(x, data['12'])
plt.legend()
plt.show()