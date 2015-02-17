from congruential_generators import LinearCongruentialGenerator

A = 1666
C = 12
M = 6075

g1 = LinearCongruentialGenerator(a=A, c=C, x0=1, m=M)

x0, x1, x2, x3, x4 = g1.get_list(5)

def euclid(a, b):
    if b == 0:
        return (a, 1, 0)
    _d, _x, _y = euclid(b, a % b)
    return (_d, _y, _x - (a/b)*_y)


def solution(a, b, c):
    print a, b, c
    d, x0, y0 = euclid(abs(a), abs(b))
    if c % d != 0:
        return list()

    x0 *= c / d;
    y0 *= c / d;

    x0 = x0 if a > 0 else -x0
    y0 = y0 if b > 0 else -y0

    return (x0, y0)

print solution(x3-x2, 1, x4 - x3)
