"""Многомерная ИНТЕРПОЛЯЦИЯ"""
from  math import cos, pi, fabs, factorial, ceil
import numpy as np
from prettytable import PrettyTable


def f(x, y):
    return x ** 2 + y ** 2


def get_table(up_x, down_x, up_y, down_y, step, func):
    xs = [x for x in np.arange(up_x, down_x, step)]
    ys = [y for y in np.arange(up_y, down_y, step)]
    zs = []
    for y in np.arange(up_y, down_y + step, step):
        buf = []
        for x in np.arange(up_x, down_x + step, step):
            buf.append(func(x, y))
        zs.append(buf)
    return xs, ys, zs



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


def newton_interpolation(lst_x, lst_z, x):
    i = bin_search(lst_x, x)  # поиск ближайшего
    z_x = lst_z[0]
    for i in range(1, len(lst_0x)):
        k = 1
        for j in range(i):
           k *= (x - lst_x[j])
        dd = divided_difference(lst_x[:i+1], lst_z[:i+1])
        z_x += (k * dd)
    return z_x


def sequential_interpolation(xs, ys, zs, x, y, n, m):
    i_x = bin_search(xs, x)
    i_y = bin_search(ys, y)
    lx = len(xs)
    ly = len(ys)

    if i_y - (m + 1) / 2 < 0:  # если  х вначале
        sample_y = ys[:i_y + ceil((m + 1) / 2) + 1]
        sample_z = zs[:i_y + ceil((m + 1) / 2) + 1]
    elif ly < i_y + (m + 1) / 2:  # если х вконце
        sample_y = ys[i_y - ceil((m + 1) / 2):]
        sample_z = zs[i_y - ceil((m + 1) / 2):]
    else:
        if m % 2 != 0:
            sample_y = ys[i_y - ceil((m + 1) / 2): i_y + ceil((m + 1) / 2)]
            sample_z = zs[i_y - ceil((m + 1) / 2): i_y + ceil((m + 1) / 2)]
        else:
            sample_y = ys[i_y - ceil((m + 1) / 2) - 1: i_y + ceil((m + 1) / 2)]
            sample_z = zs[i_y - ceil((m + 1) / 2) - 1: i_y + ceil((m + 1) / 2)]

    left = 0
    right = 0

    if i_x - (n + 1) / 2 < 0:  # если  х вначале
        sample_x = xs[:i_x + ceil((n + 1) / 2) + 1]
        right = i_x + ceil((n + 1) / 2) + 1
    elif lx < i_x + (n + 1) / 2:  # если х вконце
        sample_x = xs[i_x - ceil((n + 1) / 2):]
        left = i_x - ceil((n + 1) / 2)
    else:
        if n % 2 != 0:
            sample_x = xs[i_x - ceil((n + 1) / 2): i_x + ceil((n + 1) / 2)]
            left = i_x - ceil((n + 1) / 2)
            right = i_x + ceil((n + 1) / 2)
        else:
            sample_x = xs[i_x - ceil((n + 1) / 2) - 1: i_x + ceil((n + 1) / 2)]
            left = i_x - ceil((n + 1) / 2) - 1
            right = i_x + ceil((n + 1) / 2)

    for i in range(len(sample_z)):
        sample_z[i] = sample_z[i][left:right]

    #print(sample_x, "\n", sample_y, "\n", sample_z)

    answ = []

    for i in range(len(sample_y)):
        answ.append(newton_interpolation(sample_x, sample_z[i], x))

    return newton_interpolation(sample_y, answ, y)


a = float(input('Введите нижнюю границу значений Х: '))
b = float(input('Введите верхнюю границу значений Х: '))
c = float(input('Введите нижнюю границу значений Y: '))
d = float(input('Введите верхнюю границу значений Y: '))
h = float(input('Введите шаг: '))

xss, yss, zss = get_table(a, b, c, d, h, func=f)

"""table = PrettyTable()
table.add_column("X", xss)
table.add_column("Y", yss)
#table.add_column("Z", zss)
#print(xss, "\n", yss, "\n\n", zss)
print(table)"""

try:
    x = float(input('Введите значение х в пределах [{0}, {1}]: '.format(a, b)))
    if x > b or x < a:
        x = float(input("X должен лежать в пределах [{0}, {1}]! Повторите ввод х: ".format(a,b)))
    n = int(input('Введите степень полинома для Х: '))
    if n < 0:
        n = int(input('Степень должна быть больше 0!\nПовторите ввод: '))

except ValueError:
    print("Неверный ввод! Повторите")
    x = float(input('Введите значение х в пределах [{0}, {1}]: '.format(a, b)))
    if x > b or x < a:
        x = float(input("X должен лежать в пределах [{0}, {1}]! Повторите ввод х: ".format(a, b)))
    n = int(input('Введите степень полинома ждля Х: '))
    if n < 0:
        n = int(input('Степень должна быть больше 0!\nПовторите ввод: '))


try:
    y = float(input('Введите значение y в пределах [{0}, {1}]: '.format(c, d)))
    if y > d or y < c:
        y = float(input("Y должен лежать в пределах [{0}, {1}]! Повторите ввод Y: ".format(c, d)))
    m = int(input('Введите степень полинома: '))
    if m < 0:
        m = int(input('Степень должна быть больше 0!\nПовторите ввод: '))

except ValueError:
    print("Неверный ввод! Повторите")
    y = float(input('Введите значение Y в пределах [{0}, {1}]: '.format(c, d)))
    if y > d or y < c:
        y = float(input("Y должен лежать в пределах [{0}, {1}]! Повторите ввод Y: ".format(c, d)))
    m = int(input('Введите степень полинома для  У: '))
    if m < 0:
        m = int(input('Степень должна быть больше 0!\nПовторите ввод: '))

int_res = sequential_interpolation(xss, yss, zss, x, y, n, m)
r_res = f(x, y)
absolute_error = fabs(int_res - r_res)
try:
    ratio_error = absolute_error / fabs(r_res)
except ZeroDivisionError:
    ratio_error = None
    print('Упс')
print("Результат при интерполяции: ", int_res, "\n", "Реальный результат:", r_res)
print("\nОтносителная ошибка: ", ratio_error)












