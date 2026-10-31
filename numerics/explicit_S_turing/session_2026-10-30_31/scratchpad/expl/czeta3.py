import numpy as np, math
from scipy.integrate import quad
from czeta2 import sieve, czeta
def tail_pnt(d,cR,cI,N):
    s1=0.5+d; s2=0.5+2*d
    def h(L):
        A0=-sum(c*L**(j-1)/math.factorial(j-1) for j,c in cR.items())/math.pi
        B0=((1/L)*(math.exp(-(s2-s1)*L)-2)-sum(c*L**(j-1)/math.factorial(j-1) for j,c in cI.items()))/math.pi
        return math.hypot(A0,B0)*math.exp((1-s1)*L)
    return quad(h,math.log(N),3000,limit=1000)[0]
if __name__=='__main__':
    pi=math.pi; P=sieve(10**8)
    for name,(d,a1,a2,a3,a4) in {'BW(2.43)':(0.713,1.061,0.940,0.315,-0.300),'BW(2.44)':(0.722382,1.074223,0.925936,0.327241,-0.138682)}.items():
        cR={1:pi/4*d*a1,2:pi/4*d*d*a2}; cI={2:pi/4*a3,3:pi/4*d**3*a4}; C1=cR[1]/(2*pi)
        for N in [10**7,10**8]:
            cz=czeta(d,cR,cI,P[P<=N],N)+tail_pnt(d,cR,cI,N)
            print(name,'N=%.0e Czeta~%.4f  K=7/8+Cz-C1 log2pi ~ %.4f   (BW const %s)'%(N,cz,7/8+cz-C1*math.log(2*pi),'5.746' if '43' in name else '4.954'),flush=True)
