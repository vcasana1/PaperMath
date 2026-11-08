# W(X)=sum_{d<=X} mu(d) d Cl_2(2 pi {X/d})  (mu-twin of TP U01833) ;  W = -2 pi int_1^X H ; Mellin -(2pi/s) Fhat(s-1)/zeta(s-1)
import numpy as np, math, mpmath as mp
from scipy.special import bernoulli
from scipy.integrate import quad
exec(open('clausen_phi.py').read().split('print("Cl2 check')[0])   # reuse Cl2
N=400000
mu=np.ones(N+1,dtype=np.int64); isp=np.ones(N+1,bool); isp[:2]=False
for p in range(2,N+1):
    if isp[p]: isp[2*p::p]=False; mu[p::p]*=-1; mu[p*p::p*p]=0
def W(X):
    d=np.arange(1,int(X)+1,dtype=np.float64); return np.sum(mu[1:int(X)+1]*d*Cl2(2*np.pi*np.mod(X/d,1.0)))
def H(x):
    d=np.arange(1,int(x)+1,dtype=np.float64); return np.sum(mu[1:int(x)+1]*np.log(np.abs(2*np.sin(np.pi*x/d))))
for X in [57.3, 300.7]:
    I=quad(H,1,X,limit=4000,points=list(range(2,int(X)+1)))[0]
    print(f"X={X}: W={W(X):.6f}  -2pi int_1^X H={-2*math.pi*I:.6f}")
mp.mp.dps=15
Z=[mp.zetazero(j) for j in range(1,101)]
def A(s): return (mp.log(mp.pi)-mp.euler-mp.digamma(1-s/2)+1/s+2*mp.nsum(lambda k:(mp.zeta(2*k)-1)/(2*k-s),[1,mp.inf]))/s
cw=[-2*mp.pi*A(r)/((r+1)*mp.diff(mp.zeta,r)) for r in Z]
rng=np.random.default_rng(9)
for e in [3,4,5]:
    Xs=10.0**e*(1+rng.random(60))
    w=np.array([W(X) for X in Xs])
    pred=np.array([float(2*mp.re(sum(cw[j]*mp.mpf(X)**(Z[j]+1) for j in range(len(Z))))) for X in Xs])
    print(f"1e{e}: max|W|/X^1.5={np.max(np.abs(w)/Xs**1.5):.4f} rms W/X^1.5={np.sqrt(np.mean(w**2/Xs**3)):.4f}  corr(W,100-zero sum)={np.corrcoef(w,pred)[0,1]:.5f} slope={np.polyfit(pred,w,1)[0]:.4f}")
