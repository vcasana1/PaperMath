# G(y)=sum_{k<=y} log|2 sin(pi y/k)| at non-integer y; R(y)=G(y)-(log2-C)y
import numpy as np, math
C=0.74379486183940054
c1=math.log(2)-C
rng=np.random.default_rng(1)
def G(y):
    k=np.arange(1,int(y)+1,dtype=np.float64)
    return np.sum(np.log(np.abs(2*np.sin(np.pi*(y/k)))))
def Dfloor(y):  # Delta(y)=sum_{k<=y} floor(y/k) - y log y -(2g-1)y
    k=np.arange(1,int(y)+1,dtype=np.float64)
    return np.sum(np.floor(y/k)) - y*math.log(y) - (2*0.5772156649015329-1)*y
print("scale  N   rms R   rms R / y^{1/4}   rms Delta / y^{1/4}   mean R")
for e in [3,4,5,6,7]:
    Y=10.0**e
    N=400 if e<7 else 60
    ys=Y*(1+rng.random(N))   # random real y in [Y,2Y)
    R=np.array([G(y)-c1*y for y in ys])
    D=np.array([Dfloor(y) for y in ys])
    sc=np.mean(ys**0.5)**0.5
    print(f"1e{e} {N:4d} {np.sqrt(np.mean(R**2)):10.4f} {np.sqrt(np.mean(R**2))/sc:10.4f} {np.sqrt(np.mean(D**2))/sc:10.4f} {np.mean(R):9.4f}")
