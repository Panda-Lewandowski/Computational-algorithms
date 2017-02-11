import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.lines as plt_lines
from prettytable import PrettyTable


def function(x, y):
    return math.exp(x**3 - y) - x**6 + 2*(x**3)*y+2*(x**3)-y**2-2*y-2


def find_points(x_start, x_end, y_start, y_end, eps, f):
    xs = [x_start]
    ys = [y_start]
    h = eps # DO NOT CHANGE THIS CONSTANT
    rng = h
    y_now = y_start
    for x in np.arange(x_start + h, x_end, h):
        answ = round(bisection(y_now - rng, y_now + rng, x, eps, f), 4)
        xs.append(x)
        ys.append(answ)
        y_now = answ
        rng += h
    xs.append(x_end)
    ys.append(y_end)
    return [xs, ys]


def bisection(a, b, x, eps, f):
    if f(x, a) == eps:
        return a
    if f(x, b) == eps:
        return b
    while b - a > eps:
        c = (a + b) / 2
        if f(x, b) * f(x, c) < 0:
            a = c
        else:
            b = c
    return (a + b)/2


def trapezium_method(down, up, h,  ys):
    n = int((up - down) / h)
    integral = 0
    for i in range(0, n):
        integral += abs(ys[i] + ys[i + 1])/2
    return integral * h

x, y = find_points(0, 2, -0.35, 7.64, 1e-2, function)

table = PrettyTable()
table.add_column("X", x)
table.add_column("Y", y)
print(table)

i = trapezium_method(0, 2, 1e-2, y)
plt.figure('F(x,y) = e^(x^3 - y) - x^6 + 2(x^3) * y + 2(x^3)- y^2 - 2y - 2 = 0 ')
x = np.array(x)
y = np.array(y)
plt.plot(x, y, color='r', linewidth=1.0)
plt.subplot(111).spines['bottom'].set_position('zero')
plt.ylabel("y")
plt.xlabel("x")
plt.grid(True)
plt.text(0, 6, "INTEGRAL \n {0:.4f}".format(i))
plt.show()



