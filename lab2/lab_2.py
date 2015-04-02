
from congruential_generators import LinearCongruentialGenerator
from probability_gen import BinominalGenarator, GeometryGenerator, PoissonGenerator

from tests import PirsonTest

def get_generators(count):
    from numpy import random

    result = []
    m = 2**31 - 1
    for i in xrange(0, count):
        result.append(LinearCongruentialGenerator(a=48271, m=m, c =0, x0=random.randint(1, 2000000)))

    return result

def draw_hist(gen, n=10000, k=1, h=1):
    import numpy as np
    import matplotlib.mlab as mlab
    import matplotlib.pyplot as plt

    values = [gen.next for i in xrange(0, n)]

    avg = reduce(lambda x,y : x + float(y/n), values, 0)

    sample_moment = reduce(lambda x, y: x + float(y**k)/n, values, 0)
    sample_central_moment = reduce(lambda x, y: x + float((y - avg)**k)/n, values, 0)

    max_x = max(values)
    min_x = min(values)

    n, bins, patches = plt.hist(values, 50, normed=True, facecolor='green', alpha=0.75)

    plt.title("Sample moments: %s, central moment: %s" % (sample_moment, sample_central_moment))

    plt.xlabel('Smarts')
    plt.ylabel('Probability')
    plt.axis([min_x, max_x, 0, h])
    plt.grid(True)

    plt.show()


def benominal_generator():
    gen = BinominalGenarator(p=0.7, generators=get_generators(20))

    test = PirsonTest()

    print test.check(10000,gen)

    draw_hist(gen, n=10000, k=19, h=1)


def poisson_generator():
    m = 2**32 - 1
    l = LinearCongruentialGenerator(a=48271, m=m, c=0, x0=4)
    test = PirsonTest()
    gen = PoissonGenerator(p=10, generator=l)

    
    print test.check(10000, gen)

    draw_hist(gen, n=10000, k=2, h=0.5)


def geometry_generator():
    m = 2**32 - 1
    l = LinearCongruentialGenerator(a=48271, m=m, c=0, x0=4)
    gen = GeometryGenerator(p=0.2, gen=l)

    print test.check(10000, gen)

    # draw_hist(gen, n=10000, k=2, h=2)


if __name__ == "__main__":
    
    benominal_generator()
    poisson_generator()
    geometry_generator()
    

    
