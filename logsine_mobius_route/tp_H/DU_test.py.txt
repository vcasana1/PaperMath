# Test of |D_U(n)| << U^eps / sqrt(n), 1 <= n < U^2, where D_U(n) = sum_{d,j<=U, dj>n} mu(d)mu(j)/(dj) = m(U)^2 - B_U(n).
import numpy as np, math
def mobius(N):
    mu=np.ones(N+1,dtype=np.int64); isp=np.ones(N+1,bool); isp[:2]=False
    for p in range(2,N+1):
        if isp[p]: isp[2*p::p]=False; mu[p::p]*=-1; mu[p*p::p*p]=0
    mu[0]=0; return mu
for U in [100,300,1000,2000]:
    mu=mobius(U); N=U*U
    c=np.zeros(N+1)
    sq=np.array([d for d in range(1,U+1) if mu[d]!=0])
    for d in sq: np.add.at(c, d*sq, mu[d]*mu[sq]/(d*sq.astype(float)))
    D=np.cumsum(c[::-1])[::-1]          # D[k] = sum_{m>=k} c(m)
    n=np.arange(1,N); Dn=D[n+1]           # sum over m>n
    r=np.abs(Dn)*np.sqrt(n)
    m=np.sum(mu[1:]/np.arange(1,U+1))
    i=np.argmax(r)
    print(f"U={U}: m(U)={m:+.3e}  max_n sqrt(n)|D_U(n)| = {r.max():.3f} at n={n[i]} (n/U={n[i]/U:.2f})   at n=U: {r[U-1]:.3f}   "
          f"max over n<=U: {r[:U].max():.3f}   max over U<n<U^2: {r[U:].max():.3f}   median: {np.median(r):.3f}")
