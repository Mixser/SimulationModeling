import random
import math
import numpy as np


def monte_carlo_integral(n, function):
    uniform = UniformDistribution(n=n, a=0, b=1, function=random.random)
    list = [function(uniform.next) for i in xrange(0, n)]
    mean = sum(list)
    return mean / n


def read_file(filename):
    try:
        with open(filename) as f:
            lines = f.readlines()
            A = [map(float, line.split()) for line in lines[:-2]]
            F = map(float, lines[-1].split())
            return len(F), A, F
    except IOError:
        print 'no such file or directory'
    return 0, [], []


def monte_carlo_system(filename, N, m):
    n, A, F = read_file(filename)
    x = [0] * n
    pi = [1.0 / n] * n
    p = [pi] * n
    h = np.eye(n)
    i = [0] * (N + 1)
    Q = [0] * (N + 1)
    for item in xrange(0, n):
        ksi = [0] * m
        for j in xrange(0, m):
            alpha = random.random()
            s = 0
            for k in xrange(0, n):
                s += pi[k]
                if alpha < s:
                    i[0] = k
                    break
            for l in xrange(1, N+1):
                alpha = random.random()
                s = 0
                for k in xrange(0, n):
                    s += p[i[l - 1]][k]
                    if alpha < s:
                        i[l] = k
                        break

            Q[0] = (h[item][i[0]] / pi[i[0]]) if pi[i[0]] > 0 else 0

            for k in xrange(1, N + 1):
                Q[k] = (Q[k - 1] * A[i[k - 1]][i[k]] / p[i[k - 1]][i[k]]) if (p[i[k - 1]][i[k]]) > 0 else 0

            for k in xrange(0, N + 1):
                ksi[j] += Q[k] * F[i[k]]

        for k in xrange(0, m):
            x[item] += ksi[k]
        x[item] /= m


    matrix_a = np.array(A)
    matrix_x = np.array(x)

    matrix_f = np.array(F)

    e = np.eye(len(matrix_a))
    x_toch = np.linalg.solve(e - matrix_a, matrix_f)


    return x, x_toch


class Laws(object):
    def __init__(self, **kwargs):
        self.n = kwargs.get('n', None)
        self.function = kwargs.get('function', None)

    def next(self):
        raise NotImplementedError


class LinearCongruentMethod:
    def __init__(self, **kwargs):
        self.n = kwargs.get('n', 1)
        self.a = kwargs.get('a', None)
        self.x_0 = kwargs.get('x_0', None)
        self.M = kwargs.get('M', None)
        self.c = kwargs.get('c', None)
        self.i = 1

    def next(self):
        temp = (self.a * self.x_0 + self.c) % self.M
        self.x_0 = temp
        return temp * 1.0 / self.M

    def next_alfa(self):
        if self.i > n:
            raise IndexError
        temp = float(self.i) / (self.n + 1)
        self.i += 1
        return temp


class UniformDistribution(Laws):
    def __init__(self, **kwargs):
        self.a = kwargs.pop('a')
        self.b = kwargs.pop('b')
        super(UniformDistribution, self).__init__(**kwargs)

    @property
    def next(self):
        return (self.b - self.a) * self.function() + self.a


if __name__ == '__main__':
    # n = 10000
    # function = lambda x: math.e ** (-1.0 / (1 - x)) * (math.sin(1/(1 - x))**5) / (1 - x) ** 2
    # WOLFRAM_RESULT = 0.19177932
    # result = monte_carlo_integral(n, function)
    # print 'Monte carlo: %s' % result
    # print 'WOLFRAM: %s' % WOLFRAM_RESULT
    x, x_toch = monte_carlo_system('11.txt', 1000, 10000)


    with open('out.txt', 'w') as f:
        f.write(', '.join([str(i) for i in x]))

    print x_toch



