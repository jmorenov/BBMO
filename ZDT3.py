import math

def F1(x):
    return x[0]

def F2(x):
    def g(x2m):
        sum = 0

        for i in x2m:
            sum = sum + (i / (len(x2m) - 1))

        return 1 + 9 * sum

    def h(f1, g):
        return 1 - math.sqrt(f1 / g) - (f1 / g) * math.sin(10 * math.pi * f1)

    x2m = x[1:len(x)]

    return g(x2m) * h(F1(x), g(x2m))