import numpy as np, math, mpmath as mp, sympy
from sympy import totient, mobius
# Euler product constants
pr=list(sympy.primerange(2,10**6))
P1=np.prod([1+1/(p*p*(p-1)) for p in pr]); A1=np.prod([1+1/(p*(p-1)) for p in pr])
print("prod(1+1/(p^2(p-1)))=",P1,"  V=(prod-1)/4=",(P1-1)/4,"   A(1)=",A1)
# DFT identity: sum_{r=1}^{k-1} log(2 sin(pi r/k)) e(-mr/k) =? log k + gamma + (psi(m/k)+psi(1-m/k))/2
g=float(mp.euler); worst=0
for k in range(2,60):
    r=np.arange(1,k); l=np.log(2*np.sin(np.pi*r/k))
    for m in range(1,k):
        lhs=np.sum(l*np.exp(-2j*np.pi*m*r/k))
        rhs=math.log(k)+g+0.5*(float(mp.digamma(m/k))+float(mp.digamma(1-m/k)))
        worst=max(worst,abs(lhs-rhs))
print("max |DFT - (log k + A(m/k))| k<60:",worst)
# variance of F_y over h: direct sampling vs Parseval with formula (8)
y=60
ks=list(range(2,y+1)); phis={k:int(totient(k)) for k in ks}
def Sk(k,h):
    s=0.0
    for d in sympy.divisors(k):
        mu=int(mobius(d))
        if mu==0: continue
        s+= mu*math.log(k/d) if h%d==0 else mu*math.log(abs(2*math.sin(math.pi*h/d)))
    return s
rng=np.random.default_rng(5)
hs=rng.integers(1,10**15,size=6000)
F=np.array([sum(Sk(k,int(h))/phis[k] for k in ks) for h in hs])
M=sum(math.log(k)/k for k in ks)
print("y=",y," sample mean F=",F.mean()," M_y=",M,"  sample var=",F.var())
def Ahat(t): return g+0.5*(float(mp.digamma(t))+float(mp.digamma(1-t)))
par=0.0
for q in range(2,y+1):
    mq=int(mobius(q))
    if mq==0: continue
    for a in range(1,q):
        if math.gcd(a,q)!=1: continue
        c=mq/int(totient(q))*sum((math.log(q*j)+Ahat(a/q))/(q*j) for j in range(1,y//q+1))
        par+=c*c
print("Parseval from (8):",par,"   (1/4)(prod-1)log^4 y=",(P1-1)/4*math.log(y)**4,"  0.084946 log^4 y=",0.084946*math.log(y)**4)
