# Huxley-Watt / U00605 with d=3:  mu = 3 mu_N - 3 mu_N*mu_N*1 + mu_N*mu_N*mu_N*1*1  on n <= N^3
# => W(X) = 3 T1 - 3 T2 + T3,  T1=sum_{n<=N} mu(n) n Cl2(2piX/n), T2=sum c2(n) n G1(X/n), T3=sum c3(n) n G2(X/n)
import numpy as np, math
exec(open('clausen_phi.py').read().split('print("Cl2 check')[0])
M=200000
mu=np.ones(M+1,dtype=np.int64); isp=np.ones(M+1,bool); isp[:2]=False
for p in range(2,M+1):
    if isp[p]: isp[2*p::p]=False; mu[p::p]*=-1; mu[p*p::p*p]=0
tau=np.zeros(M+1,dtype=np.int64)
for i in range(1,M+1): tau[i::i]+=1
def G(Y,w):
    L=np.arange(1,int(Y)+1); return np.sum(w[L]*L*Cl2(2*np.pi*np.mod(Y/L,1.0)))
one=np.ones(M+1,dtype=np.int64)
for X in [20000.5, 100000.5]:
    N=int(math.ceil(X**(1/3)))+1; n=int(X)
    muN=np.zeros(n+1,dtype=np.int64); muN[1:N+1]=mu[1:N+1]
    # Dirichlet convolutions up to n
    def conv(a,b):
        c=np.zeros(n+1,dtype=np.int64)
        for i in np.nonzero(a[1:])[0]+1:
            c[i::i][: (n//i)]+=a[i]*b[1:n//i+1]
        return c
    c2=conv(muN,muN); c3=conv(c2,muN)
    d=np.arange(1,n+1,dtype=float)
    W=np.sum(mu[1:n+1]*d*Cl2(2*np.pi*np.mod(X/d,1.0)))
    T1=np.sum(muN[1:n+1]*d*Cl2(2*np.pi*np.mod(X/d,1.0)))
    T2=sum(c2[k]*k*G(X/k,one) for k in np.nonzero(c2[1:])[0]+1)
    T3=sum(c3[k]*k*G(X/k,tau) for k in np.nonzero(c3[1:])[0]+1)
    s=X**1.5
    print(f"X={X} N={N}: W={W/s:+.4f}  3T1={3*T1/s:+.4f}  -3T2={-3*T2/s:+.2f}  T3={T3/s:+.2f}   check={3*T1-3*T2+T3-W:.2e}  [X^1.5]   X^2/X^1.5={X**0.5:.0f}")
