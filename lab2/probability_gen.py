#-*- coding: utf-8 -*-
# python 2


from abc import ABCMeta, abstractmethod
from congruential_generators import LinearCongruentialGenerator


class ProbabilityGenerator(object):
    NEED_PARAMS = list()

    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        for attr in self.NEED_PARAMS:
            if attr not in kwargs.keys():
                raise ValueError('Error: %s' % repr(self.NEEDED_PARAMS))

        for k,v in kwargs.items():
            setattr(self, k, v)


    @abstractmethod
    def _generate_next(self):
        pass

    @property
    def next(self):
        return self._generate_next()


class BinominalGenarator(ProbabilityGenerator):
    NEED_PARAMS = ['p', 'generators']

    def __init__(self, *args, **kwargs):
        super(BinominalGenarator, self).__init__(*args, **kwargs)

    def _generate_next(self):
        f = lambda x: 1 if x > 0 else 0
        x = reduce(lambda x, y: x + f(self.p - y.nextDouble), self.generators, 0)
        return x


class GeometryGenerator(ProbabilityGenerator):
    NEED_PARAMS = ['gen', 'p']

    def __init__(self, *args, **kwargs):
        super(GeometryGenerator, self).__init__(*args, **kwargs)
        self.q = 1 - self.p

    def _generate_next(self):
        from math import log, ceil
        return ceil(log(self.gen.nextDouble) / log(self.q))


class PoissonGenerator(ProbabilityGenerator):
    NEED_PARAMS = ['p', 'generator']

    def __init__(self, *args, **kwargs):
        super(PoissonGenerator, self).__init__(*args, **kwargs)

    def _generate_next(self):
        from math import exp
        x = 0.0
        b = exp(-self.p)
        r = self.generator.nextDouble
        tr = 1
        tr = tr * r 

        while tr - b > 0:
            x += 1.0
            r = self.generator.nextDouble
            tr = tr * r

        return x

def get_generators(count):
    from numpy import random

    result = []
    m = 2**31 - 1
    for i in xrange(0, count):
        result.append(LinearCongruentialGenerator(a=48271, m=m, c =0, x0=random.randint(1, 2000000)))

    return result

def draw_hist(gen, h):
    import numpy as np
    import matplotlib.mlab as mlab
    import matplotlib.pyplot as plt

    x = [gen.next for i in xrange(0, 10000)]

    max_x = max(x)
    min_x = min(x)

    n, bins, patches = plt.hist(x, 50, normed=True, facecolor='green', alpha=0.75)
    mu, sigma = 100, 15

    plt.xlabel('Smarts')
    plt.ylabel('Probability')
    plt.axis([min_x, max_x, 0, h])
    plt.grid(True)

    plt.show()


def benominal_generator():
    gen = BinominalGenarator(p=0.7, generators=get_generators(20))
    draw_hist(gen, 1)


def poisson_generator():
    m = 2**32 - 1
    l = LinearCongruentialGenerator(a=48271, m=m, c=0, x0=4)

    gen = PoissonGenerator(p=1, generator=l)

    draw_hist(gen, 10)


def geometry_generator():
    m = 2**32 - 1
    l = LinearCongruentialGenerator(a=48271, m=m, c=0, x0=4)

    gen = GeometryGenerator(p=0.2, gen=l)

    for x in xrange(0, 1000):
        print gen.next

    draw_hist(gen, 2)





if __name__ == "__main__":
    
    # benominal_generator()
    poisson_generator()
    # geometry_generator()
    

    
