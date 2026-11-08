import numpy as np, math
C=0.74379486183940054; c1=math.log(2)-C; g=0.5772156649015329
rng=np.random.default_rng(7)
N=20000
d=np.zeros(N+1,dtype=np.int64)
for i in range(1,N+1): d[i::i]+=1
nn=np.arange(1,N+1,dtype=np.float64); dd=d[1:].astype(np.float64)*nn**-0.75
def G(y):
    k=np.arange(1,int(y)+1,dtype=np.float64); return np.sum(np.log(np.abs(2*np.sin(np.pi*(y/k)))))
def Delta(y):
    k=np.arange(1,int(y)+1,dtype=np.float64); return np.sum(np.floor(y/k))-y*math.log(y)-(2*g-1)*y-0.25
ys=10**5*(1+3*rng.random(300))
R=np.array([G(y)-c1*y for y in ys]); D=np.array([Delta(y) for y in ys])
ph=np.array([4*np.pi*np.sqrt(nn*y)-np.pi/4 for y in ys])
S=np.array([ys[i]**0.25*np.sum(dd*np.sin(ph[i])) for i in range(len(ys))])
Cc=np.array([ys[i]**0.25*np.sum(dd*np.cos(ph[i])) for i in range(len(ys))])
for name,v in [("Delta",D),("R",R)]:
    A=np.vstack([S,Cc]).T
    coef,res,_,_=np.linalg.lstsq(A,v,rcond=None)
    fit=A@coef
    print(name,"coef(sin,cos)=",coef,"  corr=",np.corrcoef(fit,v)[0,1], " 1/(pi sqrt2)=",1/(math.pi*math.sqrt(2))," 1/sqrt2=",1/math.sqrt(2))
# sign identity check
import sympy
bad=0
for p in sympy.primerange(3,20000):
    s=sum(int(p//k) for k in range(2,p)) % 2
    if s != int(math.isqrt(p))%2: bad+=1
print("sign law violations p<2e4:",bad)
