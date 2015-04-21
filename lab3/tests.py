from __future__ import division

from abc import ABCMeta, abstractmethod

import io

from scipy.special import gammainc
from numpy.linalg import matrix_rank

from math import floor, exp



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



class BinaryMatriceTest(IRandomTest):



    @classmethod
    def rank(cls, matrice):
        rank = 0
        rt = 0 
        i = 0
        m = len(matrice)

        for k in xrange(0, m):
            i = k

            while rt >= m or matrice[i][rt] == 0:
                i = i + 1

                if( i < m ):
                    continue
                else:
                    rt += 1
                    if rt<m:
                      i=k
                      continue
                return rank

            rank += 1
            if i!=k:
                matrice[i], matrice[k] = matrice[k], matrice[i]

            for j in xrange(i+1, m):
                if matrice[j][rt] == 0 :
                    continue
                else:  
                    for z in xrange(0, m):
                        matrice[j][z] = matrice[j][z] ^ matrice[k][z];

            rt += 1

        return rank;  







    @classmethod
    def F_m(cls, m, matrices):
        result_m = 0
        result_m_1 = 0
        for matrice in matrices:
            r = cls.rank(matrice)

            if r == m:
                result_m += 1

            if r == m - 1:
                result_m_1 +=1 
        return result_m, result_m_1



    @classmethod
    def test_input(cls, input):
        if isinstance(input, list):
            bits = input
        else:
            bits = cls.get_bits_from_file(input)



        M = Q = 32

        N = int(floor(len(bits)/(M * Q)))

        print 'Count of matrices {0}'.format(N)

        matrices = []

        current = 0

        for i in xrange(N):

            matrice = [[0] * Q for i in xrange(M)]

            for row in xrange(M):
                for col in xrange(Q):
                    matrice[row][col] = bits[current]
                    current += 1

            matrices.append(matrice)



        F_m, F_m_1 = cls.F_m(M, matrices)

        print 'F_m={0} F_m_1={1} N - F_m - F_m_1 {2}'.format(F_m, F_m_1, N - F_m - F_m_1)


        first = ((F_m - 0.2888*N)*(F_m - 0.2888*N))/(0.2888 * N)
        second = ((F_m_1 - 0.5776*N)*(F_m_1 - 0.5776*N))/(0.5776 * N)
        third = ((N - F_m - F_m_1 - 0.1336 * N)*(N - F_m - F_m_1 - 0.1336 * N)) / (0.1336 * N)
        chi2 = first + second + third

        print chi2
        passed = False if exp(-chi2/2.0) < 0.01  else True
        return (chi2, exp(-chi2/2.0),  passed)







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
            print 'J less than 500 ({})'.format(J)

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

        passed = True

        for p_value in p_values:
            if p_value < 0.01:
                passed = False
        
        return (chi2s, p_values, passed)


if __name__ == '__main__':
    # results = BinaryMatriceTest.test_input([0,1,0,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,0,1])
    # results = BinaryMatriceTest.test_input('inputs/seq7.bin')
    results = RandomExcursionsTest.test_input('inputs/seq5.bin')
    print results