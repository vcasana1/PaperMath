# Mean squares over x in [X,2X] of W_Q (d<=X^{4/5}) and W_alto (X^{4/5}<d<=x), in units of X^3
import numpy as np, math
exec(open('clausen_phi.py').read().split('print("Cl2 check')[0])
N=200000
mu=np.ones(N+1,dtype=np.int64); isp=np.ones(N+1,bool); isp[:2]=False
for p in range(2,N+1):
    if isp[p]: isp[2*p::p]=False; mu[p::p]*=-1; mu[p*p::p*p]=0
rng=np.random.default_rng(8)
for X in [5000,20000,80000]:
    Q=int(X**0.8); xs=X*(1+rng.random(150))
    lo=[];hi=[];lo1=[];hi1=[]
    for x in xs:
        d=np.arange(1,int(x)+1,dtype=float); w=d*Cl2(2*np.pi*np.mod(x/d,1.0)); m=mu[1:int(x)+1]
        lo.append(np.sum((m*w)[:Q])); hi.append(np.sum((m*w)[Q:])); lo1.append(np.sum(np.abs(m)*w)[()] if False else np.sum((np.abs(m)*w)[:Q])); hi1.append(np.sum((np.abs(m)*w)[Q:]))
    f=lambda a: np.mean(np.array(a)**2)/X**3
    print(f"X={X} Q=X^0.8={Q}:  mu: <W_Q^2>/X^3={f(lo):.3f}  <W_alto^2>/X^3={f(hi):.3f}   |mu| (chi=1): <W_Q^2>/X^3={f(lo1):.3f}  <W_alto^2>/X^3={f(hi1):.1f}")
