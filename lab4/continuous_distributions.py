from __future__ import division

from abc import ABCMeta, abstractmethod
from math import log, exp

from congruential_generators import LinearCongruentialGenerator
from tests import PirsonTest, KolmagorovTest

from collections import OrderedDict


class ContinuosDistribution(object):
    __metaclass__ = ABCMeta
    NEEDED_PARAMS = list()


    generator = LinearCongruentialGenerator(a=48271, m=2**32-1, c=0, x0=104)

    def __init__(self, *args, **kwargs):
        for attr in self.NEEDED_PARAMS:
            if not attr in kwargs.keys():
                raise AttributeError('Needed params %s' % ', '.join(self.NEEDED_PARAMS))

        for k, v in kwargs.items():
            setattr(self, k, v)


    @abstractmethod
    def probability_func(self, x):
        raise NotImplementedError()


    @abstractmethod
    def _generate_next(self):
        raise NotImplementedError()

    @property
    def next(self):
        return self._generate_next()


class UniformDistribution(ContinuosDistribution):
    NEEDED_PARAMS = ('a', 'b')


    def probability_func(self, x):
        if x < self.a:
            return 0.0
        if x >= self.b:
            return 1.0

        return (x - self.a) / (self.b - self.a)

    def _generate_next(self):
        eta = self.generator.nextDouble
        return (self.b - self.a) * eta + self.a


class ExponentialDistribution(ContinuosDistribution):
    NEEDED_PARAMS = ('lam', )

    def _generate_next(self):
        l = - (1.0 / self.lam)
        a = self.generator.nextDouble
        return l * log(a)

    def probability_func(self, x):
        return 1 - exp(-self.lam * x)



class LaplaceDistribution(ContinuosDistribution):
    NEEDED_PARAMS = ('lam', ) 

    def _generate_next(self):
        l = 1.0/self.lam
        a = self.generator.nextDouble
        result = l * log(2 * a) if a < 0.5 else -l * log(2 * (1 - a))

        return result

    def probability_func(self, x):
        if x <= 0:
            return 0.5 * exp(self.lam * x)
        else:
            return 1.0 - 0.5 * exp(-self.lam * x)


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    a = UniformDistribution(a=5, b=15)
    # a = ExponentialDistribution(lam=5)
    # a = LaplaceDistribution(lam=5.0)

    values = [a.next for i in xrange(0, 10000)]

    print sum(values) / len(values)

    with open('out.txt', 'w') as f:
        f.write(str(values))

    print PirsonTest.check(10000, 10, a)
    print KolmagorovTest.check(10000, 10, a, 0.01)

    n, bins, patches = plt.hist(values, 1000, normed=True, facecolor='green', alpha=0.75)

    plt.title("Sample moments: ")

    plt.xlabel('Smarts')
    plt.ylabel('Probability')
    plt.axis([-2.0, 15.0, 0, 0.2])
    plt.grid(True)

    plt.show()