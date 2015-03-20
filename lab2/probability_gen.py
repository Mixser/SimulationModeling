from abc import ABCMeta, abstractmethod
from congruential_generators import LinearCongruentialGenerator


from tests import PirsonTest


from math import factorial, ceil, exp


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
        k = ceil(x)
        m = len(self.generators)
        m_k = float(factorial(m)) / (factorial(m - k) * factorial(k))

        return m_k * self.p ** k * (1-self.p)**(m-k)


class GeometryGenerator(ProbabilityGenerator):
    NEED_PARAMS = ['gen', 'p']

    def __init__(self, *args, **kwargs):
        super(GeometryGenerator, self).__init__(*args, **kwargs)
        self.q = 1 - self.p

    def probability_func(self, x):
        x = ceil(x)
        return self.p*(1-self.p)**(x-1)

    def _generate_next(self):
        from math import log, ceil
        return ceil(log(self.gen.nextDouble) / log(self.q))


class PoissonGenerator(ProbabilityGenerator):
    NEED_PARAMS = ['p', 'generator']

    def __init__(self, *args, **kwargs):
        super(PoissonGenerator, self).__init__(*args, **kwargs)

    def probability_func(self, x):
        x = ceil(x)
        first = float(self.p ** x)/factorial(x)
        second = exp(-self.p)
        return first * second

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

