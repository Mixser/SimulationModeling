from math import pow

from scipy import stats

class PirsonTest(object):

    @staticmethod
    def check(n, gen):
        sequence = [gen.next for i in xrange(0, n)]

        X = dict()

        for x in sequence:
            if x not in X:
                X[x] = 1
            else:
                X[x] += 1

        k = len(X)

        hi = 0
        for (x, value) in X.items():
            hi += float((value - n * gen.probability_func(x))**2) / (gen.probability_func(x) * n)        

        print 1 - stats.chi2.cdf(hi, k)
        return hi, k