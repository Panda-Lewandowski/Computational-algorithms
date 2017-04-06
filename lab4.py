"""Differentiation"""
from  math import pi, fabs, e, pow, log
import numpy as np
from prettytable import PrettyTable
from itertools import combinations


def f(x):
    return pow(e, x)


def get_table(up, down, step, func):
    xs = []
    ys = []
    for x in np.arange(up, down + step, step):
        xs.append(x)
        ys.append(func(x))
    return xs, ys


def left_side_diff(ys, h):
    l = [None]
    for i in range(1, len(ys)):
        l.append((ys[i] - ys[i - 1]) / h)
    return l


def right_side_diff(ys, h):
    l = []
    for i in range(0, len(ys) - 1):
        l.append((ys[i + 1] - ys[i]) / h)
    l.append(None)
    return l


def centre_diff(ys, h):
    l = [None]
    for i in range(1, len(ys) - 1):
        l.append((ys[i + 1] - ys[i - 1]) / (2 * h))
    l.append(None)
    return l


def extreme_points(ys, h):
    l = []
    l.append((-3 * ys[0] + 4 * ys[1] - ys[2]) / (2 * h))
    for i in range(1, len(ys) - 1):
        l.append(None)
    l.append((ys[len(ys) - 3] - 4 * ys[len(ys) - 2] + 3 * ys[len(ys) - 1]) / (2 * h))
    return l


def runge(ys, h, r):
    l = [None, None]
    for i in range(2, len(ys) - 2):
        yh = (ys[i + 1] - ys[i - 1]) / (2 * h)
        y2h = (ys[i + r] - ys[i - r]) / (2 * h * r)
        l.append(yh + (yh - y2h) / (r ** 2 - 1))
    l.append(None)
    l.append(None)
    return l


def levelling(xs, ys, h):
    etas = [log(y) for y in ys]
    l = centre_diff(etas, h)
    new_l = []
    for i in range(len(l)):
        if l[i] is None:
            new_l.append(None)
        else:
            new_l.append(l[i] * ys[i])
    return new_l


def divided_difference(xs, ys):
    l = len(xs)
    if l == 1:
        return ys[0]
    else:
        return (divided_difference(xs[:-1], ys[:-1]) - divided_difference(xs[1:], ys[1:])) / (xs[0] - xs[l - 1])


def polinomial(xs, ys, x):
    z = [x - xi for xi in xs]
    y_on_x = divided_difference(xs[:2], ys[:2])
    for i in range(1, len(z)):
        it = combinations(z[:i + 1], i)
        sum = 0
        for k in it:
            if k is not None:
                p = 1
                for i in range(len(k)):
                    p *= k[i]
                sum += p
        y_on_x += (sum * divided_difference(xs[:i + 2], ys[:i + 2]))
    return y_on_x


a = float(input('Введите нижнюю границу значений Х: '))
b = float(input('Введите верхнюю границу значений Х: '))
h = float(input('Введите шаг: '))

xss, yss = get_table(a, b, h, f)
left = left_side_diff(yss, h)
right = right_side_diff(yss, h)
centre = centre_diff(yss, h)
exrt = extreme_points(yss, h)
r = runge(yss, h, 2)
lev = levelling(xss, yss, h)

table = PrettyTable()
table.add_column("X", xss)
table.add_column("Y", yss)
table.add_column("Левостороняя", left)
table.add_column("Правостороняя", right)
table.add_column("Центральная", centre)
table.add_column("Повышенная точность", exrt)
table.add_column("Рунге", r)
table.add_column("Выравнивающие", lev)
print(
    "+-----+--------------------+-----------------------------------------------------------------------------------------------------------------------------+\n"
    "|                          |                                                y'(x)                                                                        |")
print(table)
x = float(input('Введите  Х: '))
print("\nПолиномиальные формулы:", polinomial(xss, yss, x), '\n')
print("Реальный результат: ", f(x))
