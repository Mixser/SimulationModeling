from abc import ABCMeta, abstractmethod


class CongruentialGenerator(object):
    NEEDED_PARAMS = dict()

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        for attr in self.NEEDED_PARAMS:
            if not attr in kwargs.keys():
                raise ValueError('Error: %s' % repr(self.NEEDED_PARAMS))

        for k, v in kwargs.items():
            setattr(self, k, v)

        self._x = None

    @abstractmethod
    def _generate_next(self):
        pass

    def get_list(self, length):
        l = [self.next for i in xrange(0, length)]
        return l

    @property
    def next(self):
        return self._generate_next()

    @property
    def x(self):
        if not self._x:
            self._x = self._generate_next()
        return self._x


class LinearCongruentialGenerator(CongruentialGenerator):
    NEEDED_PARAMS = ('a', 'c', 'm', 'x0')

    def __init__(self, **kwargs):
        super(LinearCongruentialGenerator, self).__init__(**kwargs)

    def _generate_next(self):
        self._x = self.x0 if not self._x else \
            (self.a * self._x + self.c) % self.m
        return self._x


class SquareCongruentialGenerator(CongruentialGenerator):
    NEEDED_PARAMS = ('a', 'b', 'c', 'm', 'x0')

    def __init__(self, **kwargs):
        super(SquareCongruentialGenerator, self).__init__(**kwargs)

    def _generate_next(self):
        self._x = self.x0 if not self._x else \
            (self.a * self._x ** 2 + self.b * self._x + self.c) % self.m
        return float(self._x) / self.m


class MacLarenMarsaglia(CongruentialGenerator):
    NEEDED_PARAMS = ('k', 'X', 'Y')

    def __init__(self, **kwargs):
        super(MacLarenMarsaglia, self).__init__(**kwargs)

        if not isinstance(self.X, CongruentialGenerator):
            raise ValueError('X must be a CongruentialGenerator type')

        if not isinstance(self.Y, CongruentialGenerator):
            raise ValueError('Y must be a CongruentialGenerator type')

        self.V = self.X.get_list(self.k)

    def _generate_next(self):
        j = int((self.k * self.Y.next) * 1.0 / self.Y.m)
        result = self.V[j]
        self.V[j] = self.X.next
        return result
