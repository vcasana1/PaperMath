# residues of What(s) = -(2pi/s) Fhat(s-1)/zeta(s-1) at s=1+rho (simple zeros): r = -(2pi/(1+rho)) A(rho)/zeta'(rho)
import mpmath as mp
mp.mp.dps=20
def A(s): return (mp.log(mp.pi)-mp.euler-mp.digamma(1-s/2)+1/s+2*mp.nsum(lambda k:(mp.zeta(2*k)-1)/(2*k-s),[1,mp.inf]))/s
rs=[]
for j in range(1,11):
    r=mp.zetazero(j); res=-2*mp.pi*A(r)/((1+r)*mp.diff(mp.zeta,r))
    rs.append(abs(res)); print(j, mp.nstr(r.imag,10), " |A|=",mp.nstr(abs(A(r)),6)," |zeta'|=",mp.nstr(abs(mp.diff(mp.zeta,r)),6)," |res|=",mp.nstr(abs(res),6))
print("max single-zero Omega constant:",mp.nstr(max(rs),6))
