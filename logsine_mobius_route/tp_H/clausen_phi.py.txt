# TP U01833: G(X)=sum_{q<X} phi(q) Cl_2(2 pi {X/q}) = c_Cl X^2 + o(X^2). Measure the error scale.
import numpy as np, math, mpmath as mp
from scipy.special import bernoulli, polygamma
from scipy.integrate import quad
Bn=bernoulli(80)
coef=[abs(Bn[2*k])/(2*k*(2*k+1)*math.factorial(2*k)) for k in range(1,36)]
def Cl2(theta):
    t=np.mod(theta+np.pi,2*np.pi)-np.pi
    a=np.abs(t); out=a-a*np.log(np.where(a>0,a,1.0))
    p=a.copy()
    for c in coef:
        p=p*a*a; out=out+c*p
    return np.sign(t)*out
print("Cl2 check:",Cl2(np.array([1.0,2.0,np.pi/3]))," mp:",[float(mp.clsin(2,x)) for x in [1.0,2.0,mp.pi/3]])
c=(6/math.pi**2)*quad(lambda t: float(mp.clsin(2,2*math.pi*t))*(-0.5*float(polygamma(2,1+t))),0,1,limit=200)[0]
print("c_Cl=",c)
N=400000
phi=np.arange(N+1,dtype=np.int64)
for p in range(2,N+1):
    if phi[p]==p: phi[p::p]-=phi[p::p]//p
rng=np.random.default_rng(4)
for e in [3,4,5]:
    Xs=np.unique((10**e*(1+rng.random(40))).astype(np.int64))
    E=[]
    for X in Xs:
        q=np.arange(2,X); G=np.sum(phi[2:X]*Cl2(2*np.pi*np.mod(X/q,1.0)))
        E.append(G-c*X*X)
    E=np.array(E,float)
    for a in [1.0,1.25,1.5]:
        pass
    print(f"X~1e{e}: rms E={np.sqrt(np.mean(E**2)):.4e}  rms/X={np.sqrt(np.mean(E**2))/np.mean(Xs):.4f}  rms/X^1.25={np.sqrt(np.mean(E**2))/np.mean(Xs**1.25):.4f} rms/X^1.5={np.sqrt(np.mean(E**2))/np.mean(Xs**1.5):.5f}")
