import math
from sympy import primerange, factorint, mobius, divisors, totient
def S_direct(k,h):
    s=0.0
    for a in range(1,k+1):
        if math.gcd(a,k)!=1 or (a+h)%k==0: continue
        s+=math.log(abs(2*math.sin(math.pi*(a+h)/k)))
    return s
def S_formula(k,h):
    s=0.0
    for d in divisors(k):
        m=mobius(d)
        if m==0: continue
        if h%d==0: s+=m*math.log(k/d)
        else: s+=m*math.log(abs(2*math.sin(math.pi*h/d)))
    return s
err=max(abs(S_direct(k,h)-S_formula(k,h)) for k in range(2,80) for h in range(0,60))
print("max|S_direct-S_formula| k<80,h<60:",err)
# E = -gamma + sum_p log p/(p-1)^2
g=0.5772156649015329
tail=0.0
s=sum(math.log(p)/(p-1)**2 for p in primerange(2,10**7))
print("E approx", -g+s, "(primes<1e7; tail ~ 1/1e7)")
