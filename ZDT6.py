import math

def F1(x):
    return 1 - math.exp(-4*x[0]) * math.pow(math.sin(6 * math.pi * x[0]), 6)

def F2(x):
    def g(x2m):
        sum = 0

        for i in x2m:
            sum = sum + i

        return 1 + 9 * math.pow(sum/(len(x) - 1), 0.25)

    def h(f1, g):
        return 1 - (f1 / g) * (f1 / g)

    x2m = x[1:len(x)]

    return g(x2m) * h(F1(x), g(x2m))