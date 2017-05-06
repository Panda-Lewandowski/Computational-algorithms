from math import log, e
import numpy as np
import matrix

def jacobi(p, k, T, Z, K):
    # начальные значения
    Xe = log(0.1)
    X = [0, 0, -5, -15]
    dXe = log(0.1)
    dX = [0, 0, -5, -15]
    A = np.zeros((5, 5))
    B = np.zeros((5, 1))

    while dXe / Xe > 0.01:
        Xe = dXe
        dX = dX[:]
        # заполняем матрицы
        B[0] = -e ** Xe + e ** X[0] + e ** X[1] + e ** X[2] + e ** X[3] - (p / k / T)
        B[1] = -Z[1] * e ** X[1] - Z[2] * e ** X[2] - Z[3] * e ** X[3] + e ** Xe
        B[2] = - Xe - X[1] + X[0] + log(K[0])
        B[3] = - Xe - X[2] + X[1] + log(K[1])
        B[4] = - Xe - X[3] + X[2] + log(K[2])

        A[0][0] = e ** Xe
        for i in range(1, 5):
            A[0][i] = e ** X[i - 1]

        A[1][0] = - e ** Xe
        A[1][2] = Z[1] * e ** X[1]
        A[1][3] = Z[2] * e ** X[2]
        A[1][4] = Z[3] * e ** X[3]

        A[2][0] = 1
        A[2][1] = -1
        A[2][2] = 1

        A[3][0] = 1
        A[3][2] = -1
        A[3][3] = 1

        A[4][0] = 1
        A[4][3] = -1
        A[4][4] = 1

        A = nparray_to_list(A)
        B = B.ravel()

        D = matrix.inv(A)
        R = matrix.multi(D, B)

        dXe = R[0]
        dX = R[1:]

    return dXe, dX


def nparray_to_list(a):
    a = list(a)
    for i in range(len(a)):
        a[i] = list(a[i])
    return a



if __name__ == "__main__":
    print(jacobi(1000, 8, 2000, [0, 1,2,3, 4], [2,4,6,4,5]))
