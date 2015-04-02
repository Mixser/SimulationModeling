from math import pow

class PirsonTest(object):

    def check(self,n, k, gen):
        sequence = [gen.next for i in xrange(0, n)]


        min_value = min(sequence)
        max_value = max(sequence)


        
        h = float(max_value - min_value) /  k

        print min_value, max_value, h


        segments = [min_value + h]
        print segments

        frequence = [0.0 for i in xrange(0, k + 1)]
        print 'h', h
        for i in xrange(1, k):
            print segments
            segments.append(segments[i-1] + h)

        for i in xrange(0, n):
            j = 0
            while (sequence[i] >= segments[j]):
                j += 1
                if (j == k):
                    j -= 1
                    break
            frequence[j] += 1

        hi = 0.0

        print frequence

        for i in xrange(0, k):
            print '->', frequence[i], n * gen.probability_func(segments[i])
            h = frequence[i] - n * gen.probability_func(segments[i])
            d = n * gen.probability_func(i)
            print h, d

            hi += h * h / d

        return hi