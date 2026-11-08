# (i) sum_{d>=1} mu(d) log|sinc(x/d)| = log|1-x^2|
# (ii) H(x) = log|x^2-1| + sum_{d<=x} mu(d) log(2 pi x/d) - sum_{d>x} mu(d) log sinc(x/d)
# (iii) sum over Farey fractions a/q in (0,1), q<=N, of log|2 sin(pi a/q)| = psi(N)
import numpy as np, math
D=4*10**6
mu=np.ones(D+1,dtype=np.int8); isp=np.ones(D+1,bool); isp[:2]=False
for p in range(2,int(D**0.5)+1):
    if isp[p]: isp[p*p::p]=False
for p in np.nonzero(isp)[0]:
    mu[p::p]*=-1; mu[p*p::p*p]=0
d=np.arange(1,D+1,dtype=np.float64); m=mu[1:].astype(np.float64)
def logsinc(y): return np.log(np.abs(np.sin(np.pi*y)/(np.pi*y)))
rng=np.random.default_rng(11)
print("(i)/(ii): x, sum mu log|sinc(x/d)| (d<=4e6), log|1-x^2|, H direct, H via identity")
for x in [2.37, 17.61, 1234.5678, 98765.4321]:
    s=np.sum(m*logsinc(x/d))
    sel=d<=x
    Hd=np.sum(m[sel]*np.log(np.abs(2*np.sin(np.pi*x/d[sel]))))
    Hi=math.log(abs(x*x-1))+np.sum(m[sel]*np.log(2*math.pi*x/d[sel]))-np.sum(m[~sel]*logsinc(x/d[~sel]))
    print(f"{x:12.4f} {s:14.8f} {math.log(abs(1-x*x)):14.8f} {Hd:14.8f} {Hi:14.8f}")
# (iii) Farey
for N in [10,100,1000,3000]:
    tot=0.0
    for q in range(2,N+1):
        a=np.arange(1,q); a=a[np.gcd(a,q)==1]
        tot+=np.sum(np.log(2*np.sin(np.pi*a/q)))
    psi=sum(math.log(p)*int(math.log(N)/math.log(p)+1e-12) for p in range(2,N+1) if all(p%r for r in range(2,int(p**0.5)+1)))
    print(f"Farey N={N}: sum log|2 sin| = {tot:.8f}   psi(N) = {psi:.8f}")
