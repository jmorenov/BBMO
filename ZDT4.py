import math

def F1(x):
    return x[0]

def F2(x):
    def g(x2m):
        sum = 0

        for i in x2m:
            sum = sum + (i * i  - 10 * math.cos(4 * math.pi * i))

        return 1 + 10 * (len(x) - 1) + sum

    def h(f1, g):
        return 1 - math.sqrt(f1 / g)

    x2m = x[1:len(x)]

    return g(x2m) * h(F1(x), g(x2m))