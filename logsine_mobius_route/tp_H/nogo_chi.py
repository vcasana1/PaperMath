# Any PSD quadratic certificate in mu (squarefree support) also certifies every multiplicative +-1 pattern chi.
# chi == 1 gives W_1(X) = sum_{m<=X squarefree} m Cl_2(2 pi X/m) ~ c X^2. Also random chi.
import numpy as np, math
exec(open('clausen_phi.py').read().split('print("Cl2 check')[0])
N=200000
mu=np.ones(N+1,dtype=np.int64); isp=np.ones(N+1,bool); isp[:2]=False
for p in range(2,N+1):
    if isp[p]: isp[2*p::p]=False; mu[p::p]*=-1; mu[p*p::p*p]=0
sq=(mu!=0)
primes=np.nonzero(isp)[0]
# completely multiplicative chi on squarefree from random signs eps_p
def chi_vec(eps):
    c=np.ones(N+1,dtype=np.int64)
    for p,e in zip(primes,eps):
        if e<0: c[p::p]*=-1
    return c*sq
rng=np.random.default_rng(0)
for X in [1000.5, 10000.5, 100000.5]:
    n=int(X); m=np.arange(1,n+1,dtype=float); w=m*Cl2(2*np.pi*np.mod(X/m,1.0))
    W_mu=np.sum(mu[1:n+1]*w); W_1=np.sum(sq[1:n+1]*w)
    Wr=[np.sum(chi_vec(rng.choice([-1,1],size=len(primes)))[1:n+1]*w) for _ in range(5)]
    print(f"X={X}: W_mu/X^1.5={W_mu/X**1.5:.4f}   W_chi=1 /X^2={W_1/X**2:.4f}   random chi: max|W|/X^1.5={max(abs(np.array(Wr)))/X**1.5:.3f}")
print("--- chi = mu on all primes <= sqrt X, free signs on primes > sqrt X (at most one such prime divides m<=X) ---")
for X in [10000.5, 100000.5, 200000-0.5]:
    n=int(X); s=int(math.isqrt(n))
    mm=np.arange(1,n+1); w=np.zeros(n+1); w[1:]=mm*Cl2(2*np.pi*np.mod(X/mm,1.0))
    # largest prime factor > s ?
    big=np.zeros(n+1,dtype=np.int64)
    for p in primes[primes>s]:
        if p>n: break
        big[p::p]=p
    smooth_part=np.sum((mu[1:n+1]*w[1:])[big[1:n+1]==0])
    gain=0.0; Wmu_big=0.0
    for p in primes[(primes>s)&(primes<=n)]:
        r=np.arange(1,n//p+1); t=np.sum(mu[r]*w[p*r])   # mu(pr)=-mu(r)
        gain+=abs(t); Wmu_big+=-t
    Wmu=smooth_part+Wmu_big
    print(f"X={X}: W_mu/X^1.5={Wmu/X**1.5:.4f}   max_chi W_chi /X^1.5={(smooth_part+gain)/X**1.5:.2f}   (/X^2={(smooth_part+gain)/X**2:.4f})")
