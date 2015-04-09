from abc import ABCMeta, abstractmethod

import io

from scipy.special import gammainc

VALUES = [-4,-3,-2,-1,1,2,3,4]

class IRandomTest(object):
    __metaclass__ = ABCMeta


    @classmethod
    def get_bits_from_file(cls, file_path):
        result = []
        io.BytesIO
        with open(file_path, 'rb') as f:
            bytes = (ord(b) for b in f.read())
            for b in bytes:
                for i in xrange(8):
                    result.append((b >> i) & 1)

        return result


    @abstractmethod
    def test_input(cls, input):
        pass

class RandomExcursionsTest(IRandomTest):

    @classmethod
    def __generate_x(cls, bits):
        return [2 * e - 1 for e in bits]

    @classmethod
    def __generate_s(cls, X):
        S = []
        sum = 0
        for i in xrange(1, len(X)+1):
            sum += X[i-1]
            S.append(sum)
        S = [0] + S + [0]
        return S

    @classmethod
    def __calculate_cicles(cls, S):
        cicles = []
        start = 0
        J = 0
        for i in xrange(1, len(S)):
            if S[i] == 0:
                J = J + 1
                cicles.append(S[start:i+1])
                start = i
        return cicles, J


    @classmethod
    def __v_k(cls, k,x,cicles):
        result = 0
        for cicle in cicles:
            if k != 5:
                if cicle.count(x) == k:
                    result += 1
            else:
                if cicle.count(x) >= k:
                    result += 1
        return result


    @classmethod 
    def __pi_k(cls, x, k):
        if k == 0:
            return 1 - 1.0/(2 * abs(x))

        if k == 5:
            return 1.0 /(2 * abs(x)) * (1 - 1.0/(2*abs(x)))**4

        return 1.0/(4 * x**2)*(1- 1.0/(2 * abs(x)))**(k-1)





    @classmethod
    def test_input(cls, input):
        if isinstance(input, list):
            bits = input
        else:
            bits = RandomExcursionsTest.get_bits_from_file(input)

        print 'Get {0} bites from {1}'.format(len(bits), input)

        X = cls.__generate_x(bits)
        print 'X was generated.'
        S = cls.__generate_s(X)
        print 'S was generated.'
        cicles, J = cls.__calculate_cicles(S)

        print 'Cicles was generated.'

        if J < 500:
            raise ValueError("This input is bad")

        # frequence = [[0] * 8 for i in xrange(0, len(cicles))]

        # for i,cicle in enumerate(cicles):
        #     for j,value in enumerate(VALUES):
        #         frequence[i][j] += cicle.count(value)


        chi2s = []
        p_values = []
        print 'Start calculating chi2 for values'

        

        for x in VALUES:
            print 'Calculating for {0} value'.format(x)
            chi2 = 0
            for k in xrange(0, 6):
                q = (cls.__v_k(k, x, cicles) - J * cls.__pi_k(x, k))**2
                p = J * cls.__pi_k(x, k)
                chi2 += float(q) / p
            chi2s.append(chi2)
            p_values.append(1 - gammainc(5.0/ 2, chi2/2.0))
        print 'Test finished.'
        
        return (chi2s, p_values)


if __name__ == '__main__':
    results = RandomExcursionsTest.test_input('inputs/seq1.bin')
    print results