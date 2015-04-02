import random
import math

from math import factorial as fac

def binom(x, y):
    try:
        binom = fac(x) // fac(y) // fac(x - y)
    except ValueError:
        binom = 0
    return binom

class LinearCongruentMethod:
    def __init__(self, **kwargs):
        self.n = kwargs.get('n', 1)
        self.a = kwargs.get('a', None)
        self.x_0 = kwargs.get('x_0', None)
        self.M = kwargs.get('M', None)
        self.c = kwargs.get('c', None)

    def next(self):
        temp = (self.a * self.x_0 + self.c) % self.M
        self.x_0 = temp;
        return temp * 1.0 / self.M

class Laws(object):
    def __init__(self, **kwargs):
        self.probability = kwargs.get('probability', None)
        self.n = kwargs.get('n', None)
        self.m = kwargs.get('m', None)
        self.function = kwargs.get('function', None)
        # self.delta = kwargs.get('delta', None)
        # self.sequence = []

    def next(self):
        raise NotImplementedError

    def getList(self):
        return [self.next for i in xrange(0, self.n)]
    #
    # def writeInFile(self, file_name):
    #     f = open(file_name, 'w')
    #     for i in xrange(0, self.n):
    #         f.write(str(self.sequence[i]) + '\n')

    def pirson_test(self, k, p = None, list = None):
        minimum = min(list)
        maximum = max(list)
        h = float(maximum - minimum) / k
        segments = []
        frequency = []
        segments.append(round(h + minimum))
        for index in xrange(0, k):
            segments.append(round(segments[index] + h))
            frequency.append(0)

        for i in xrange(0, self.n):
            j = 0
            while list[i] >= segments[j]:
                j += 1
                if j == k:
                    j -= 1
                    break
            frequency[j] += 1

        hi = 0
        for index in xrange(0, k):
            hi += ((frequency[index] - self.n * p[index]) ** 2) / float(self.n * p[index])
        return hi

    def rq_probability(self):
        raise NotImplementedError

class BernulliDistribution(Laws):

    @property
    def next(self):
        a = self.function()
        result = 1 if a <= self.probability else 0
        return result

    def rq_probability(self):
        return [1 - self.probability, self.probability]

class BinomialDistribution(Laws):

    @property
    def next(self):
        x = 0
        for j in range(0, self.m):
            a = self.function()
            if (self.probability - a) > 0:
                x += 1
        return x

    def rq_probability(self):
        return [binom(self.m, i) * (self.probability ** i) * ((1 - self.probability) ** (self.m - i)) for i in xrange(0, self.m)]

class GeometricDistribution(Laws):

    @property
    def next(self):
        return int(math.log(self.function()) / math.log(1 - self.probability))

    def rq_probability(self, k):
        return [self.probability * ((1 - self.probability) ** i) for i in xrange(0, k)]

class NegativBinomialDistribution(Laws):

    @property
    def next(self):
        x = 0
        for j in xrange(0, self.m):
            x += int(math.log(self.function())/ math.log(1 - self.probability))
        return x

    def rq_probability(self, k):
        return [binom(i + self.m - 1, i) * (self.probability ** self.m) * (1 - self.probability) ** i for i in xrange(0, k)]

class PuassonDistribution(Laws):

    @property
    def next(self):
        k = -1
        a = 1
        while True:
            a *= self.function()
            k += 1
            if a < math.e ** (- self.m):
                break
        return k

    def rq_probability(self, k):
        return [((math.e ** (-self.m)) * (self.m ** i)) / math.factorial(i) for i in xrange(0, k)]

class UniformDiscretDistribution(Laws):
    def __init__(self, **kwargs):
        self.a = kwargs.pop('a',None)
        self.b = kwargs.pop('b', None)
        super(UniformDiscretDistribution, self).__init__(**kwargs)

    @property
    def next(self):
        s = self.generate()
        j = 0
        x = self.function()
        while x > s[j] and j < self.b - self.a + 2:
            j +=1
        return j

    def generate(self):
        s = [0]
        temp = self.b - self.a + 1
        p = 1.0 / temp
        for i in xrange(1, temp + 1):
            s.append(s[i - 1] + p)
        return s

    def rq_probability(self):
        temp = self.b - self.a + 1
        return [1.0 / temp for i in xrange(0, temp)]

class HyperGeometricDistribution(Laws):
    def __init__(self, **kwargs):
        self.N = kwargs.pop('N', None)
        self.D = kwargs.pop('D', None)
        super(HyperGeometricDistribution, self).__init__(**kwargs)

    @property
    def next(self):
        k = 0
        white = self.D
        black = self.N - self.D
        for j in xrange(0, self.m):
            p = float(white) / (white + black)
            bernulli = BernulliDistribution(probability=p, function=self.function)
            if bernulli.next == 1:
                k += 1
                white -= 1
            else:
                black -= 1
        return k

    def rq_probability(self, k):
        return [float(binom(self.D, i)) * binom(self.N - self.D, self.m - i) / binom(self.N, self.m) for i in xrange(0, k)]

if __name__ == '__main__':
    line = LinearCongruentMethod(M=2 ** 30, a=1025, c=1333333, x_0=60897271)

    # bernulli = BernulliDistribution(probability=0.7, n=10001, m=0, function=line.next)
    # list = bernulli.getList()
    # print list
    # p = bernulli.rq_probability()
    # print bernulli.pirson_test(2, p, list=list)

    binomial = BinomialDistribution(probability=0.7, n=10001, m=14, function=line.next)
    list = binomial.getList()
    print list
    p = binomial.rq_probability()
    print binomial.pirson_test(14, p, list=list)

    # geometric = GeometricDistribution(probability=0.4, n=10001, function=line.next)
    # list = geometric.getList()
    # print list
    # p = geometric.rq_probability(k=20)
    # print geometric.pirson_test(20, p, list=list)

    # negativ = NegativBinomialDistribution(probability=0.4, n=10001, m=5, function=line.next)
    # list = negativ.getList()
    # print list
    # p = negativ.rq_probability(36)
    # print negativ.pirson_test(36, p, list=list)

    # puasson = PuassonDistribution(n=10001, m=4, function=line.next)
    # list = puasson.getList()
    # print list
    # p = puasson.rq_probability(14)
    # print puasson.pirson_test(14, p, list=list)

    # uniform = UniformDiscretDistribution(n=10001, a=0, b=25, function=line.next)
    # list = uniform.getList()
    # print list
    # p = uniform.rq_probability()
    # print uniform.pirson_test(26, p, list=list)

    # hyper = HyperGeometricDistribution(n=10001, m=8, N=100, D=13, function=line.next)
    # list = hyper.getList()
    # print list
    # p = hyper.rq_probability(6)
    # print hyper.pirson_test(6, p, list=list)





