# W-analogue of TP U00605 (mu = 2 mu_u - mu_u*mu_u*1 on n<=u^2):
# W(X) = 2 W_u(X) - sum_{d,j<=u} mu(d)mu(j) dj G(X/(dj)),  G(Y)=sum_{l<=Y} l Cl_2(2 pi Y/l),  u >= sqrt X
# G(Y) = pi (C - log 2) Y^2 + E_G(Y)   (pole of zeta(s-1) at s=2; C = 0.7437948618...)
import numpy as np, math
exec(open('clausen_phi.py').read().split('print("Cl2 check')[0])
C=0.74379486183940054; cG=math.pi*(C-math.log(2))
N=400000
mu=np.ones(N+1,dtype=np.int64); isp=np.ones(N+1,bool); isp[:2]=False
for p in range(2,N+1):
    if isp[p]: isp[2*p::p]=False; mu[p::p]*=-1; mu[p*p::p*p]=0
def Gs(Y):
    l=np.arange(1,int(Y)+1,dtype=float); return np.sum(l*Cl2(2*np.pi*np.mod(Y/l,1.0)))
def Wfull(X,u=None):
    n=int(X if u is None else min(X,u)); d=np.arange(1,n+1,dtype=float)
    return np.sum(mu[1:n+1]*d*Cl2(2*np.pi*np.mod(X/d,1.0)))
print("c_G = pi(C-log2) =",cG)
rng=np.random.default_rng(1)
for e in [3,4,5]:
    Ys=10.0**e*(1+rng.random(20)); E=np.array([Gs(Y)-cG*Y*Y for Y in Ys])
    print(f"Y~1e{e}: G/Y^2 mean={np.mean([Gs(Y)/Y**2 for Y in Ys[:5]]):.5f}  rms E_G/Y^0.75={np.sqrt(np.mean(E**2/Ys**1.5)):.4f}  rms E_G/Y={np.sqrt(np.mean(E**2/Ys**2)):.4f}")
for X in [5000.5, 30000.5]:
    u=math.sqrt(X); U=int(u); D=np.arange(1,U+1); mD=mu[1:U+1]
    bil=0.0; mainpart=0.0; Epart=0.0
    for d in D[mD!=0]:
        for j in D[mD!=0]:
            Y=X/(d*j)
            if Y<1: continue
            g=Gs(Y); s=mu[d]*mu[j]*d*j
            bil+=s*g; mainpart+=s*cG*Y*Y; Epart+=s*(g-cG*Y*Y)
    mu_u=np.sum(mD/D)
    rhs=2*Wfull(X,u)-bil
    print(f"X={X}: W={Wfull(X):.4f}  2W_u - bilinear={rhs:.4f} | 2W_u={2*Wfull(X,u):.1f}  main=-cG X^2 m_u^2={-cG*X*X*mu_u**2:.1f} (check {-mainpart:.1f})  E-part={-Epart:.1f}  X^1.5={X**1.5:.0f}")
print("--- where B_E lives: split by Y = X/(dj) ---")
for X in [30000.5, 120000.5]:
    u=math.sqrt(X); U=int(u); D=np.arange(1,U+1); sq=D[mu[1:U+1]!=0]
    parts={}
    for d in sq:
        js=sq[sq*d<=X]; Y=X/(d*js)
        for jj,YY in zip(js,Y):
            val=mu[d]*mu[jj]*d*jj*(Gs(YY)-cG*YY*YY)
            key='Y<=4' if YY<=4 else ('4<Y<=64' if YY<=64 else 'Y>64')
            parts[key]=parts.get(key,0.0)+val
    print(f"X={X}: " + "  ".join(f"{k}: {-v:.0f}" for k,v in parts.items()) + f"   total E-part {-sum(parts.values()):.0f}  X^1.5={X**1.5:.0f}")
