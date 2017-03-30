from PyQt5 import QtWidgets, uic
from  math import sin, pi, fabs, pow
from random import uniform
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QTableWidgetItem
import matplotlib.pyplot as plt

#TODO если получен сигнал изменения ячейки счиать


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
        self.css = None
        self.err_up = None
        self.err_down = None



def fill_table(win, func):
    a = win.x_b.value()
    b = win.x_e.value()
    h = win.x_h.value()
    win.err_up = win.eps_b.value()
    win.err_down = win.eps_e.value()
    win.xss = []
    win.yss = []
    win.pss = []

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
        win.xss.append(a)
        win.yss.append(func(a) + r)
        win.pss.append(1)
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
        item_y = win.table.item(i, 1)
        item_p = win.table.item(i, 2)
        print(i, item_x.text())
        print("\n")

def solve(win):
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

        D = np.linalg.inv(A)
        D = np.matrix(D)
        C = D * B

        C = C.transpose()
        win.css = C.ravel()
        draw(win)


def approx_func(win):
    n = win.d.value() + 1
    a = win.x_b.value()
    b = win.x_e.value()
    xs = np.arange(a, b, 0.01)
    ys = []
    for x in xs:
        y = 0
        for j in range(n):
            y += win.css[0, j] * pow(x, j)
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
        app_x, app_y = approx_func(win)
        plt.figure("Среднеквадратичное приближение")
        plt.plot(x, y, color='r', linewidth=1.0, label="Фактический результат")
        plt.plot(real_x, real_y, color='g', linewidth=1.0, label="Реальный результат")
        plt.plot(app_x, app_y, color='b', linewidth=1.0, label="Аппроксимация")
        plt.grid(True)
        plt.xlabel(u'X')
        plt.ylabel(u'Y')
        plt.legend()
        plt.show()


def add_row(win):
    win.table.insertRow(win.table.rowCount())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())