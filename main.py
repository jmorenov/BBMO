import BBMO
import matplotlib.pyplot as plt
import ZDT6 as test
import numpy
import json

F1 = getattr(test, "F1")
F2 = getattr(test, "F2")
numberOfIsland = 200
numberOfGenerations = 250
dimension = 30
lb = 0
ub = 1
pmutate = 0.01
keep = 2

population, solutions = BBMO.bbmo([F1, F2], numberOfIsland, numberOfGenerations, dimension, lb, ub, pmutate, keep)

pop = []
for i in range(len(population)):
    pop.append([population[i][2], population[i][3]])

pop.sort(key=lambda x: x)

optimal_front = json.load(open("zdt6.json"))
optimal_front = sorted(optimal_front[i] for i in range(0, len(optimal_front), 2))
optimal_front = numpy.array(optimal_front)
front = numpy.array([ind for ind in pop])
plt.scatter(optimal_front[:,0], optimal_front[:,1], c="r")
plt.plot(front[:,0], front[:,1], linewidth=2.0)
plt.show()