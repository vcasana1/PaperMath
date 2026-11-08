import numpy as np, math, sympy
C=0.74379486183940054
N=20000
d=np.zeros(N+1,dtype=np.int64)
for i in range(1,N+1): d[i::i]+=1
nn=np.arange(1,N+1,dtype=np.float64); dd=d[1:]*nn**-0.75
ps=np.array(list(sympy.primerange(100000,100000+40000)))[::40]
E=[];S=[]
for p in ps:
    k=np.arange(2,p,dtype=np.float64)
    E.append(np.sum(np.log(np.abs(np.sin(np.pi*(p/k)))))+C*p)
    S.append(p**0.25*np.sum(dd*np.sin(4*np.pi*np.sqrt(nn*p)-np.pi/4)))
E=np.array(E);S=np.array(S);L=np.log(ps)
A=np.vstack([S,L,np.ones_like(S)]).T
coef=np.linalg.lstsq(A,E,rcond=None)[0]
print("primes",len(ps),"coef(S,log p,1)=",coef,"corr(E,S)=",np.corrcoef(E,S)[0,1])
print("rms(E)/p^{1/4}=",np.sqrt(np.mean(E**2))/np.mean(ps**0.25), " rms residual=",np.sqrt(np.mean((E-A@coef)**2)))
for p in [101,1009,10007,100003]:
    k=np.arange(2,p,dtype=np.float64); e=np.sum(np.log(np.abs(np.sin(np.pi*(p/k)))))+C*p
    s=p**0.25*np.sum(dd*np.sin(4*np.pi*np.sqrt(nn*p)-np.pi/4))/math.sqrt(2)
    print(p, round(e,3), round(s,3))
