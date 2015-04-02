from math import pow

from scipy import stats

class PirsonTest(object):

    @staticmethod
    def check(n, k, gen):

        sequence = [gen.next for i in xrange(0, n)]

        minimum = min(sequence)
        maximum = max(sequence)
        h = float(maximum - minimum) / k
        segments = []
        frequency = []
        segments.append(round(h + minimum))

        for index in xrange(0, k):
            segments.append(round(segments[index] + h))
            frequency.append(0)

        for i in xrange(0, n):
            j = 0
            while sequence[i] >= segments[j]:
                j += 1
                if j == k:
                    j -= 1
                    break
            frequency[j] += 1
        hi = 0

        p = lambda i: gen.distribution_func(minimum + i * h) - gen.distribution_func((i-1) * h + minimum)

        for i in xrange(1, k):
            hi += float((frequency[i] - p(i) * n)**2) / n * p(i)        

        print len(frequency)
        print 1 - stats.chi2.cdf(hi, k)
        return hi, k