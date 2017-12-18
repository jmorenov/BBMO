import BBOMO
import ZT1 as test
import matplotlib.pyplot as plt

F1 = getattr(test, "F1")
F2 = getattr(test, "F2")
numberOfIsland = 30
numberOfGenerations = 250
dimension = 30
lb = 0
ub = 1
pmutate = 0.001
keep = 2

population, solutions = BBOMO.bbomo([F1, F2], numberOfIsland, numberOfGenerations, dimension, lb, ub, pmutate, keep)

x = []
y = []

for i in range(len(solutions)):
    x.append(solutions[i][2])
    y.append(solutions[i][3])

print x
print y

plt.plot(x, y, linewidth=2.0)
plt.show()