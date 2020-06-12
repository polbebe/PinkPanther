import math as m
import random as r
import numpy as np
import matplotlib.pyplot as plt

i = 0

v = [0.09366486193742063, -0.3910298281777823, -0.38048775348185426,
	 0.3533151448874734, 0.40102390766150287, -0.48292162810047734,
	 -0.48226864217303356, 0.12424497460368811, -0.2594928275420473,
	 -0.4998096572544207, -0.3108416532536089, -0.4172196785824154]

elbow_pos = []
knee_pos = []
i_s = []

while i<1000:

	i_s.append(i)
	elbow_pos.append(v[0] + v[1]*m.sin(i*0.1 + v[2]))
	knee_pos.append(v[6] + v[7]*m.sin(i*0.1 + v[8]))

	i += 1

# Plot elbow position
print("Max elbow pos:",np.max(elbow_pos),"Min elbow pos:",np.min(elbow_pos))
plt.plot(i_s, elbow_pos)
plt.title("elbow position over Time")
plt.ylabel("Position [rad]")
plt.xlabel("Time [s]")
plt.savefig("elbow.png")
plt.clf()

# Plot knee position
print("Max knee pos:",np.max(knee_pos),"Min knee pos:",np.min(knee_pos))
plt.plot(i_s, knee_pos)
plt.title("Knee position over Time")
plt.ylabel("Position [rad]")
plt.xlabel("Time [s]")
plt.savefig("knee.png")
plt.clf()

