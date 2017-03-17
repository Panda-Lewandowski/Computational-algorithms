"""Обратная интерполяция"""
from math import cos, sin, pi, fabs, ceil, log
from prettytable import PrettyTable

relative_accuracy = 0.001

left_fist = -5
right_first = 1

left_second = -3
right_second = 3


def f(x, y):
    return x ** 3 - 15 * y + 4


def g(x, y):
    return cos(x) - y


def bisection(a, b, x, eps, f):
    if f(x, a) == eps:
        return a
    if f(x, b) == eps:
        return b
    c = (a + b) / 2
    while abs(b - a) > eps * abs(c) + eps:
        c = (a + b) / 2
        if f(x, b) * f(x, c) < 0:
            a = c
        else:
            b = c
    return (a + b) / 2


def for_first_equation(x):
    return bisection(left_fist, right_first, x, relative_accuracy, f)


def for_second_equation(x):
    return bisection(left_fist, right_first, x, relative_accuracy, g)


def create_table(left, right, step, function):
    x = []
    y = []

    while left <= right:
        x.append(left)
        y.append(function(left))
        left += step

    return [x, y]


def find_beg(x, table, size, near, deg):
    deg += 1
    if near == 0 and table[near] > x:
        return 0

    if near == size - 1 and table[near] < x:
        return size - deg - 1

    if x <= table[near]:
        if near < deg / 2:
            return 0
        if (size - 1 - near) < (ceil(deg / 2) - 1):
            return size - deg - 1
        return near - deg / 2

    if x > table[near]:
        if near < (ceil(deg / 2) - 1):
            return 0
        if size - 1 - deg < deg / 2:
            return size - 1 - deg
        return near - (ceil(deg / 2) - 1)

    return 0


def nearest_value(x, table, size):
    if x < table[0]:
        return 0

    if x > table[size - 1]:
        return size - 1\

    diff = fabs(x - table[0])
    first_y = 0

    for i in range(1, size):
        if fabs(x - table[i]) < diff:
            first_y = i
            diff = fabs(x - table[i])

    return first_y


def newton_interpolation(x, degree, beginnig, table_x, table_y):
    result = table_y[beginnig]

    for i in range((beginnig + 1), beginnig + degree):
        divided = 0
        for j in range(beginnig, i + 1):
            difference = 1
            for k in range(beginnig, i + 1):
                if (k != j):
                    difference *= (table_x[j] - table_x[k])
            divided += (table_y[j] / difference)
        for k in range(beginnig, i):
            divided *= (x - table_x[k])
        result += divided

    return result


a = float(input('Введите левый предел: \n'))
b = float(input('ВВедите правый предел: \n'))
step = float(input("Вывдете шаг: \n"))

x_column_first, y_column_first = create_table(a, b, step, for_first_equation)

x_column_second, y_column_second = create_table(a, b, step, for_second_equation)

x_result, y_result = [], []

for index in range(len(y_column_first)):
    y_result.append(x_column_first[index])
    x_result.append(y_column_second[index] - y_column_first[index])

table_data = PrettyTable()
table_data.add_column('X', x_result)
table_data.add_column('Y(X)', y_result)
print(table_data)

degree = int(input('Enter degree of Newton\'s polynomial: \n'))
x = 0

for_first_y = nearest_value(x, x_result, len(x_result))
beginning = find_beg(x, x_result, len(x_result), for_first_y, degree)

result = newton_interpolation(x, degree, int(beginning), x_result, y_result)

print('\n -------- Results -------- \n')
print('X = ', result)
y_first = for_first_equation(result)
y_second = for_second_equation(result)
print('Y = ', y_first + (y_second - y_first) / 2)
