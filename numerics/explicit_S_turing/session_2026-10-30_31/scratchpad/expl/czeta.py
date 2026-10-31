# C_zeta = sum over prime powers n of sqrt(alpha_n^2+beta_n^2) (float estimate, n<=Nmax, plus crude tail estimate)
import numpy as np, math, sys
def primes_upto(N):
    s=np.ones(N+1,bool); s[:2]=False
    for i in range(2,int(N**0.5)+1):
        if s[i]: s[i*i::i]=False
    return np.nonzero(s)[0]
def czeta(d,cR,cI,Nmax=10**7):
    s1=0.5+d; s2=0.5+2*d
    P=primes_upto(Nmax); tot=0.0
    for p in P:
        lp=math.log(p); n=p; k=1
        while n<=Nmax:
            L=k*lp; ns1=n**(-s1); ns2=n**(-s2)
            A=-sum(c*lp*L**(j-1)/math.factorial(j-1) for j,c in cR.items())*ns1/math.pi
            Bv=((lp/L)*(ns2-2*ns1)-sum(c*lp*L**(j-1)/math.factorial(j-1) for j,c in cI.items())*ns1)/math.pi
            tot+=math.hypot(A,Bv); n*=p; k+=1
    return tot
if __name__=='__main__':
    pi=math.pi
    for name,(d,a1,a2,a3,a4) in {'BW(2.43)':(0.713,1.061,0.940,0.315,-0.300),'BW(2.44)':(0.722382,1.074223,0.925936,0.327241,-0.138682)}.items():
        cR={1:pi/4*d*a1,2:pi/4*d*d*a2}; cI={2:pi/4*a3,3:pi/4*d**3*a4}
        C1=cR[1]/(2*pi)
        for N in [10**5,10**6]:
            cz=czeta(d,cR,cI,N)
            print(name,'C1=%.5f'%C1,'N=%d Czeta=%.4f'%(N,cz),' const for |N-main| (T>=T_P): %.4f'%(cz+7/8-C1*math.log(2*pi)),flush=True)
