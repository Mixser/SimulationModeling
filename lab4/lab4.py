from numpy.random import laplace, uniform

import matplotlib.pyplot as plt

values = uniform(0, 1, 10000)

print sum(values) / float(len(values))

n, bins, patches = plt.hist(values, 1000, normed=True, facecolor='green', alpha=0.75)

plt.title("Sample moments: ")

plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.axis([-2.0, 2.0, 0, 5.0])
plt.grid(True)

plt.show()