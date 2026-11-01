# Rigorous upper bound (Arb ball arithmetic, 256 bits) for sup_{T >= 1} F_u(T) and sup_{T >= 1} F_l(T), where
#   F_u(T) = E_u(T) - A1 log T,   F_l(T) = -E_l(T) - A1 log T,
#   E_u(T) = (1/pi)(2 Ael(s1) - Ael(s2)) - main(T) + (1/pi) sum_iota c_iota Phi_iota(D_j(s1)),
#   E_l(T) = (1/pi)(2 Ael(s1) - Ael(s2)) - main(T) - (1/pi) [ sum_{(R,j)} c Re D_j(s1) - sum_{(I,j)} c (-Im D_j(s1)) ],
#   Ael(s) = arg s + arg(s-1) - (T/2) log pi + Im log Gamma(s/2),   main(T) = (T/2pi) log(T/(2 pi e)),
#   D_1(s) = 1/s + 1/(s-1) - (1/2) log pi + (1/2) psi(s/2),   D_j(s) = s^-j + (s-1)^-j + ((-1)^(j-1)/(j-1)!) 2^-j psi^(j-1)(s/2) (j >= 2),
#   s1 = 1/2 + d + iT,  s2 = 1/2 + 2d + iT,  Phi_R = Re,  Phi_I = -Im.
# Mode S replaces main(T) by theta(T)/pi + 1 (then the bounds are for |S(T)|).
# [1, T0]: centred form F(mid) + F'(box) * [-half-width, half-width] on geometric intervals of ratio 1001/1000;
# T >= T0: Lemma "The elementary part for large T": F_u <= 7/8 - C1 log(2 pi) + K/T, F_l <= -7/8 - C1 log(2 pi) + K/T
# (mode S: -C1 log(2 pi) + (K + (1/16 + 1/8 + 1/3)/pi)/T), with the constant K of that lemma; needs A1 >= C1 = c_R1/(2 pi).
#
# Usage:  python3 elem_gen.py <solution.json> <A1> [T0] [N|S]      (the article uses T0 = 10000)
# Output: <solution>_elem.json or <solution>_elemS.json with 'Fsup_upper' (decimal rounded upwards).
import sys, os, json, time
from fractions import Fraction as Fr
from math import factorial
from flint import arb, acb
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'hybrid_asymptotic'))   # certutil.py lives there (or next to this file in the flat archive)
from certutil import A, up_str, provenance

sol = json.load(open(sys.argv[1])); A1 = A(Fr(sys.argv[2])); T0 = int(sys.argv[3]) if len(sys.argv) > 3 else 10**4
MODE = sys.argv[4] if len(sys.argv) > 4 else 'N'
print(provenance(sys.argv[1], __file__, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'hybrid_asymptotic', 'certutil.py') if not os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certutil.py')) else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'certutil.py')), flush=True)
assert MODE in ('N', 'S') and T0 >= 1
d = Fr(sol['d']).limit_denominator(10**6); B = [tuple(b) for b in sol['B']]; c = [A(Fr(x)) for x in sol['c']]
assert len(c) == len(B) and B[0] == ('R', 1) and ('I', 1) not in B and d > Fr(1, 2)
J = max(j for _, j in B)
PI = arb.pi(); s1r = A(Fr(1, 2)+d); s2r = A(Fr(1, 2)+2*d); LOGPI = PI.log()
cR1 = c[0]; C1 = cR1/(2*PI)
assert A1 >= C1, 'A1 must be >= c_R1/(2 pi)'

def psi(k, z): return z.polygamma(k)
def Dj(j, s, ps):   # ps[k] = psi^(k)(s/2)
    if j == 1: return 1/s+1/(s-1)-LOGPI/2+ps[0]/2
    return s**(-j)+(s-1)**(-j)+arb((-1)**(j-1))/factorial(j-1)/2**j*ps[j-1]
def dDj(j, s, ps):  # d/ds D_j(s)
    if j == 1: return -s**-2-(s-1)**-2+ps[1]/4
    return -j*s**(-j-1)-j*(s-1)**(-j-1)+arb((-1)**(j-1))/factorial(j-1)/2**(j+1)*ps[j]
def combine(vals):  # sum_{(R,j)} c Re(.) and sum_{(I,j)} c (-Im(.))
    R = sum((cc*vals[i].real for i, ((k, j), cc) in enumerate(zip(B, c)) if k == 'R'), arb(0))
    I = sum((cc*(-vals[i].imag) for i, ((k, j), cc) in enumerate(zip(B, c)) if k == 'I'), arb(0))
    return R, I
def F_at(T):
    # (F_u(T), F_l(T)) at an exact T
    s1 = acb(s1r, T); s2 = acb(s2r, T)
    Ael = lambda s: (s.log().imag+(s-1).log().imag)-T/2*LOGPI+(s/2).lgamma().imag
    base = (2*Ael(s1)-Ael(s2))/PI-T/(2*PI)*(T/(2*PI*arb(1).exp())).log()
    if MODE == 'S':   # replace main(T) by theta(T)/pi + 1
        theta = acb(arb(1)/4, T/2).lgamma().imag-T/2*LOGPI
        base = base+T/(2*PI)*(T/(2*PI*arb(1).exp())).log()-theta/PI-1
    ps = [psi(k, s1/2) for k in range(J)]
    R, I = combine([Dj(j, s1, ps) for (_, j) in B])
    return base+(R+I)/PI-A1*T.log(), -(base-(R-I)/PI)-A1*T.log()
def dF_ball(Tb):
    # (F_u'(T), F_l'(T)) on a ball Tb of heights; the polygammas on the ball by the mean value form psi^(k)(z_m) + psi^(k+1)(z_ball) (z - z_m)
    Tm = arb(Tb.mid()); rad = Tb-Tm
    def P(k, sr):
        zm = acb(sr, Tm)/2; zb = acb(sr, Tb)/2
        return psi(k, zm)+psi(k+1, zb)*acb(0, rad/2)
    s1 = acb(s1r, Tb); s2 = acb(s2r, Tb)
    dAel = lambda s, sr: ((1/s).real+(1/(s-1)).real)-LOGPI/2+P(0, sr).real/2      # d/dT Ael(sr + iT)
    dbase = (2*dAel(s1, s1r)-dAel(s2, s2r))/PI-(Tb/(2*PI)).log()/(2*PI)
    if MODE == 'S':   # d/dT [main - theta/pi] = (1/2pi) log(T/2pi) - (1/2pi) Re psi(1/4+iT/2) + (1/2pi) log pi
        zm = acb(arb(1)/4, Tm/2); zb = acb(arb(1)/4, Tb/2)
        P0 = psi(0, zm)+psi(1, zb)*acb(0, rad/2)
        dbase = dbase+(Tb/(2*PI)).log()/(2*PI)-(P0.real-LOGPI)/(2*PI)
    ps = [P(k, s1r) for k in range(J+1)]
    R, I = combine([acb(0, 1)*dDj(j, s1, ps) for (_, j) in B])              # d/dT = i d/ds
    return dbase+(R+I)/PI-A1/Tb, -(dbase-(R-I)/PI)-A1/Tb

# [1, T0]
t0 = time.time(); ratio = Fr(1001, 1000); a = Fr(1); n = 0; supu = None; supl = None
while a < T0:
    b = min(a*ratio, Fr(T0)); m = (a+b)/2; dl = (b-a)/2
    fu, fl = F_at(A(m)); gu, gl = dF_ball(A(a).union(A(b)))
    eu = (fu+gu*A(dl)*arb(0, 1)).upper(); el = (fl+gl*A(dl)*arb(0, 1)).upper()
    supu = eu if supu is None or eu > supu else supu; supl = el if supl is None or el > supl else supl
    a = b; n += 1
print('intervals', n, ' sup F_u on [1,T0] <=', up_str(supu, 10), '  sup F_l <=', up_str(supl, 10))
# T >= T0 (Lemma "The elementary part for large T")
T = A(Fr(T0)); s1 = s1r; s2 = s2r
K = (2*s2-1)/PI+(s1*s1/2+(s2-1)*s2/2+1)/PI+(2*s2*s2/4+(s1-1)*s1)/PI        # arguments and Gamma factors
K += abs(cR1)/PI*((2*s1-1)+s1*s1/4+arb(8)/3)/T                             # j = 1: |delta_1| <= B/T^2 <= B/(T0 T)
for (k, j), cc in zip(B, c):
    if j == 1: continue
    # |D_j(s1)| <= 2/T^j + |psi^(j-1)(z1)| / ((j-1)! 2^j),  |psi^(k)(z1)| <= (k-1)! (2/T)^k + k! (2/T)^(k+1)/2 + (k+1)! (4/(3T)) (4/T)^(k+1);
    # T times the bound is non-increasing in T, so the bound at T0 times T0/T is valid for T >= T0
    kk = j-1
    ps = arb(factorial(kk-1))*(2/T)**kk+arb(factorial(kk))*(2/T)**(kk+1)/2+arb(factorial(kk+1))*(4/(3*T))*(4/T)**(kk+1)
    Dbound = 2/T**j+ps/(factorial(j-1)*2**j)
    K += abs(cc)/PI*Dbound*T
Finf_u = arb(7)/8-C1*(2*PI).log(); Finf_l = -arb(7)/8-C1*(2*PI).log()
if MODE == 'S':   # theta/pi + 1 - main = 7/8 + varpi/pi, |varpi(T)| <= (1/16 + 1/8 + 1/3)/T (Lemma "The theta function")
    Finf_u = -C1*(2*PI).log(); Finf_l = -C1*(2*PI).log(); K = K+(arb(1)/16+arb(1)/8+arb(1)/3)/PI
tu = (Finf_u+K/T).upper(); tl = (Finf_l+K/T).upper()
S = max(supu, supl, tu, tl)
print('T>=T0: F_u <=', up_str(tu, 10), ' F_l <=', up_str(tl, 10), ' (K =', K.str(6), ')')
print('SUP over T>=1 of max(F_u,F_l) <=', up_str(S, 12), '   time %.0fs' % (time.time()-t0))
json.dump({'A1': sys.argv[2], 'T0': T0, 'mode': MODE, 'Fsup_upper': up_str(S, 15)}, open(sys.argv[1].replace('.json', '_elem%s.json' % ('' if MODE == 'N' else 'S')), 'w'))
