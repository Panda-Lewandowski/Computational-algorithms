from math import exp, log
import numpy

def input_table():
    f = open("1.txt", "r")
    T = []
    for line in f:
        l = line.split()
        T.append([float(l[0]), float(l[1]), float(l[2]), float(l[3]),float(l[4])])
    #print(T)
    return T

class gas:
    def __init__(self, P0, T0, Tw, m, n, T, E):
        self.P0 = P0
        self.T0 = T0
        self.Tw = Tw
        self.m = m
        self.n = n
        self.T = T
        self.E = E

def kol_razb_lezh(a, b, ntek, nn):
    sh = (b-a)/ntek
    xpr = a
    xt = a+sh
    k = 0;
    #KRC = []
    for i in range(ntek):
        if(poly(xpr, nn)*poly(xt, nn) <= 0):
            #KRC.append(bin_div(xpr, xt, nn, 1e-7))
            k += 1;
        xpr = xt
        xt = xpr+sh
    #print(KRC)
    #print(len(KRC))
    #print(ntek)
    #print(k," ", nn)
    if k < nn:
        ntek = kol_razb_lezh(a, b, ntek*2, nn)
        #print("RR - ", ntek)
    return ntek

def bin_div(a, b, n, eps):
    c = (b+a)/2
    while(abs(b-a) > abs(c)*eps+eps):
        c = (b+a)/2
        if poly(a, n)*poly(c, n) < 0:
            b = c
        else:
            a = c
    return c

def poly(x, n):
    p0 = 1
    p1 = x
    for i in range(2, n+1):
        p = (2*i-1)/i*x*p1 - (i-1)/i*p0
        p0 = p1
        p1 = p
    return p

def lezh(n):
    A = []
    ntek = kol_razb_lezh(-1, 1, n*2, n)
    #print(ntek)
    sh = 2/ntek
    xp = -1
    xt = xp+sh
    for i in range(ntek):
        if(poly(xp, n)*poly(xt, n) <= 0):
            A.append(bin_div(xp, xt, n, 1e-10))
        xp = xt
        xt = xp+sh
    return A

def koef(AK, n):
    M = []
    V = []
    #print(AK)
    #print(n)
    #print(len(AK))
    for i in range(n):
        M.append([])
    for i in range(n):
        for j in range(n):
            M[i].append(AK[j]**i)
        if i%2 == 0:   
            V.append(2/(i+1))
        else:
            V.append(0)
    #
    #T = gauss(M, V, n)
    #
    T = numpy.linalg.solve(M, V)
    """
    if T == 0:
        return 0
    
    V = T[1]
    return V
    """
    return T

def upt(M, V, n):
    for i in range(n-1):
        max_n = i
        max_z = abs(M[i][i])
        for j in range(i+1, n):
            znach = M[j][i]
            if znach > max_z:
                max_n = j
                max_z = znach


        if max_n > i:
            t = M[i]
            M[i] = M[max_n]
            M[max_n] = t

            t = V[i]
            V[i] = V[max_n]
            V[max_n] = t
        else:
            if(abs(max_z) <= 1e-40):
                #print(M)
                return [[-1]]


        znach = M[i][i]
        for j in range(i+1, n):
            koef = M[j][i]/znach
            for k in range(n):
                M[j][k] -= M[i][k]*koef
            V[j] -= V[i]*koef
        #print("i: ",i, M)

    if abs(M[n-1][n-1]) <= 1e-20:
        #print(M)
        return [[-1]]
    return M

def gauss(M, V, n):
    M = upt(M, V, n)
    #print(M)
    #print(V)
    if M[0][0] == -1:
        return [[[-1]], [-1]]

    for i in range(n-1, -1, -1):
        if i != n-1:
            for j in range(i+1, n):
                V[i] -= M[i][j]*V[j]
        V[i] /= M[i][i]
    return [M, V]

def get_DE(gamm, T, i, Z):
    return 8.617*(10**-5)*T*(log(((1+Z[i]*Z[i]*(gamm/2))*(1+(gamm/2)))/(1+Z[i-1]*Z[i-1]*(gamm/2))))

def interpol(X, X0, X1, Y0, Y1):
    return Y0+(Y1-Y0)*(X-X0)/(X1-X0) 

def get_Q(T, i, gas):
    ind = 0
    while(gas.T[ind][0] < T):
        ind += 1
    if(gas.T[ind][0] == T):
        return gas.T[ind][i]
    if(ind == 0):
        return interpol(T, gas.T[0][0], gas.T[1][0], gas.T[0][i], gas.T[1][i])
    else:
        return interpol(T, gas.T[ind-1][0], gas.T[ind][0], gas.T[ind-1][i], gas.T[ind][i])
    
def get_k(T, gas, i, gamm, Z):
    return 4.830*(10**-3)*(get_Q(T, i+1, gas)/get_Q(T, i, gas))*(T**(3/2))*exp(-(E[i-1]-get_DE(gamm, T, i, Z))*11603/T)

def get_alpha(gamm, T):
    return 0.285*(10**-11)*((gamm*T)**3)

def get_gamm(T, X, Z):
    eps = 1e-7
    a = 0
    b = 2
    c = (a+b)/2
    while(abs(b-a) > eps*abs(c)+eps):
        ta = 0
        tc = 0
        for i in range(2, 5):
            ta+= (exp(X[i])*Z[i-1]*Z[i-1])/(1+Z[i-1]*Z[i-1]*a/2)
            tc+= (exp(X[i])*Z[i-1]*Z[i-1])/(1+Z[i-1]*Z[i-1]*c/2)
            #print(i)

            
        G1 = a**2 - 5.87*(10**10)*(1/(T**3))*(exp(X[0])/(1+(a/2)) + ta)
        G2 = c**2 - 5.87*(10**10)*(1/(T**3))*(exp(X[0])/(1+(c/2)) + tc)
        #print("G1 - ", G1)
        #print("G2 - ", G2)
        if(G1*G2 < eps):
            b = c
        else:
            a = c
        c = (a+b)/2
    return c

    

def solve_system(T, p, X, gas):
    eps = 1e-7
    
    flag = 1
    Z = [0,1,2,3,4]
    Gam = 0
    while(flag):
        Dx = []
        Fun = []
        Mk = []
        for i in range(5):
            Mk.append([])

        Mk[0] = [1, -1, 1, 0, 0]
        Mk[1] = [1, 0, -1, 1, 0]
        Mk[2] = [1, 0, 0, -1, 1]
        
        temp = []
        temp.append(exp(X[0]))
        temp.append(0)
        temp.append(-Z[1]*exp(X[2]))
        temp.append(-Z[2]*exp(X[3]))
        #print(X[4])
        temp.append(-Z[3]*exp(X[4]))
        Mk[3] = temp
        
        temp = []
        temp.append(-exp(X[0]))
        temp.append(-exp(X[1]))
        temp.append(-exp(X[2]))
        temp.append(-exp(X[3]))
        temp.append(-exp(X[4]))
        Mk[4] = temp

        Fun.append(-(X[0]+X[2]-X[1]-log(get_k(T, gas, 1, Gam, Z))))
        Fun.append(-(X[0]+X[3]-X[2]-log(get_k(T, gas, 2, Gam, Z))))
        Fun.append(-(X[0]+X[4]-X[3]-log(get_k(T, gas, 3, Gam, Z))))
        Fun.append(-(exp(X[0])-Z[1]*exp(X[2])-Z[2]*exp(X[3])-Z[3]*exp(X[4])))
        Fun.append(-(7242*p/T - exp(X[0]) - exp(X[1]) - exp(X[2]) - exp(X[3]) - exp(X[4]) + get_alpha(Gam, T)))

        temp = []
        Dx = Fun
        #
        #temp = gauss(Mk, Dx, 5)
        #
        #Dx = temp[1]
        #
        Dx = numpy.linalg.solve(Mk, Dx)

        max_ = Dx[0]/X[0]
    
        #print(Dx)
        #print(X)
        
        for i in range(1, 5):
            t = Dx[i]/X[i]
            if (t > max_):
                max_ = t
        #print(Dx)
        #print(X)
        
        for i in range(5):
            X[i] += Dx[i]
            
        Gam = get_gamm(T, X, Z)
        #print(Gam)
        
        if(abs(max_) < eps ):
            flag = 0
            break
    return X
        
        
        

def find_nt(T, p, gas):
    X = [log(0.1), 1, 1, -5, -15]
    X = solve_system(T, p, X, gas)
    N = []
    for i in range(1, 5):
        N.append(exp(X[i]))
    Nt = 0
    for i in range(4):
        Nt+=N[i]
    return Nt

def integrate(gas):
    eps = 1e-7
    a = 5
    b = 25
    c = (a+b)/2
    t = lezh(gas.n)
    A = koef(t, gas.n)
    while(abs(b-a) > eps*abs(c)+eps):
        z = []
        Tz = [] 
        Nt1 = []
        Nt2 = []
        for i in range(gas.n):
            z.append((1/2)*t[i]+1/2)
            Tz.append(gas.T0+(gas.Tw - gas.T0)*(z[i]**gas.m))
            Nt1.append(find_nt(Tz[i], a, gas))
            Nt2.append(find_nt(Tz[i], c, gas))
        int_a = 7242*gas.P0/Tn
        int_c = 7242*gas.P0/Tn
        sum_a = 0
        sum_c = 0
        for i in range(gas.n):
            sum_a += A[i]*Nt1[i]*z[i]
            sum_c += A[i]*Nt2[i]*z[i]

        """
        print("int:")
        print(int_a)
        print(int_c)
        print("sum:")
        print(sum_a)
        print(sum_c)
        print()
        """
        
        int_a -= sum_a
        int_c -= sum_c

        """
        print(int_a)
        print(int_c)
        print()
        """
        
        if(int_a*int_c < eps):
            b = c
        else:
            a = c
        c = (a+b)/2
    p = c
    return p


P0 = float(input("Введите начальное давление: "))
Tn = float(input("Введите Tnach: "))
T0 = float(input("Введите T0: "))
Tw = float(input("Введите Tw: "))
m = int(input("Введите m: "))
n = int(input("Введите степень полинома лежандра: "))
T = input_table()
E = [12.13, 20.98, 31.0, 45.0]
G = gas(P0, T0, Tw, m, n, T, E)
p = integrate(G)
print("Рабочее давление: ", p)





