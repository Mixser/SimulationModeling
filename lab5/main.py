from __future__ import division

from numpy.random import uniform, normal

from math import log, sin, exp, pi, sqrt



def first():
    N = 10000
    low, high = 88, 99
    func1 = lambda x : log(x) * sin(x)
    p = lambda x : 1/(high - low)
    func = lambda x : func1(x) / p(x)
    a = 1 / N * reduce(lambda x, y: x + func(uniform(low=low, high=high) ) , xrange(N), 0)

    return a


def second():
    # 7.64034
    N = 10000
    p = lambda x: exp(-x**2 / 2)

    p_i = lambda x : exp(-x**2)

    p = lambda x, y: p_i(x) * p_i(y)

    ev = lambda a: sqrt(-log(a) * 2)

    func = lambda x,y: 2 * pi * sqrt(1 + sin(x + 2 * y) ** 2 )

    a = 1 / N * reduce(lambda x, y: x +  func(normal(), normal()), xrange(N), 0)

    print a

first()
# second()