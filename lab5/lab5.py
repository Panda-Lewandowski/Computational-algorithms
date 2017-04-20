from math import pi, e, erf, sqrt
from bisection import bisection_xy
import integral



def f(x):
    return (1 / sqrt(2 * pi)) * (e ** (- (x ** 2) / 2))


def F(x, α):
    global n, f
    return integral.integrate(0, x, n, f) - α


if __name__ == "__main__":
    a = float(input('Введите нижнюю границу значений Х: '))
    b = float(input('Введите верхнюю границу значений Х: '))
    alpha = float(input('Введите  α: '))
    n = int(input('Введите максимальную степень полинома Лежандра: '))

    print(bisection_xy(a, b, alpha, 0.001, F))

