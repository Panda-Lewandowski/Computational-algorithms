from polynomial import Polynomial
import copy
from bisection import bisection_x


def legendre(n):
    roots = []
    roots_inter = []
    h = 2 / n
    a = -1
    b = a + h
    l = get_legendge_polynomial(n)

    while len(roots_inter) != n:
        roots_inter = []

        while b <= 1:
            if l.get(a) * l.get(b) < 0:
                roots_inter.append([a, b])
            a = b
            b += h

        h /= 2
        a = -1
        b = a + h

    for i in roots_inter:
        roots.append(bisection_x(i[0], i[1], 0.00001, l.get))
    return roots


def get_legendge_polynomial(n):
    if not n:
        return Polynomial(0, [1])
    if n == 1:
        return Polynomial(1, [1, 0])

    zero = Polynomial(0, [1])
    one = Polynomial(1, [1, 0])
    leg = None
    m = 1
    for i in range(n - 1):
        buf_one = copy.deepcopy(one)
        buf_zero = copy.deepcopy(zero)

        buf_one.up_degree()
        buf_one *= ((2 * m + 1)/(m + 1))
        buf_zero *= (m / (m + 1))
        buf_one -= buf_zero

        zero = one
        one = buf_one

        m += 1

    return one




if __name__ == "__main__":

    p = get_legendge_polynomial(2)

    l = legendre(7)
    print(l)

