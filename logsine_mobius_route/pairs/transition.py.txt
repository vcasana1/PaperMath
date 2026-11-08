import numpy as np, math, sympy
E=0.6497531; z3=1.2020569031595942; L2=math.log(2)
ps=np.array(list(sympy.primerange(100000,200000)),dtype=np.float64)
ymax=100000
ygrid=np.array([10,30,100,300,1000,3000,10000,20000,30000,50000,70000,99999])
lam=np.zeros(ymax+1)
for p in sympy.primerange(2,ymax+1):
    q=p
    while q<=ymax: lam[q]=math.log(p)/(sympy.totient(q)); q*=p
cumlam=np.cumsum(lam)
acc=np.zeros(len(ygrid)); acc2=np.zeros(len(ygrid))
k=np.arange(2,ymax+1,dtype=np.float64)
for i in range(0,len(ps),200):
    blk=ps[i:i+200][:,None]
    w=np.log(np.abs(2*np.sin(np.pi*blk/k)))      # log|2 sin(pi p/k)|, k=2..ymax
    cs=np.cumsum(w,axis=1)
    v=cs[:,ygrid-2]
    acc+=v.sum(0); acc2+=(v**2).sum(0)
n=len(ps); m=acc/n; se=np.sqrt(acc2/n-m**2)/math.sqrt(n)
ip2=np.mean(ps**-2.0)
print("primes in [1e5,2e5]:",n)
print("   y    mean sum_{2<=k<=y} log|2sin|   +-se    sum Lambda/phi    cubic -z3 y^3 E[p^-2]/(2pi^2)   pred=Lam+cubic")
for j,y in enumerate(ygrid):
    cub=-z3*y**3*ip2/(2*math.pi**2)
    print(f"{y:6d} {m[j]:12.3f} {se[j]:7.3f} {cumlam[y]:10.3f} {cub:12.3f} {cumlam[y]+cub:12.3f}")
