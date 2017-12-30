import numpy
import array
import random
from deap import tools
from deap import base
from deap import creator

def bbmo(functions, numberOfIslands, numberOfGenerations, dimension, lb, ub, pmutate, keep):
    def uniform(low, up, size=None):
        try:
            return [random.uniform(a, b) for a, b in zip(low, up)]
        except TypeError:
            return [random.uniform(a, b) for a, b in zip([low] * size, [up] * size)]

    toolbox = base.Toolbox()
    creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0))
    creator.create("Individual", array.array, typecode='d', fitness=creator.FitnessMulti)
    toolbox.register("attr_float", uniform, lb, ub, dimension)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr_float)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def initializePopulation():
        population = []

        for i in range(len(functions)):
            population.append(numpy.random.uniform(0, 1, (numberOfIslands, dimension)) * (ub - lb) + lb)

        return population

    def orderAllPopulation(population):
        def getKey(item):
            #return fitnessValuesOrdered.index([item[2], item[3]])
            for i in range(len(fitnessValuesOrdered)):
                if item[2] == fitnessValuesOrdered[i].fitness.values[0] and item[3] == fitnessValuesOrdered[i].fitness.values[1]:
                    return i

        fitness = []
        fitnessValues = []

        for i in range(len(population)):
            for j in range(len(population[i])):
                fitnessCalc0 = functions[0](population[i][j])
                fitnessCalc1 = functions[1](population[i][j])
                fitness.append([i, j, fitnessCalc0, fitnessCalc1])
                fitnessValues.append([fitnessCalc0, fitnessCalc1])

        pop = toolbox.population(n=len(functions) * numberOfIslands)

        i = 0
        for ind in pop:
            ind.fitness.values = fitnessValues[i]
            i = i + 1

        fitnessValuesOrdered = tools.selNSGA2(pop, len(functions) * numberOfIslands)
        fitnessOrdered = sorted(fitness, key=getKey)

        return fitnessOrdered

    def orderAllArchPopulation(allPopulation):
        for i in range(len(functions)):
            allPopulation[i] = orderArchPopulation(i, allPopulation[i])

        return allPopulation

    def orderArchPopulation(indexArch, archPopulation):
        def getKey(item):
            return functions[indexArch](item)

        return sorted(archPopulation, key=getKey)

    mu = numpy.zeros(numberOfIslands)
    lambda1 = numpy.zeros(numberOfIslands)

    # Calculating the mu and lambda
    for i in range(numberOfIslands):
        mu[i] = (numberOfIslands + 1 - (i)) / (numberOfIslands + 1)
        lambda1[i] = 1 - mu[i]

    population = initializePopulation()
    population = orderAllArchPopulation(population)
    populationOrdered = orderAllPopulation(population)
    solutions = []

    for g in range(numberOfGenerations):
        newPopulation = population

        for arch in range(len(functions)):
            for island in range(numberOfIslands):
                # Performing Migration operator
                if random.random() < lambda1[island]:
                    # Performing Roulette Wheel
                    RandomNum = random.random() * sum(mu)
                    Select = mu[1]
                    SelectIndex = 0
                    while (RandomNum > Select) and (SelectIndex < (numberOfIslands - 1)):
                        SelectIndex = SelectIndex + 1
                        Select = Select + mu[SelectIndex]

                    randarch = random.randint(0, len(functions) - 1)
                    j = random.randint(0, dimension - 1)
                    newPopulation[arch][island][j] = population[randarch][SelectIndex][j]

                # Performing Mutation
                for parnum in range(dimension):
                    if pmutate > random.random():
                        newPopulation[arch][island][parnum] = lb + (ub - lb) * random.random()

        newPopulationOrdered = orderAllPopulation(newPopulation)

        k = 0
        for i in range(len(newPopulationOrdered)):
            if k >= keep:
                break

            newElementSelected = newPopulationOrdered[len(newPopulationOrdered) - 1 - i]
            newArch = newElementSelected[0]
            newIsland = newElementSelected[1]

            oldElementSelected = populationOrdered[i]
            oldArch = oldElementSelected[0]
            oldIsland = oldElementSelected[1]

            newPopulation[newArch][newIsland] = population[oldArch][oldIsland]

            k = k + 1

        population = newPopulation
        population = orderAllArchPopulation(population)
        populationOrdered = orderAllPopulation(population)
        solutions.append(populationOrdered[0])

        print "Generation: " + str(g) + " | Best solution F1: " + str(solutions[g][2]) + " | F2: " +  str(solutions[g][3])

    return populationOrdered, solutions