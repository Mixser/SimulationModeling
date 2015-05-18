from __future__ import division

from math import pow, floor, ceil, sqrt

from scipy import stats

class PirsonTest(object):

    @staticmethod
    def check(n, k, gen):

        sequence = [gen.next for i in xrange(n)]

        h = ceil(max(sequence) - floor(min(sequence))) / k

        X = dict()

        start = min(sequence)
        
        for i in xrange(k):

            x_first, x_second = start + h * i, start + h * (i + 1)
            X[(x_first, x_second)] = 1
            for j in sequence:
                if j >= x_first and j < x_second:
                    X[(x_first, x_second)] += 1


        hi = 0
        i = 0
        for (x, value) in X.items():

            temp = float(value) - n * (gen.probability_func(x[1]) - gen.probability_func(x[0]))
            temp = temp * temp

            hi += temp / (n*(gen.probability_func(x[1]) - gen.probability_func(x[0])))
            i += 1
        hi = hi
        print 'P-value: ',1 - stats.chi2.cdf(hi, k)
        return '(hi^2, k): ',hi, k


class KolmagorovTest(object):
    @staticmethod
    def check(n, k, gen, eps):
        values = [gen.next for i in xrange(n)]
        Dn = KolmagorovTest.calculate_statistic(values, gen)

        pValue = 1 - stats.ksone.cdf(Dn, n)

        success = pValue > eps


        return Dn * sqrt(n), eps, pValue, success

    @staticmethod
    def calculate_statistic(values, gen):
        Dn = 0
        sorted_values = sorted(values)
        n = len(sorted_values)
        for i in xrange(1, n):
            diff1 = abs(i / n - gen.probability_func(sorted_values[i-1]))
            diff2 = abs((i-1)/n) - gen.probability_func(sorted_values[i-1])

            if diff1 > Dn:
                Dn = diff1

            if diff2 > Dn:
                Dn = diff2

        return Dn