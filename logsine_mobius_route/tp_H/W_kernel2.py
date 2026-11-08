import mpmath as mp, math
mp.mp.dps=20
def mu(n):
    r=1;k=2;m=n
    while k*k<=m:
        if m%k==0:
            m//=k
            if m%k==0: return 0
            r=-r
        k+=1
    return -r if m>1 else r
X=mp.mpf('37.4'); n=int(X)
W=sum(mu(d)*d*mp.clsin(2,2*mp.pi*X/d) for d in range(1,n+1))
M=[0]*(n+2); s=0
for k in range(1,n+1): s+=mu(k); M[k]=s
K=lambda u: mp.clsin(2,2*mp.pi*X/u)+(2*mp.pi*X/u)*mp.log(abs(2*mp.sin(mp.pi*X/u)))
brk=sorted(set([mp.mpf(1)]+[X/j for j in range(1,n+1) if X/j>=1]+[mp.mpf(k) for k in range(1,n+1)]+[X]))
tot=mp.mpf(0)
for a,b in zip(brk[:-1],brk[1:]):
    m=M[int(mp.floor(a+mp.mpf('1e-15')))]
    if m: tot+=m*mp.quad(K,[a,b])
print("W=",W,"  -int M K=",-tot)
