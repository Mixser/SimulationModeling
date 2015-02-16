class StatisticsUtils(object):
    @classmethod
    def E_k(cls, x, k=1):
        result = 0
        for i in x:
            result += i ** k
        result = float(result) / len(x)
        return result

    @classmethod
    def central_moments(cls, X, k=1):
        x = [x - cls.E_k(X) for x in X]
        return cls.E_k(x, k)

