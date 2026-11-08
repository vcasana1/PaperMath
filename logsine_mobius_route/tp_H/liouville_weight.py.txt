# Corner as a weighted Liouville sum: C(X) = sum_{U<n<=X} lambda(n) b_U(n) n E_G(X/n), b_U = |a_U| >= 0.
# Statistics of the weight b_U and of the contributions by value of b_U.  Also the unweighted indicator sum.
import numpy as np, math
exec(open('bilinear_W.py').read().split('print("c_G')[0])
for X in [30000.5, 120000.5, 380000.5]:
    U=int(math.sqrt(X)); NX=int(X)
    sq=np.array([d for d in range(1,U+1) if mu[d]!=0])
    aU=np.zeros(NX+2)
    for d in sq:
        js=sq[sq*d<=X]; np.add.at(aU, d*js, mu[d]*mu[js])
    n=np.arange(U+1,NX+1); a=aU[n]; b=np.abs(a); lam=np.sign(a)
    g=np.array([k*(Gs(X/k)-cG*(X/k)**2) for k in n])
    s=X**1.5; supp=b>0
    print(f"X={X}: C={np.sum(a*g)/s:+.4f}  #n in (U,X]={len(n)}  #supp={supp.sum()} ({supp.mean():.3f})  sum b={int(b.sum())}  mean b|supp={b[supp].mean():.2f}  max b={int(b.max())}")
    for k in range(1,int(b.max())+1):
        m=b==k
        if m.sum()==0: continue
        print(f"   b_U={k}: #n={m.sum():6d}  sum lam n E_G={np.sum(lam[m]*g[m])/s:+.4f}  sum|.|={np.sum(np.abs(g[m]))/s:.2f}  weighted contribution={k*np.sum(lam[m]*g[m])/s:+.4f} [X^1.5]")
    print(f"   indicator sum  sum_{{b>0}} lam n E_G = {np.sum(lam[supp]*g[supp])/s:+.4f};   plain Liouville sum_{{U<n<=X}} lambda(n) n E_G(X/n) needs lambda: ", end="")
    # full lambda via sieve
    L=np.ones(NX+1,dtype=np.int64)
    for p in range(2,NX+1):
        if L[p]==1 and all(p%q for q in range(2,int(p**0.5)+1)) if p<4 else None: pass
    # simple Omega sieve
    Om=np.zeros(NX+1,dtype=np.int64); isp=np.ones(NX+1,bool); isp[:2]=False
    for p in range(2,NX+1):
        if isp[p]:
            isp[2*p::p]=False; q=p
            while q<=NX: Om[q::q]+=1; q*=p
    lamfull=(-1)**Om
    print(f"{np.sum(lamfull[n]*g)/s:+.4f}  (sum|g| over all n = {np.sum(np.abs(g))/s:.2f}) [X^1.5]")
