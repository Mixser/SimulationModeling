from abc import ABCMeta, abstractmethod
from congruential_generators import LinearCongruentialGenerator


from tests import PirsonTest


from math import factorial, ceil, exp, floor


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
    def probability_func(self, x):
        pass


    @abstractmethod
    def distribution_func(self, x):
        pass


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


    def probability_func(self, x):
        x = ceil(x)
        m = len(self.generators)
        m_k = float(factorial(m)) / (factorial(max(0, m - x)) * factorial(x))

        return m_k * self.p ** x * (1-self.p)**(m-x)


    def distribution_func(self, x):
        from scipy.stats import binom
        n = len(self.generators)
        return binom.cdf(x, n=n, p=self.p)



class GeometryGenerator(ProbabilityGenerator):
    NEED_PARAMS = ['gen', 'p']

    def __init__(self, *args, **kwargs):
        super(GeometryGenerator, self).__init__(*args, **kwargs)
        self.q = 1 - self.p

    def probability_func(self, x):

        from scipy.stats import geom

        return geom.ppf(x, self.p)


    def distribution_func(self, x):
        from scipy.stats import geom
        return geom.cdf(x, self.p)

    def _generate_next(self):
        from math import log, ceil
        from scipy.stats import geom
        return geom.rvs(self.p)

        # return floor(log(1 - self.gen.nextDouble) / log(self.q))


class PoissonGenerator(ProbabilityGenerator):
    NEED_PARAMS = ['p', 'generator']

    def __init__(self, *args, **kwargs):
        super(PoissonGenerator, self).__init__(*args, **kwargs)

    def probability_func(self, x):
        x = ceil(x)
        first = float(self.p ** x) / factorial(x)
        second = exp(-self.p)
        return first * second

    def distribution_func(self, x):
        from scipy.stats import poisson
        return poisson.cdf(x, self.p)



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

