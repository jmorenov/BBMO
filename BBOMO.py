import numpy
import random

def bbomo(functions, numberOfIslands, numberOfGenerations, dimension, lb, ub, pmutate, keep):
    def initializePopulation():
        population = []

        for i in range(len(functions)):
            population.append(numpy.random.uniform(0, 1, (numberOfIslands, dimension)) * (ub - lb) + lb)

        return population

    def orderAllPopulation(population):
        def getKey(item):
            return item[2] + item[3]

        fitness = []

        for i in range(len(functions)):
            for j in range(len(population[i])):
                fitnessCalc0 = functions[0](population[i][j])
                fitnessCalc1 = functions[1](population[i][j])
                fitness.append([i, j, fitnessCalc0, fitnessCalc1])

        fitnessOrdered = sorted(fitness, key=getKey)

        return fitnessOrdered

    def orderArchPopulation(indexArch, archPopulation):
        def getKey(item):
            return functions[0](item) + functions[1](item)

        return sorted(archPopulation, key=getKey)

    mu = numpy.zeros(numberOfIslands)
    lambda1 = numpy.zeros(numberOfIslands)

    # Calculating the mu and lambda
    for i in range(numberOfIslands):
        mu[i] = (numberOfIslands + 1 - (i)) / (numberOfIslands + 1)
        lambda1[i] = 1 - mu[i]

    population = initializePopulation()
    populationOrdered = orderAllPopulation(population)
    newPopulation = population
    solutions = []

    for g in range(numberOfGenerations):
        for arch in range(len(functions)):
            newPopulation[arch] = orderArchPopulation(arch, newPopulation[arch])

            for island in range(numberOfIslands):
                # Performing Migration operator
                for j in range(dimension):
                    if random.random() < lambda1[island]:
                        # Performing Roulette Wheel
                        RandomNum = random.random() * sum(mu)
                        Select = mu[1]
                        SelectIndex = 0
                        while (RandomNum > Select) and (SelectIndex < (numberOfIslands - 1)):
                            SelectIndex = SelectIndex + 1
                            Select = Select + mu[SelectIndex]

                        newPopulation[arch][island][j] = population[arch][SelectIndex][j]

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

        populationOrdered = orderAllPopulation(population)
        newPopulation = population

        solutions.append(populationOrdered[0])

        print "Generation: " + str(g) + " | Best solution F1: " + str(solutions[g][2]) + " | F2: " +  str(solutions[g][3])

    return populationOrdered, solutions