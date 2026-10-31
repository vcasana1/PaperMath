import mpmath as mp, math
mp.mp.dps=30
def elem(T,d,cR,cI):
    T=mp.mpf(T); s1=mp.mpf(1)/2+d+1j*T; s2=mp.mpf(1)/2+2*d+1j*T
    def Ael(s): return mp.im(mp.log(s)+mp.log(s-1))-T/2*mp.log(mp.pi)+mp.im(mp.loggamma(s/2))
    base=(2*Ael(s1)-Ael(s2))/mp.pi-T/(2*mp.pi)*mp.log(T/(2*mp.pi*mp.e))
    def Del(j):
        if j==1: return 1/s1+1/(s1-1)-mp.log(mp.pi)/2+mp.psi(0,s1/2)/2
        return s1**(-j)+(s1-1)**(-j)+(-1)**(j-1)/mp.factorial(j-1)/2**j*mp.psi(j-1,s1/2)
    R=sum(c*mp.re(Del(j)) for j,c in cR.items()); I=sum(c*(-mp.im(Del(j))) for j,c in cI.items())
    return base+(R+I)/mp.pi, base-(R-I)/mp.pi
if __name__=='__main__':
    pi=math.pi
    for name,(d,a1,a2,a3,a4),Cz,bwc,A1 in [('BW(2.43)',(0.713,1.061,0.940,0.315,-0.300),4.3823,5.746,0.0946),('BW(2.44)',(0.722382,1.074223,0.925936,0.327241,-0.138682),3.7776,4.954,0.097)]:
        cR={1:pi/4*d*a1,2:pi/4*d*d*a2}; cI={2:pi/4*a3,3:pi/4*d**3*a4}
        worst=-9;wT=None
        for T in [1,1.2,1.5,2,2.5,3,4,5,7,10,14,20,30,50,100,1e3,1e4,1e6,1e9,1e15]:
            u,l=elem(T,d,cR,cI); B=max(u,-l)+Cz-A1*math.log(T)
            if B>worst: worst,wT=B,T
            if T in (1,2,5,14,100,1e6,1e15): print(name,'T=%g Elem_u=%.4f -Elem_l=%.4f  B-A1logT=%.4f'%(T,u,-l,B))
        print(name,' sup(B - A1 log T) ~ %.4f at T=%g   vs BW constant %.3f'%(worst,wT,bwc))
