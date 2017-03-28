from PyQt5 import QtWidgets, uic
from  math import sin, pi
from random import randrange
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QTableWidgetItem


def f(x):
    return x * sin(x / pi) / 5


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.autofill.clicked.connect(lambda: fill_table(self))


def fill_table(win):
    a = win.x_b.value()
    b = win.x_e.value()
    h = win.x_h.value()
    eps_up = win.eps_b.value()
    eps_down = win.eps_e.value()

 #если вдруг не влезет расширить

    col = win.table.currentColumn()
    row = win.table.currentRow()
    print(col, row)
    ap = 0
    for i in np.arange(a, b, h):
        item = QTableWidgetItem()
        win.table.itemAt(col, row).setText('lol')
        row += 1






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())