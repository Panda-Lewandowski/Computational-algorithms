"""СПЛАЙН"""

from  math import cos, pi, sin
import numpy as np
from prettytable import PrettyTable


def get_table(up, down, step):
    xs = []
    ys = []
    for x in np.arange(up, down, step):
        xs.append(x)
        ys.append(sin(pi / 6 * x))
    return xs, ys


def bin_search(lst, x):
    a = 0
    b = len(lst) - 1
    while a < b:
        m = int((a + b) / 2)
        if x > lst[m]:
            a = m + 1
        else:
            b = m
    return b


def spline_interpolation(xs, ys, n, x):
    pos = bin_search(xs, x)
    h = [0 for i in range(n)]
    A = [0 for i in range(n)]
    B = [0 for i in range(n)]
    D = [0 for i in range(n)]
    F = [0 for i in range(n)]
    a = [0 for i in range(n)]
    b = [0 for i in range(n)]
    c = [0 for i in range(n + 1)]
    d = [0 for i in range(n)]
    ksi = [0 for i in range(n + 1)]
    eta = [0 for i in range(n + 1)]


    # находим шаги между каждым х
    for i in range(1, n):
        h[i] = xs[i] - xs[i - 1]

    # находим коэффициэнты 3-х диагональной слау, сравнивая с нашей системой
    for i in range(2, n):
        A[i] = h[i-1]
        B[i] = -2 * (h[i - 1] + h[i])
        D[i] = h[i]
        F[i] = -3 * ((ys[i] - ys[i - 1]) / h[i] - (ys[i - 1] - ys[i - 2]) / h[i - 1])

    # прямой ход
    for i in range(2, n):
        ksi[i + 1] = D[i] / (B[i] - A[i] * ksi[i])
        eta[i + 1] = (A[i] * eta[i] + F[i]) / (B[i] - A[i] * ksi[i])

    # обратный ход
    for i in range(n - 2, -1, -1):
        c[i] = ksi[i + 1] * c[i + 1] + eta[i + 1]

    ##c[n] =

    # ищем a, b, c
    for i in range(1, n):
        a[i] = ys[i - 1]
        b[i] = (ys[i] - ys[i - 1]) / h[i] - h[i] / 3 * (c[i + 1] + 2 * c[i])
        d[i] = (c[i + 1] - c[i]) / (3 * h[i])

    return a[pos] + b[pos] * (x - xs[pos - 1]) + c[pos] * ((x - xs[pos - 1]) ** 2) + d[pos] * ((x - xs[pos - 1]) ** 3)


a = float(input('Введите нижнюю границу значений Х: '))
b = float(input('Введите верхнюю границу значений Х: '))
n = int(input('Введите количество Х: '))

h = abs(a - b) / n
#print(a, b, n, h)

xss, yss = get_table(a, b, h)

table = PrettyTable()
table.add_column("X", xss)
table.add_column("Y", yss)

try:
    x = float(input('Введите значение х в пределах [{0}, {1}]: '.format(a, b)))
    if x > b or x < a:
        x = float(input("X должен лежать в пределах [{0}, {1}]! Повторите ввод х: ".format(a, b)))

except ValueError:
    print("Неверный ввод! Повторите")
    x = float(input('Введите значение х в пределах [{0}, {1}]: '.format(a, b)))
    if x > b or x < a:
        x = float(input("X должен лежать в пределах [{0}, {1}]! Повторите ввод х: ".format(a, b)))

print(table)
in_res = spline_interpolation(xss, yss, n, x)
r_res = sin(pi / 6 * x)
absolute_error = abs(in_res - r_res)
try:
    ratio_error = absolute_error / abs(r_res)
except ZeroDivisionError:
    ratio_error = None
    print('Упс')
print("Результат при интерполяции:  ", in_res)
print("Реальный результат:  ", r_res)
print("Абсолютная погрешность: {0:.5e}".format(absolute_error))
print("Относительная погрешность: {0:.5e}".format(ratio_error))
