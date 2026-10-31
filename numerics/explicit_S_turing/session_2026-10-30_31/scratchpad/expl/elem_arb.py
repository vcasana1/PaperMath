# Rigorous sup over T>=1 of F_u(T)=Elem_u(T)-A1 log T and F_l(T)=-Elem_l(T)-A1 log T (elementary part, no zeta).
import sys, json
from fractions import Fraction as Fr
from flint import arb, acb, ctx
ctx.prec=256
def A(q): return arb(q.numerator)/arb(q.denominator) if isinstance(q,Fr) else arb(q)
sol=json.load(open(sys.argv[1])); A1=A(Fr(sys.argv[2])); T0=int(sys.argv[3]) if len(sys.argv)>3 else 10**4
d=Fr(sol['d']).limit_denominator(10**6); c={tuple(b):A(Fr(x)) for b,x in zip(sol['B'],sol['c'])}
cR1,cR2,cI2,cI3=c[('R',1)],c[('R',2)],c[('I',2)],c[('I',3)]
PI=arb.pi(); s1r=A(Fr(1,2)+d); s2r=A(Fr(1,2)+2*d); C1=cR1/(2*PI); LOGPI=PI.log()
def psi(k,z): return z.polygamma(k) if k>0 else z.polygamma(0)
def pieces(T, ball=None):
    """values at T (arb point); if ball=(Tm,delta) return derivative enclosure over ball."""
    s1=acb(s1r,T); s2=acb(s2r,T); z1=s1/2; z2=s2/2
    Ael=lambda s: (s.log().imag+(s-1).log().imag)-T/2*LOGPI+(s/2).lgamma().imag
    base=(2*Ael(s1)-Ael(s2))/PI-T/(2*PI)*(T/(2*PI*arb(1).exp())).log()
    D1=1/s1+1/(s1-1)-LOGPI/2+psi(0,z1)/2
    D2=s1**-2+(s1-1)**-2-psi(1,z1)/4
    D3=s1**-3+(s1-1)**-3+psi(2,z1)/16
    R=cR1*D1.real+cR2*D2.real; I=cI2*(-D2.imag)+cI3*(-D3.imag)
    return base+(R+I)/PI-A1*T.log(), -(base-(R-I)/PI)-A1*T.log()
def derivs(Tb):
    # derivative enclosure over ball Tb; psi^(k) over ball via mean value: psi_k(mid)+psi_{k+1}(ball)*(z-zmid)
    Tm=arb(Tb.mid()); rad=Tb-Tm
    s1=acb(s1r,Tb); s2=acb(s2r,Tb); z1=s1/2; z2=s2/2
    def P(k,zb,sr):
        zm=acb(sr,Tm)/2; return psi(k,zm)+psi(k+1,zb)*acb(0,rad/2)
    dA=lambda s,zb,sr: ( (1/s).real+(1/(s-1)).real )-LOGPI/2+P(0,zb,sr).real/2
    dbase=(2*dA(s1,z1,s1r)-dA(s2,z2,s2r))/PI-(Tb/(2*PI)).log()/(2*PI)
    I_=acb(0,1)
    dD1=I_*(-s1**-2-(s1-1)**-2+P(1,z1,s1r)/4)
    dD2=I_*(-2*s1**-3-2*(s1-1)**-3-P(2,z1,s1r)/8)
    dD3=I_*(-3*s1**-4-3*(s1-1)**-4+P(3,z1,s1r)/32)
    R=cR1*dD1.real+cR2*dD2.real; I=cI2*(-dD2.imag)+cI3*(-dD3.imag)
    return dbase+(R+I)/PI-A1/Tb, -(dbase-(R-I)/PI)-A1/Tb
# certified sup on [1,T0]: geometric intervals, centered form
ratio=Fr(1001,1000); a=Fr(1); supu=arb(-100); supl=arb(-100); n=0
while a<T0:
    b=min(a*ratio,Fr(T0)); m=(a+b)/2; dl=(b-a)/2
    fu,fl=pieces(A(m)); gu,gl=derivs(A(a).union(A(b)))
    eu=fu+gu*A(dl)*arb(0,1); el=fl+gl*A(dl)*arb(0,1)
    supu=supu.union(eu) if n else eu; supl=supl.union(el) if n else el
    if n==0: print('T=1: F_u in',eu.str(8),' F_l in',el.str(8))
    a=b; n+=1
print('intervals',n,' sup F_u on [1,T0] <=',supu.upper().str(10,radius=False),'  sup F_l <=',supl.upper().str(10,radius=False))
# analytic bound for T>=T0
T=A(Fr(T0)); s1=s1r; s2=s2r
Ku=(2*s2-1)/PI + (s1*s1/2+(s2-1)*s2/2+1)/PI \
   + abs(cR1)/PI*((2*s1-1)+s1*s1/4+arb(8)/3)/T \
   + (abs(cR2)+abs(cI2))/PI*(2/T+(2+2/T+arb(128)/(3*T*T))/4) \
   + abs(cI3)/PI*(2/(T*T)+(4/T+8/(T*T)+512/T**3)/16)
Finf_u=arb(7)/8-C1*(2*PI).log(); Finf_l=-arb(7)/8-C1*(2*PI).log()
tailu=Finf_u+Ku/T; taill=Finf_l+Ku/T
print('T>=T0: F_u <=',tailu.upper().str(10,radius=False),' F_l <=',taill.upper().str(10,radius=False),' (K_u=',Ku.str(6),')')
S=max(supu.upper(),tailu.upper(),supl.upper(),taill.upper())
print('SUP over T>=1 of max(F_u,F_l) <=',S.str(10,radius=False))
