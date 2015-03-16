import matplotlib.pyplot as plt

from utils import StatisticsUtils

from congruential_generators import LinearCongruentialGenerator, \
    MacLarenMarsaglia, SquareCongruentialGenerator, CongruentialGenerator


def init_generator(klass):
    if not issubclass(klass, CongruentialGenerator):
        raise ValueError("Generator must be a CongruentialGenerator type")
    kwargs = {}
    for param in klass.NEEDED_PARAMS:
        kwargs[param] = int(raw_input('%s: ' % param))

    return klass(**kwargs)

def init_generators():
    g1 = LinearCongruentialGenerator(a=106, c=, x0=1, m=6075)
    # g1 = init_generator(LinearCongruentialGenerator)

    g2 = SquareCongruentialGenerator(a=106, b=1283, c=123, x0=1, m=6075)
    # g2 = init_generator(SquareCongruentialGenerator)

    X = LinearCongruentialGenerator(a=106, c=1283, x0=1, m=2 * 6075)
    Y = SquareCongruentialGenerator(a=106, b=1283, c=123, x0=1, m=2 * 6075)


    g3 = MacLarenMarsaglia(k=256, X=X, Y=Y)

    return (g1, g2, g3)


if __name__ == '__main__':
    n, s = 50, 10
    generators = init_generators()

    for generator in generators:
        values = generator.get_list(n)
        raw_moment = StatisticsUtils.E_k(values, s)
        central_moments = StatisticsUtils.central_moments(values, s)
        print values[:3000]
        print "Raw moments: %s;" % raw_moment
        print "Central moments: %s;" % central_moments
        values = values[:3000]
        plt.plot(values[:-1], values[1:], 'ro')

        plt.axis([0, 1.0, 0, 1.0])

        plt.show()
