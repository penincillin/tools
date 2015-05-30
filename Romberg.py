#Implementation of Romberg algorithm(one kind of numerical integration)
#2015/05/30
#produced by Rong Yu

from numpy import *

f = lambda x : 2.0/sqrt(pi)*exp(-x)

eps = 1.0/10.0**5


if __name__ == '__main__':
    (b, a, n) = (1.0, 0.0, 0)
    h = b-a
    T = [[h/2*(f(a)+f(b))]]
    while True:
        tmp = 0.5*T[n][0]
        print '-----------------'
        for i in xrange(2**n):
            tmp += f( 0.5*1.0/(2**n) + 1.0/(2**n)*i )*h/2.0
            #print 0.5*1.0/(2**n) + 1.0/(2**n)*(i>0)
        T.append([tmp])
        for i in xrange(0,n+1):
            T[n+1].append( float(T[n+1][i]*4**(i+1) - T[n][i])/(4.0**(i+1) - 1.0) )
        if abs(T[n+1][n+1] - T[n][n])<eps:
            break
        n += 1
        h /= 2.0

    print T[n+1][n+1]
