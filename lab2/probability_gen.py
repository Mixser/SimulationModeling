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
    draw_hist(gen, n=10000, k=2, h=1)


def poisson_generator():
    m = 2**32 - 1
    l = LinearCongruentialGenerator(a=48271, m=m, c=0, x0=4)

    gen = PoissonGenerator(p=10, generator=l)

    draw_hist(gen, n=10000, k=2, h=0.5)


def geometry_generator():
    m = 2**32 - 1
    l = LinearCongruentialGenerator(a=48271, m=m, c=0, x0=4)

    gen = GeometryGenerator(p=0.2, gen=l)

    draw_hist(gen, n=10000, k=2, h=2)


if __name__ == "__main__":
    
    benominal_generator()
    poisson_generator()
    geometry_generator()
    

    
