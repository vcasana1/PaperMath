import numpy as np, math, mpmath as mp
mp.mp.dps=20
X=2*10**6
mu=np.ones(X+1,dtype=np.int64); isp=np.ones(X+1,bool); isp[:2]=False
for p in range(2,X+1):
    if isp[p]:
        isp[2*p::p]=False; mu[p::p]*=-1; mu[p*p::p*p]=0
dm=np.nonzero(mu[1:])[0]+1; mv=mu[dm].astype(float)
def H(x):
    sel=dm<=x; d=dm[sel].astype(float)
    return np.sum(mv[sel]*np.log(np.abs(2*np.sin(np.pi*x/d))))
rng=np.random.default_rng(3)
def A(s):
    return mp.log(2*mp.pi)/s+1/s**2+mp.nsum(lambda k: mp.zeta(2*k)/(k*(2*k-s)),[1,mp.inf])
Z=[mp.zetazero(j) for j in range(1,151)]
W=[A(r)/mp.diff(mp.zeta,r) for r in Z]
print("A(rho1)=",mp.nstr(A(Z[0]),8),"  |A(rho1)|*|rho1|=",mp.nstr(abs(A(Z[0]))*abs(Z[0]),6))
for e in [3,4,5,6]:
    xs=10.0**e*(1+rng.random(150))
    h=np.array([H(x) for x in xs])
    pred=np.array([float(2*mp.re(sum(W[j]*mp.mpf(x)**Z[j] for j in range(len(Z))))) for x in xs])
    print(f"1e{e}: rms H/sqrt x={np.sqrt(np.mean(h**2/xs)):.4f}  corr(H, 150-zero sum)={np.corrcoef(h,pred)[0,1]:.4f}  slope={np.polyfit(pred,h,1)[0]:.3f}")
