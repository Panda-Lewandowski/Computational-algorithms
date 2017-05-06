import numpy as np
from prettytable import PrettyTable
from math import e, log, pow
from const import A, k, E
from jacobi import jacobi

# импортрруем данные
data = np.loadtxt('data.csv', delimiter=',')
T = [data[i][0] for i in range(9)]
Q = [data[i][1:] for i in range(9)]
Г = [e ** 2 / (k * Ti) for Ti in T]
Z = [0, 1, 2, 3, 4]
K = np.zeros((len(data), 4))
ΔE = np.zeros((len(data), 4))

for i in range(len(T)):
    for j in range(4):
        ΔE[i][j] = k * T[i] * log((1 + (Z[j + 1] ** 2) * (Г[i] / 2)) *
                                  (1 + (Г[i] / 2)) / (1 + (Z[j] ** 2) * (Г[i] / 2)))

for i in range(len(T)):
    for j in range(4):
        K[i][j] = 2 * A * Q[i][j + 1] / Q[i][j] * (T[i] ** 1.5) * (e ** ((-(E[j] - ΔE[i][j])) / (k * T[i])))

if __name__ == "__main__":
    p = float(input("Введите начальное давление р: "))
    table = PrettyTable()
    table.field_names = ["T", "X1", "X2", "X3", "X4", "Г"]
    for i in range(len(T)):
        #table.add_row(jacobi(p, k, T[i], Z, K[i]))
        print(jacobi(p, k, T[i], Z, K[i]))