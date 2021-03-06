"""Интерполяция методом полинома Ньютона"""
from  math import cos, pi, fabs, factorial
import numpy as np
from prettytable import PrettyTable


def get_table(up, down, step):
    xs = []
    ys = []
    for x in np.arange(up, down, step):
        xs.append(x)
        ys.append(cos(x))
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


def divided_difference(xs, ys):
    l = len(xs)
    if l == 1:
        return ys[0]
    else:
        return (divided_difference(xs[:-1], ys[:-1]) - divided_difference(xs[1:], ys[1:])) / (xs[0] - xs[l - 1])


def newton_interpolation(lst_x, lst_y, x, n):
    i = bin_search(lst_x, x)  # поиск ближайшего
    if len(lst_x) < i + (n + 1) / 2:  # если не получается взыть выборку с нужным х посередине
        sample_x = lst_x[len(lst_x) - (n + 1):]
        sample_y = lst_y[len(lst_y) - (n + 1):]
    else:
        if n % 2 != 0:  
            sample_x = lst_x[i - int((n + 1) / 2): i + int((n + 1) / 2)]
            sample_y = lst_y[i - int((n + 1) / 2): i + int((n + 1) / 2)]
        else:
            sample_x = lst_x[i - int((n + 1) / 2) - 1: i + int((n + 1) / 2)]
            sample_y = lst_y[i - int((n + 1) / 2) - 1: i + int((n + 1) / 2)]
    y_x = sample_y[0]
    for i in range(1, len(sample_x)):
        k = 1
        for j in range(i):
           k *= (x - sample_x[j])
        dd = divided_difference(sample_x[:i+1], sample_y[:i+1])
        y_x += (k * dd)
    return y_x


def gen_error(x, y_inter, n, xs):
    y_real = cos(x)
    diff = abs(y_real - y_inter)
    omega = x - xs[n]
    for i in range(0, n):
        omega *= (x - xs[i])
    omega = abs(omega)
    d = abs(cos(x + (pi * n)/2)) / factorial(n + 1)
    return diff <= d * omega


a = float(input('Введите нижнюю границу значений Х: '))
b = float(input('Введите верхнюю границу значений Х: '))
h = float(input('Введите шаг: '))

xss, yss = get_table(a, b, h)

table = PrettyTable()
table.add_column("X", xss)
table.add_column("Y", yss)

try:
    x = float(input('Введите значение х в пределах [{0}, {1}]: '.format(a, b)))
    if x > b or x < a:
        x = float(input("X должен лежать в пределах [{0}, {1}]! Повторите ввод х: ".format(a,b)))
    n = int(input('Введите степень полинома: '))
    if n < 0:
        n = int(input('Степень должна быть больше 0!\nПовторите ввод: '))

except ValueError:
    print("Неверный ввод! Повторите")
    x = float(input('Введите значение х в пределах [{0}, {1}]: '.format(a, b)))
    if x > b or x < a:
        x = float(input("X должен лежать в пределах [{0}, {1}]! Повторите ввод х: ".format(a, b)))
    n = int(input('Введите степень полинома: '))
    if n < 0:
        n = int(input('Степень должна быть больше 0!\nПовторите ввод: '))

print(table)
in_res = newton_interpolation(xss, yss, x, n)
r_res = cos(x)
absolute_error = fabs(in_res - r_res)
try:
    ratio_error = absolute_error / fabs(r_res)
except ZeroDivisionError:
    ratio_error = None
    print('Упс')
print("Результат при интерполяции:  ", in_res)
print("Реальный результат:  ", r_res)
print("Абсолютная погрешность: {0:.5e}".format(absolute_error))
print("Относительная погрешность: {0:.5e}".format(ratio_error))
print('Погрешность полинома Ньютона:', gen_error(x, in_res, n, xss))

