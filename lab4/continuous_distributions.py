from __future__ import division

from abc import ABCMeta, abstractmethod

from math import log

from congruential_generators import LinearCongruentialGenerator




class ContinuosDistribution(object):
    __metaclass__ = ABCMeta
    NEEDED_PARAMS = list()


    generator = LinearCongruentialGenerator(a=48271, m=2**32-1, c=0, x0=1)

    def __init__(self, *args, **kwargs):
        for attr in self.NEEDED_PARAMS:
            if not attr in kwargs.keys():
                raise AttributeError('Needed params %s' % ', '.join(self.NEEDED_PARAMS))

        for k, v in kwargs.items():
            setattr(self, k, v)



    @abstractmethod
    def _generate_next(self):
        raise NotImplementedError()

    @property
    def next(self):
        return self._generate_next()


class UniformDistribution(ContinuosDistribution):
    NEEDED_PARAMS = ('a', 'b')

    def _generate_next(self):
        eta = self.generator.nextDouble
        return (self.b - self.a) * eta + self.a


class ExponentialDistribution(ContinuosDistribution):
    NEEDED_PARAMS = ('lam', )

    def _generate_next(self):
        l = - (1.0 / self.lam)
        a = self.generator.nextDouble
        return l * log(a)


class LaplaceDistribution(ContinuosDistribution):
    NEEDED_PARAMS = ('lam', ) 

    def _generate_next(self):
        l = 1.0/self.lam
        a = self.generator.nextDouble
        result = l * log(2 * a) if a < 0.5 else -l * log(2 * (1 - a))

        return result


if __name__ == '__main__':
    a = LaplaceDistribution(lam=0.02)

    for i in xrange(100):
        print a.next



