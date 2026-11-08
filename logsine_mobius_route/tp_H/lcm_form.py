# Selberg-type identity: sum_{[d,e]=n} mu(d)mu(e) = mu(n)  =>  W(X) = sum_{d,e} mu(d)mu(e) k_X(d,e),
# k_X(d,e) = [d,e] Cl_2(2 pi X/[d,e]) if [d,e]<=X else 0.  Spectral position of the vector mu.
import numpy as np, math
exec(open('clausen_phi.py').read().split('print("Cl2 check')[0])
def mobius_upto(N):
    mu=np.ones(N+1,dtype=np.int64); isp=np.ones(N+1,bool); isp[:2]=False
    for p in range(2,N+1):
        if isp[p]: isp[2*p::p]=False; mu[p::p]*=-1; mu[p*p::p*p]=0
    return mu
for X in [300.5, 1000.5, 2500.5]:
    N=int(X); mu=mobius_upto(N)
    D=np.array([d for d in range(1,N+1) if mu[d]!=0]); v=mu[D].astype(float)
    g=np.gcd.outer(D,D); L=(D[:,None]*D[None,:])//g
    K=np.where(L<=X, L*Cl2(2*np.pi*np.mod(X/np.maximum(L,1),1.0)), 0.0)
    Wq=v@K@v
    d=np.arange(1,N+1,dtype=float); Wd=np.sum(mu[1:]*d*Cl2(2*np.pi*np.mod(X/d,1.0)))
    lam,U=np.linalg.eigh(K); c=U.T@v; w=c**2/np.sum(c**2)
    R=Wq/np.sum(v*v)
    order=np.argsort(-np.abs(lam)); cum=np.cumsum(w[order])
    top=lambda f: np.sum(w[order][:max(1,int(f*len(lam)))])
    print(f"X={X}: n={len(D)}  W(quad)={Wq:.6f} W(direct)={Wd:.6f}")
    print(f"   lam_max={lam.max():.3e} lam_min={lam.min():.3e}  Rayleigh(mu)={R:.3e}  X^0.5={X**0.5:.1f}")
    print(f"   weight of mu on top 1%/5%/20% |lam| eigvecs: {top(0.01):.4f} {top(0.05):.4f} {top(0.20):.4f}   (uniform would be .01 .05 .20)")
    print(f"   mean |lam| under mu-weights={np.sum(w*np.abs(lam)):.3e}   plain mean |lam|={np.mean(np.abs(lam)):.3e}")

print("\n--- split at |lam| = X^a ---")
for X in [1000.5, 2500.5, 5000.5]:
    N=int(X); mu=mobius_upto(N)
    D=np.array([d for d in range(1,N+1) if mu[d]!=0]); v=mu[D].astype(float)
    g=np.gcd.outer(D,D); L=(D[:,None]*D[None,:])//g
    K=np.where(L<=X, L*Cl2(2*np.pi*np.mod(X/np.maximum(L,1),1.0)), 0.0)
    lam,U=np.linalg.eigh(K); c=U.T@v
    for a in [0.25,0.5,0.75]:
        big=np.abs(lam)>X**a
        print(f"X={X} a={a}: #|lam|>X^a = {big.sum()}/{len(lam)}  mu-weight there={np.sum(c[big]**2)/np.sum(c**2):.2e}  W_big={np.sum(lam[big]*c[big]**2):.2f}  W_small={np.sum(lam[~big]*c[~big]**2):.2f}  X^1.5={X**1.5:.0f}")
