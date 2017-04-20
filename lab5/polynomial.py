class Polynomial:
    def __init__(self, n, k=None):
        self.degree = n
        if k is None:
            self.koef = [0 for i in range(n + 1)]
        else:
            if len(k) > n:
                k = k[:n + 1]
            self.koef = [x for x in k]

    def __imul__(self, other):
        """Multiplication polynomial by the number"""
        for i in range(len(self.koef)):
            self.koef[i] *= other
        return self

    def __isub__(self, other):
        """Subtraction of polynomials"""
        if self.degree < other.degree:
            return None
        else:
            i = other.degree
            j = self.degree
            while i != -1:
                self.koef[j] -= other.koef[i]
                i -= 1
                j -= 1
            return self

    def up_degree(self) :
        """...or multiplication polynomial by x"""
        self.degree += 1
        self.koef.append(0)

    def get(self, x):
        """Substitution x"""
        res = 0
        for i in range(self.degree + 1):
            res += (self.koef[i] * (x ** (self.degree - i)))
        return res

    def __str__(self):
        i = self.degree
        prnt_str = ""
        for k in self.koef:

            if not i:
                prnt_str += " + {0}".format(k)
            else:
                if k:
                    if i != self.degree:
                        prnt_str += " + "
                    prnt_str += "{0}x^{1}".format(k, i)
            i -= 1
        return  prnt_str


if __name__ == "__main__":
    """Tests"""

    p = Polynomial(0, [1,2,3])
    print(p)

    p = Polynomial(3)
    print(p)

    p = Polynomial(2, [3, 2, 1])
    print(p)

    l = Polynomial(3, [9, 8, 7, 6])
    print(l, "\n")

    l *= 2
    print(l)

    l -= p
    print(l)

    l.up_degree()
    print(l)