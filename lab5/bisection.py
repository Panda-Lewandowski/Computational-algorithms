
def bisection_x(a, b, eps, f):
    if f(a) == eps:
        return a
    if f(b) == eps:
        return b
    c = (a + b) / 2
    while abs(b - a) > eps * abs(c) + eps:
        c = (a + b) / 2
        if f(b) * f(c) < 0:
            a = c
        else:
            b = c
    return (a + b)/2


def bisection_xy(a, b, k, eps, f):
    if f(a, k) == eps:
        return a
    if f(b, k) == eps:
        return b
    c = (a + b) / 2
    while abs(b - a) > eps * abs(c) + eps:
        c = (a + b) / 2
        if f(b, k) * f(c, k) < 0:
            a = c
        else:
            b = c
    return (a + b)/2
