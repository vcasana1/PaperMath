# kappa = (6/pi^2)^2 int_1^inf E_G(y) log y / y^3 dy = (6/pi^2)^2 [ -Theta''(2)/2 - gamma Theta'(2) + gamma_1 a ],
# Theta(s) = -(2 pi/s) Fhat(s-1), Fhat(w) = (pi/w) cot(pi w/2) zeta(w) + A(w); derivatives at w=1 by symmetric differences
# (the removable singularity of cot*zeta at w=1 is avoided).  Also the full mu^2-corner measured.
import mpmath as mp, numpy as np, math
mp.mp.dps=30
def A(w): return (mp.log(mp.pi)-mp.euler-mp.digamma(1-w/2)+1/w+2*mp.nsum(lambda k:(mp.zeta(2*k)-1)/(2*k-w),[1,mp.inf]))/w
def Fhat(w): return mp.pi/w*mp.cot(mp.pi*w/2)*mp.zeta(w)+A(w)
F1=-mp.pi**2/2+A(1); h=mp.mpf('1e-6')
F1p=(Fhat(1+h)-Fhat(1-h))/(2*h); F1pp=(Fhat(1+h)-2*F1+Fhat(1-h))/h**2
# Theta(s) = -2 pi Fhat(s-1)/s : Theta(2)=-pi F1, Theta'(2) = -pi F1p + pi F1/2, Theta''(2) = -pi F1pp + pi F1p - pi F1/2
a=-mp.pi*F1; T1=-mp.pi*F1p+mp.pi*F1/2; T2=-mp.pi*F1pp+mp.pi*F1p-mp.pi*F1/2
I=-T2/2-mp.euler*T1+mp.stieltjes(1)*a
print("Fhat(1)=",mp.nstr(F1,12)," Fhat'(1)=",mp.nstr(F1p,12)," Fhat''(1)=",mp.nstr(F1pp,12))
print("Theta(2)=",mp.nstr(a,12)," Theta'(2)=",mp.nstr(T1,12)," Theta''(2)=",mp.nstr(T2,12))
print("int_1^inf E_G log y / y^3 =",mp.nstr(I,10),"  kappa=(6/pi^2)^2 I =",mp.nstr((6/mp.pi**2)**2*I,10))
exec(open('bilinear_W.py').read().split('print("c_G')[0])
# direct check of the integral with E_G computed from G (truncated at y=Ymax, tail bounded by rms E_G ~ y^{3/4})
from scipy.integrate import quad
f=lambda y: (Gs(y)-cG*y*y)*math.log(y)/y**3
Ymax=3000; val=sum(quad(f,n,n+1,limit=200)[0] for n in range(1,Ymax))
print(f"direct int_1^{Ymax} E_G log y / y^3 = {val:.6f}  (tail beyond {Ymax} ~ 2.8*Ymax^(-5/4) log Ymax = {2.8*Ymax**-1.25*math.log(Ymax):.1e} at most)")
for X in [30000.5,120000.5,380000.5]:
    U=int(math.sqrt(X)); sq=np.array([d for d in range(1,U+1) if mu[d]!=0]); S=0.0
    for d in sq:
        js=sq[(sq*d<=X)&(sq*d>U)]
        for j in js:
            Y=X/(d*j); S+=d*j*(Gs(Y)-cG*Y*Y)
    print(f"X={X}: full mu^2 corner / X^2 = {S/X**2:.6f}")
