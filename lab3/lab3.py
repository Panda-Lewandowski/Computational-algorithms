from PyQt5 import QtWidgets, uic
from math import sin, pi, fabs, pow
from random import uniform
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QTableWidgetItem
import matplotlib.pyplot as plt
import gauss_seidel


def f(x):
    return x * sin(x / pi) / 5


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.autofill.clicked.connect(lambda: fill_table(self, f))
        self.table.setSortingEnabled(True)
        self.solve.clicked.connect(lambda: solve(self))
        self.addrow.clicked.connect(lambda: add_row(self))
        self.xss = []
        self.yss = []
        self.pss = []
        self.css_np = None
        self.css = []
        self.err_up = None
        self.err_down = None



def fill_table(win, func):
    a = win.x_b.value()
    b = win.x_e.value()
    h = win.x_h.value()
    win.err_up = win.eps_b.value()
    win.err_down = win.eps_e.value()
    c = fabs(a - b) / h
    cr = win.table.rowCount()
    if c > cr:
        diff = c - cr
        for i in range(int(diff) + 1):
            win.table.insertRow(win.table.rowCount())

    for i in range(int(c) + 1):
        item_x = QTableWidgetItem("{0:.3f}".format(a))
        r = uniform(win.err_up, win.err_down)
        item_y = QTableWidgetItem("{0:.3f} ".format(func(a) + r))
        item_p = QTableWidgetItem("{0:.2f}".format(1))
        """win.xss.append(a)
        win.yss.append(func(a) + r)
        win.pss.append(1)"""
        win.table.setItem(i, 0, item_x)
        win.table.setItem(i, 1, item_y)
        win.table.setItem(i, 2, item_p)
        a += h


def read_table(win):
    win.xss = []
    win.yss = []
    win.pss = []
    r = win.table.rowCount()
    for i in range(r):
        item_x = win.table.item(i, 0)
        if item_x:
            win.xss.append(float(item_x.text()))
    for i in range(r):
        item_y = win.table.item(i, 1)
        if item_y:
            win.yss.append(float(item_y.text()))
    for i in range(r):
        item_p = win.table.item(i, 2)
        if item_p:
            win.pss.append(float(item_p.text()))


def solve(win):
    read_table(win)
    if len(win.xss) == 0 or len(win.yss) == 0:
        QtWidgets.QErrorMessage(win).showMessage("Таблица не заполнена!", 'warning')
    else:
        n = win.d.value() + 1
        N = len(win.xss)
        A = np.zeros((n, n))
        B = np.zeros((n,1))
        for j in range(n):
            for k in range(n):
                for i in range(N):
                    A[j, k] += pow(win.xss[i], k + j) * win.pss[i]
            for i in range(N):
                B[j] += win.yss[i] * pow(win.xss[i], j) * win.pss[i]

        if win.lib.isChecked():
            D = np.linalg.inv(A)
            D = np.matrix(D)
            C = D * B
            C = C.transpose()
            win.css_np = np.array(C.ravel())
            win.css_np = nparray_to_list(win.css_np)[0]
            #draw(win)

        nparray_to_list(A)
        nparray_to_list(B)
        win.css = gauss_seidel.gauss_seidel(A, B, 0.0001)
        draw(win)


def approx_func(win, coefs):
    n = win.d.value() + 1
    a = win.x_b.value()
    b = win.x_e.value()
    xs = np.arange(a, b, 0.01)
    ys = []
    for x in xs:
        y = 0
        for j in range(n):
            y += coefs[j] * pow(x, j)
        ys.append(y)

    return xs, ys


def draw(win):
    if len(win.xss) == 0 or len(win.yss) == 0:
        QtWidgets.QErrorMessage(win).showMessage("Таблица не заполнена!", 'warning')
    else:
        x = np.array(win.xss)
        y = np.array(win.yss)
        a = win.x_b.value()
        b = win.x_e.value()
        real_x = np.arange(a, b, 0.01)
        real_y = [f(x) for x in real_x]
        app_x, app_y = approx_func(win, win.css)

        plt.figure("Среднеквадратичное приближение")
        plt.scatter(x, y, color='r', s=10, alpha=.5, label="Фактический результат")

        if win.lib.isChecked():
            np_x, np_y = approx_func(win, win.css_np)
            plt.plot(np_x, np_y, color='m', linewidth=1.0, label="NumPy")
        plt.plot(app_x, app_y, color='b', linewidth=1.0, label="Аппроксимация")
        plt.plot(real_x, real_y, color='black', linewidth=0.5, label="Реальный результат")
        plt.grid(True)
        plt.xlabel(u'X')
        plt.ylabel(u'Y')
        plt.legend()
        plt.show()


def add_row(win):
    win.table.insertRow(win.table.rowCount())


def nparray_to_list(a):
    a = list(a)
    for i in range(len(a)):
        a[i] = list(a[i])
    return a

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
