import numpy as np, math, cmath
N=5000
mu=np.ones(N+1,dtype=int); isp=np.ones(N+1,bool); isp[:2]=False
for p in range(2,N+1):
    if isp[p]: isp[2*p::p]=False; mu[p::p]*=-1; mu[p*p::p*p]=0
rng=np.random.default_rng(2); worst=0
for x in 1+ (N-2)*rng.random(200):
    d=np.arange(1,int(x)+1); m=mu[d]
    lhs=np.sum(m*np.log(1-np.exp(2j*np.pi*x/d)))
    H=np.sum(m*np.log(np.abs(2*np.sin(np.pi*x/d))))
    M=m.sum(); mm=np.sum(m/d)
    rhs=H+1j*math.pi*(x*mm-1-M/2)
    worst=max(worst,abs(lhs-rhs))
print("max |sum mu(d)log(1-e(x/d)) - [H + i pi(x m(x)-1-M/2)]| :",worst)
# H(n+) = sum_{d<=n, d∤n} mu(d) log|2 sin(pi n/d)| + Lambda(n)
def Lam(n):
    for p in range(2,n+1):
        if n%p==0:
            q=n
            while q%p==0: q//=p
            return math.log(p) if q==1 else 0.0
    return 0.0
worst=0; eps=1e-9
for n in range(2,400):
    d=np.arange(1,n+1); m=mu[d]
    Hp=np.sum(m*np.log(np.abs(2*np.sin(np.pi*(n+eps)/d))))
    reg=sum(int(mu[k])*math.log(abs(2*math.sin(math.pi*n/k))) for k in range(1,n+1) if n%k)
    worst=max(worst,abs(Hp-reg-Lam(n)))
print("max |H(n+) - reg(n) - Lambda(n)|, 2<=n<400 (eps=1e-9):",worst)
