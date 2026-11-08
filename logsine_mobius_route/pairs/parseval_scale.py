import numpy as np, math
from scipy.special import digamma
V=0.08494603839325915; g=0.5772156649015329
N=10**5
mu=np.ones(N+1,dtype=int); phi=np.arange(N+1); isp=np.ones(N+1,bool); isp[:2]=False
for p in range(2,N+1):
    if isp[p]:
        isp[2*p::p]=False; mu[p::p]*=-1; mu[p*p::p*p]=0; phi[p::p]-=phi[p::p]//p
# per q: s1=sum_{(a,q)=1} A(a/q), s2=sum A^2  (only squarefree q needed)
def sums(q):
    a=np.arange(1,q); a=a[np.gcd(a,q)==1]; t=a/q
    A=g+0.5*(digamma(t)+digamma(1-t)); return A.sum(),(A*A).sum()
qs=[q for q in range(2,N+1) if mu[q]!=0]
S={}
ylist=[60,200,1000,3000,10000,30000,100000]
for y in ylist:
    tot=0.0
    for q in qs:
        if q>y: break
        if q not in S: S[q]=sums(q)
        Y=y//q; j=np.arange(1,Y+1)
        T=np.sum(np.log(q*j)/j); H=np.sum(1.0/j)
        s1,s2=S[q]
        tot+=(phi[q]*T*T+2*T*H*s1+H*H*s2)/(float(q)*q*float(phi[q])**2)
    L=math.log(y)
    print(f"y={y:6d}  Var(F_y)={tot:12.4f}  V log^4y={V*L**4:12.4f}  ratio={tot/(V*L**4):.4f}  (Var-Vlog^4)/log^3={(tot-V*L**4)/L**3:.4f}")
