# Rigorous upper bound for C_zeta = sum_n Lambda(n) * h(log n) * n^(-sigma1), h = hypot(A0,B0),
#   A0(L) = -(cR1 + cR2 L)/pi,  B0(L) = ((exp(-d L)-2)/L - cI2 L - cI3 L^2/2)/pi,  sigma1 = 1/2+d.
# Exact Arb sum for n <= N0 (all prime powers), tail n > N0 by partial summation with psi(x) <= 1.03883 x
# (Rosser-Schoenfeld 1962, Thm 12) and monotonicity of g(x)=h(log x) x^(-sigma1) on [N0,oo).
import sys, json, time, numpy as np
from fractions import Fraction as Fr
from flint import arb, acb, ctx
ctx.prec=256
def A(q): return arb(q.numerator)/arb(q.denominator) if isinstance(q,Fr) else arb(q)
sol=json.load(open(sys.argv[1])); N0=int(float(sys.argv[2]))
d=Fr(sol['d']).limit_denominator(10**6); c={tuple(b):Fr(x) for b,x in zip(sol['B'],sol['c'])}
assert set(c)=={('R',1),('R',2),('I',2),('I',3)}
dA=A(d); s1=A(Fr(1,2)+d); PI=arb.pi()
cR1,cR2,cI2,cI3=[A(c[k]) for k in [('R',1),('R',2),('I',2),('I',3)]]
assert cR1>0 and cR2>0
def h(L):
    A0=-(cR1+cR2*L)/PI; B0=(((-dA*L).exp()-2)/L-cI2*L-cI3*L*L/2)/PI
    return (A0*A0+B0*B0).sqrt()
t0=time.time()
s=np.ones(N0+1,np.bool_); s[:2]=False
for i in range(2,int(N0**0.5)+1):
    if s[i]: s[i*i::i]=False
P=np.nonzero(s)[0]; del s
tot=arb(0); psi=arb(0)
for p in P.tolist():
    lp=arb(p).log(); n=p; k=1
    while n<=N0:
        L=k*lp; tot+=lp*h(L)*(-s1*L).exp(); psi+=lp; n*=p; k+=1
print('primes',len(P),' partial sum (n<=%d) ='%N0,tot.str(15),' psi(N0) =',psi.str(15),' %.0fs'%(time.time()-t0),flush=True)
# monotonicity on [L0,oo): (log h)' <= (|A0'|+|B0'|)/|A0| <= [cR2 + 2/L0^2 + d/L0 + |cI2|]/(cR1+cR2 L0) + |cI3|/cR2  < sigma1
L0=arb(N0).log()
bound=(cR2+2/(L0*L0)+dA/L0+abs(cI2))/(cR1+cR2*L0)+abs(cI3)/cR2
print('(log h)\' bound on [log N0,oo):',bound.str(10),' < sigma1 =',s1.str(10),bound<s1)
assert bound<s1
# integral int_{L0}^{L1} h(L) e^{(1-sigma1)L} dL (rigorous, acb.integral) + [L1,oo) bound with |A0|+|B0| <= poly
L1=arb(600)
def f(z,an):
    A0=-(acb(cR1)+acb(cR2)*z)/PI; B0=(((-acb(dA)*z).exp()-2)/z-acb(cI2)*z-acb(cI3)*z*z/2)/PI
    return (A0*A0+B0*B0).sqrt(analytic=an)*((1-acb(s1))*z).exp()
I1=acb.integral(f,acb(L0),acb(L1)).real
a=s1-1
def inc(k,X):  # int_X^oo L^k e^{-a L} dL
    from math import factorial
    return (-a*X).exp()*sum(arb(factorial(k))/factorial(i)*X**i/a**(k-i+1) for i in range(k+1))
I2=(abs(cR1)*inc(0,L1)+abs(cR2)*inc(1,L1)+3*inc(0,L1)+abs(cI2)*inc(1,L1)+abs(cI3)/2*inc(2,L1))/PI   # 2/L+1/L <= 3 for L>=1
gN0=h(L0)*(-s1*L0).exp()
tail=gN0*(arb('1.03883')*N0-psi)+arb('1.03883')*(I1+I2)
Cz=tot+tail
print('tail <= ',tail.str(10),'  (integral',I1.str(10),', far tail',I2.str(5),')')
print('C_zeta <',Cz.upper().str(12,radius=False),'   time %.0fs'%(time.time()-t0))
