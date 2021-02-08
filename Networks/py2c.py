pypos = []
cpos = []

for j in range(1,5):
	a = 10*j
	r = range(a, a+3)
	for i in r:
		pos = input("Enter your position for s{}:".format(i))
		pypos.append(pos)

print("pyLX16A: {}".format(pypos))

for i in pypos:
	a = int(i)
	cpos.append(round(a*(25/6))

print("cLX16A: {}".format(cpos))
