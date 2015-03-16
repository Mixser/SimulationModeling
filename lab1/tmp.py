from congruential_generators import LinearCongruentialGenerator


import matplotlib.pyplot as plt



M = 2 ** 4 * 3 * 5 * 7 * 11 * 13

N = M * 2


A = 2 * 2 * 3 * 5 * 7 * 11 * 13 + 1

def length(l):
    item = l[-1]
    length = 0
    for i in xrange(len(l) -2 , 0, -1):
        if l[i] == item:
            break
        length += 1
    if length:
        length += 1
    return length




g1 = LinearCongruentialGenerator(a=4, c=0, x0=1, m=13)


def pr(m):
    print 'M: %s' % m
    for a in xrange(0, m):
        for x0 in xrange(0, m):
            g = LinearCongruentialGenerator(a=a, x0=x0, c=0, m=m)
            ll = g.get_list(2 * m)
            s = ', '.join([str(j) for j in ll])
            print "  a: %s, x0: %s, l: %s; %s" % (a, x0, length(ll), s)


pr(13)