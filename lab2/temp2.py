
import math
from math import factorial as fac
import numpy as np
import matplotlib.pyplot as plt


def binom(x, y):
    try:
        binom = fac(x) // fac(y) // fac(x - y)
    except ValueError:
        binom = 0
    return binom

class ChiSquare(object):
    @staticmethod
    def test(sequence, probability, k):
        n = len(sequence)
        minimum = min(sequence)
        maximum = max(sequence)
        h = float(maximum - minimum) / k
        segments = [round(h + minimum)]
        frequency = [0] * k
        for index in xrange(0, k):
            segments.append(round(segments[index] + h))

        for i in xrange(0, n):
            j = 0
            while sequence[i] >= segments[j]:
                j += 1
                if j == k:
                    j -= 1
                    break
            frequency[j] += 1
        hi = 0
        for i in xrange(0, k):
            hi += ((frequency[i] - n * probability(i)) ** 2) / float(n * probability(i))
        return hi

class Statistic(object):
    @staticmethod
    def initial_moment(list, s):
        sum = 0
        for item in list:
            sum += item ** s
        return float(sum) / len(list)

    @staticmethod
    def central_moment(list, s):
        sum = 0
        initial = Statistic.initial_moment(list, 1)
        for item in list:
            sum += (item - initial) ** s
        return float(sum) / len(list) - 1


class DistributionMixin(object):
    @staticmethod
    def sample_moments(sequence):
        return Statistic.initial_moment(sequence, 1), Statistic.central_moment(sequence, 2)


class LinearCongruentialGenerator(object):
    def __init__(self, **kwargs):
        self.m = kwargs.pop('m')
        self.a = kwargs.pop('a')
        self.c = kwargs.pop('c')
        self.x_n = kwargs.pop('x_0')

    @property
    def next(self):
        tmp = (self.a * self.x_n + self.c) % self.m
        self.x_n = tmp
        return float(tmp)/self.m

class UniformDistribution(DistributionMixin):
    def __init__(self, **kwargs):
        self.a = kwargs.get('a')
        self.b = kwargs.get('b')
        self.n = self.b - self.a + 1.0
        self.p = self.n ** -1
        self.generator = kwargs.get('generator', LinearCongruentialGenerator(m=2**31 - 1, a=48271, c=0, x_0=40))

    @property
    def next(self):
        element = self.generator.next
        for index, step in enumerate(np.arange(self.p, 1 + self.p, self.p)):
            if element <= step:
                return index + self.a

    def probability(self, i):
        return self.p


class NegativeDistribution(DistributionMixin):
    def __init__(self, **kwargs):
        self.r = kwargs.get('r')
        self.p = kwargs.get('p')
        self.generator = kwargs.get('generator', LinearCongruentialGenerator(m=2**31 - 1, a=48271, c=0, x_0=40))

    @property
    def next(self):
        k = 0
        e = 0
        while k < self.r:
            tmp = 1 if self.generator.next <= self.p else 0
            if tmp:
                k += 1
            else:
                e += 1
        return e


    def probability(self, i):
        return binom(i + self.r - 1, i) * (self.p ** self.r) * (1 - self.p) ** i


class PuassonDistribution(DistributionMixin):
    def __init__(self, **kwargs):
        self.l = kwargs.get('l')
        self.generator = kwargs.get('generator', LinearCongruentialGenerator(m=2**31 - 1, a=48271, c=0, x_0=40))

    @property
    def next(self):
        n = 0
        alpha = self.generator.next
        while alpha >= math.e ** (-self.l):
            n += 1
            alpha *= self.generator.next
        return n

    def probability(self, i):
        return ((math.e ** (-self.l)) * (self.l ** i)) / fac(i)

# if __name__ == '__main__':
    # uniform = UniformDistribution(a=5, b=20)
    # arr = [uniform.next for i in range(0, 10000)]
    # print arr
    # print DistributionMixin.sample_moments(arr)
    # print ChiSquare.test(arr, uniform.probability, 16) 
    # plt.hist(arr, 16)
    # plt.show()


    # negative = NegativeDistribution(r=17, p=0.6)
    # arr = [negative.next for i in range(0, 10000)]
    # print arr
    # print ChiSquare.test(arr, negative.probability, 35)
    # plt.hist(arr, 35)
    # plt.show()

puasson = PuassonDistribution(l=10)
arr = [puasson.next for i in range(0, 10000)]
# print arr
for i in xrange(1, 50):
    print ChiSquare.test(arr, puasson.probability, i)
# plt.hist(arr, 14)
plt.show()