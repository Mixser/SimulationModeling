from congruential_generators import LinearCongruentialGenerator

A = 1666
C = 12
M = 6075

g1 = LinearCongruentialGenerator(a=A, c=C, x0=1, m=M)

m = M


def euclid(a, b):
    if b == 0:
        return (a, 1, 0)
    _d, _x, _y = euclid(b, a % b)
    return (_d, _y, _x - (a/b)*_y)


def solver(a, b, m):
    d, _x, _y = euclid(a, m)
    if b % d == 0:
        x0 = _x * (b / d) % m
        answer = set()
        for i in xrange(0, d):
            answer.add((x0 + i * (m/d)) % m)
        return answer
    else:
        return set()


def solve_first_system(x0, x1, x2):
    a = x1 - x0
    b = x2 - x1

    return solver(a, b, m)


def solve_second_system(a, x0, x1):
    _a = 1
    _b = x1 - a * x0
    return solver(_a, _b, m)


def test(*args):
    g1 = LinearCongruentialGenerator(a=A, c=C, x0=1, m=6075)
    g2 = LinearCongruentialGenerator(a=args[0], c=args[1], x0=1, m=6075)
    return g1.get_list(100) == g2.get_list(100)


x0, x1, x2 = g1.next, g1.next, g1.next
answers = solve_first_system(x0, x1, x2)

result = []

for a in answers:

    x0, x1 = g1.next, g1.next
    new_c = solve_second_system(a, x0, x1)

    temp = [a, ] + list(new_c)
    result.append(temp)


for t in result:
    print t, test(*t)
