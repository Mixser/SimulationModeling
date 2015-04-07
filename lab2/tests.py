from math import pow

from scipy import stats

class PirsonTest(object):

    @staticmethod
    def check(n, gen):

        sequence = [gen.next for i in xrange(0, n)]

        X = dict()

        for x in sequence:
            if x in X:
                X[x] += 1
            else: 
                X[x] = 1

        k = len(X)

        hi = 0
        i = 0
        for (x, value) in X.items():

            temp = float(value) - n * gen.probability_func(x)
            print 'val->', value
            temp = temp * temp

            print i, x, temp, (n*gen.probability_func(x))
            hi += temp / (n*gen.probability_func(x))
            i += 1
        hi = hi
        print 'P-value: ',1 - stats.chi2.cdf(hi, k)
        return '(hi^2, k): ',hi, k