import numpy as np, math
from scipy.special import gammaincc, gamma as G
def sieve(N):
    s=np.ones(N+1,np.bool_); s[:2]=False
    for i in range(2,int(N**0.5)+1):
        if s[i]: s[i*i::i]=False
    return np.nonzero(s)[0].astype(np.float64)
def terms(d,cR,cI,n,lp,L):
    s1=0.5+d; s2=0.5+2*d; ns1=np.exp(-s1*L); ns2=np.exp(-s2*L)
    A=-sum(c*L**(j-1)/math.factorial(j-1) for j,c in cR.items())*lp*ns1/math.pi
    B=((lp/L)*(ns2-2*ns1)-sum(c*L**(j-1)/math.factorial(j-1) for j,c in cI.items())*lp*ns1)/math.pi
    return np.hypot(A,B)
def czeta(d,cR,cI,P,N):
    lp=np.log(P); tot=terms(d,cR,cI,P,lp,lp).sum(); k=2
    while True:
        m=P[P**k<=N]
        if len(m)==0: break
        tot+=terms(d,cR,cI,m**k,np.log(m),k*np.log(m)).sum(); k+=1
    return tot
def tail_est(d,cR,cI,N):
    # heuristic tail with psi(x)=x: int_N^inf |coeffs| ... using |A|+|B| majorant
    s1=0.5+d; a=s1-1; X=math.log(N); tot=0
    for j,c in list(cR.items())+list(cI.items()):
        k=j-1; tot+=abs(c)/math.pi/math.factorial(k)*gammaincc(k+1,a*X)*G(k+1)/a**(k+1)
    tot+=2/math.pi*gammaincc(1e-9+0,a*X) if False else 0
    # Im log zeta part ~ (2/pi) sum Lambda/L n^-s1 ~ (2/pi) int x^-s1/log x dx : small, add crude E1
    from scipy.special import exp1
    tot+=2/math.pi*exp1(a*X)
    return tot
if __name__=='__main__':
    pi=math.pi; P=sieve(10**8)
    for name,(d,a1,a2,a3,a4) in {'BW(2.43)':(0.713,1.061,0.940,0.315,-0.300),'BW(2.44)':(0.722382,1.074223,0.925936,0.327241,-0.138682)}.items():
        cR={1:pi/4*d*a1,2:pi/4*d*d*a2}; cI={2:pi/4*a3,3:pi/4*d**3*a4}
        for N in [10**6,10**7,10**8]:
            Pn=P[P<=N]; cz=czeta(d,cR,cI,Pn,N); te=tail_est(d,cR,cI,N)
            print(name,'N=%.0e partial=%.4f tail~%.4f total~%.4f'%(N,cz,te,cz+te),flush=True)
