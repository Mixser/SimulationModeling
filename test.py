from congruential_generators import LinearCongruentialGenerator

g1 = LinearCongruentialGenerator(a=7, c=7, x0=7, m=10)

g2 = LinearCongruentialGenerator(a=2, c=2, x0=7, m=10)

print g1.get_list(10)
print g2.get_list(10)

x0 = x_prev = g1.next

x1 = x_k = g1.next

print (x0, x1)

while x_k != 0:
    x_prev = x_k
    x_k = g1.next

m = 10
f = False
k = 1
while not f:
    k += 1

    a = (k * m) / x_prev
    c = (k * m) % x_prev

    if a * x_prev + c == k * m and (a * x0 + c) % m == x1:
        f = True

print a, c