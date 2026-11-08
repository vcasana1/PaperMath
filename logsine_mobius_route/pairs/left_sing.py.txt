# H(x)=sum_{d<=x} mu(d) log|2 sin(pi x/d)| near integers n: left limit ~ -mu(n) log(eps), right limit finite
import numpy as np, math
N=200
mu=np.ones(N+1,dtype=int); isp=np.ones(N+1,bool); isp[:2]=False
for p in range(2,N+1):
    if isp[p]: isp[2*p::p]=False; mu[p::p]*=-1; mu[p*p::p*p]=0
def H(x):
    d=np.arange(1,int(math.floor(x))+1); return np.sum(mu[d]*np.log(np.abs(2*np.sin(np.pi*x/d))))
print(" n  mu(n)  [H(n-1e-6)-H(n-1e-9)]/log(1e3)   [H(n+1e-6)-H(n+1e-9)]/log(1e3)")
for n in [6,7,10,12,30,36,97,100]:
    L=(H(n-1e-6)-H(n-1e-9))/math.log(1e3); R=(H(n+1e-6)-H(n+1e-9))/math.log(1e3)
    print(f"{n:3d} {mu[n]:4d}   {L:8.4f}   {R:8.4f}")
