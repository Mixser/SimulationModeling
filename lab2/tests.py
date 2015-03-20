from math import pow

class PirsonTest(object):

    def check(self,n, k, gen):
        sequence = [gen.next for i in xrange(0, n)]


        min_value = min(sequence)
        max_value = max(sequence)
        h = float(max_value - min_value) /  k

        segments = [min_value + h]

        frequence = [0 for i in xrange(0, k)]

        for i in xrange(1, k):
            segments.append(segments[i-1] + h)

        for i in xrange(0, n):
            j = 0
            while (sequence[i] > segments[j]):
                j += 1
                if (j == k):
                    j -= 1
                    break
            frequence[j] += 1

        hi = 0.0
        for j in xrange(0, k):
            hi += pow(frequence[j] - gen.probability_func(h * j), 2) / gen.probability_func(h * j)

        return hi

