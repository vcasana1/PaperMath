# Rigorous sup over T >= 1 of F_u(T) = Elem_u(T) - A1 log T and F_l(T) = -Elem_l(T) - A1 log T, any kernel basis.
# Elem_u = (1/pi)(2 Ael(s1) - Ael(s2)) - main(T) + (1/pi) sum_i c_i Phi_i(D_j(s1)),  Elem_l: same with -(sum c_R Phi_R - sum c_I Phi_I),
# Ael(s) = arg s + arg(s-1) - (T/2) log pi + Im log Gamma(s/2),  D_1 = 1/s+1/(s-1)-(1/2)log pi+(1/2)psi(s/2),
# D_j = s^-j + (s-1)^-j + ((-1)^(j-1)/(j-1)!) 2^-j psi^(j-1)(s/2)  (j >= 2);  Phi_R = Re, Phi_I = -Im.
# [1, T0]: centred form on geometric intervals; T >= T0: Stirling with Olver's remainder |R_1(z)| <= sec^2(ph z/2)/(12|z|)
# (DLMF 5.11(ii)) and Cauchy estimates |R_1^(k)(z)| <= k! (2/(3|z|)) (2/|z|)^k on the circle |w-z| = |z|/2.
import sys, json
from fractions import Fraction as Fr
from math import factorial
from flint import arb, acb, ctx
ctx.prec = 256
def A(q): return arb(q.numerator)/arb(q.denominator) if isinstance(q, Fr) else arb(q)
sol = json.load(open(sys.argv[1])); A1 = A(Fr(sys.argv[2])); T0 = int(sys.argv[3]) if len(sys.argv) > 3 else 10**4
MODE = sys.argv[4] if len(sys.argv) > 4 else 'N'   # 'N': |N - main|;  'S': |S(T)| = |N - theta/pi - 1|
d = Fr(sol['d']).limit_denominator(10**6); B = [tuple(b) for b in sol['B']]; c = [A(Fr(x)) for x in sol['c']]
J = max(j for _, j in B)
PI = arb.pi(); s1r = A(Fr(1, 2)+d); s2r = A(Fr(1, 2)+2*d); LOGPI = PI.log()
cR1 = c[B.index(('R', 1))]; C1 = cR1/(2*PI)
assert A1 >= C1
def psi(k, z): return z.polygamma(k)
def Dj(j, s, ps):   # ps[k] = psi^(k)(s/2)
    if j == 1: return 1/s+1/(s-1)-LOGPI/2+ps[0]/2
    return s**(-j)+(s-1)**(-j)+arb((-1)**(j-1))/factorial(j-1)/2**j*ps[j-1]
def dDj(j, s, ps):  # d/ds D_j
    if j == 1: return -s**-2-(s-1)**-2+ps[1]/4
    return -j*s**(-j-1)-j*(s-1)**(-j-1)+arb((-1)**(j-1))/factorial(j-1)/2**(j+1)*ps[j]
def combine(vals):
    R = sum((cc*vals[i].real for i, ((k, j), cc) in enumerate(zip(B, c)) if k == 'R'), arb(0))
    I = sum((cc*(-vals[i].imag) for i, ((k, j), cc) in enumerate(zip(B, c)) if k == 'I'), arb(0))
    return R, I
def F_at(T):
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
    Tm = arb(Tb.mid()); rad = Tb-Tm
    def P(k, sr):   # psi^(k) over the ball, mean value form
        zm = acb(sr, Tm)/2; zb = acb(sr, Tb)/2
        return psi(k, zm)+psi(k+1, zb)*acb(0, rad/2)
    s1 = acb(s1r, Tb); s2 = acb(s2r, Tb)
    dA = lambda s, sr: ((1/s).real+(1/(s-1)).real)-LOGPI/2+P(0, sr).real/2
    dbase = (2*dA(s1, s1r)-dA(s2, s2r))/PI-(Tb/(2*PI)).log()/(2*PI)
    if MODE == 'S':   # d/dT [main - theta/pi] = (1/2pi) log(T/2pi) - (1/(2pi)) Re psi(1/4+iT/2) + (1/(2pi)) log pi
        zm = acb(arb(1)/4, Tm/2); zb = acb(arb(1)/4, Tb/2)
        P0 = psi(0, zm)+psi(1, zb)*acb(0, rad/2)
        dbase = dbase+(Tb/(2*PI)).log()/(2*PI)-(P0.real-LOGPI)/(2*PI)
    ps = [P(k, s1r) for k in range(J+1)]
    R, I = combine([acb(0, 1)*dDj(j, s1, ps) for (_, j) in B])
    return dbase+(R+I)/PI-A1/Tb, -(dbase-(R-I)/PI)-A1/Tb
ratio = Fr(1001, 1000); a = Fr(1); n = 0
while a < T0:
    b = min(a*ratio, Fr(T0)); m = (a+b)/2; dl = (b-a)/2
    fu, fl = F_at(A(m)); gu, gl = dF_ball(A(a).union(A(b)))
    eu = fu+gu*A(dl)*arb(0, 1); el = fl+gl*A(dl)*arb(0, 1)
    supu = eu if n == 0 else supu.union(eu); supl = el if n == 0 else supl.union(el)
    a = b; n += 1
print('intervals', n, ' sup F_u on [1,T0] <=', supu.upper().str(10, radius=False), '  sup F_l <=', supl.upper().str(10, radius=False))
# T >= T0: F_u <= 7/8 - C1 log(2 pi) + K/T, F_l <= -7/8 - C1 log(2 pi) + K/T  (A1 >= C1)
T = A(Fr(T0)); s1 = s1r; s2 = s2r
K = (2*s2-1)/PI+(s1*s1/2+(s2-1)*s2/2+1)/PI+(2*s2*s2/4+(s1-1)*s1)/PI      # arg and Gamma parts (both signs)
K += abs(cR1)/PI*((2*s1-1)+s1*s1/4+arb(8)/3)/T                           # j = 1 corrections (O(1/T^2))
for (k, j), cc in zip(B, c):
    if j == 1: continue
    # |D_j| <= 2/T^j + (1/((j-1)! 2^j)) |psi^(j-1)(z)|,  |psi^(k)(z)| <= (k-1)!(2/T)^k + k!(2/T)^(k+1)/2 + (k+1)!(4/(3T))(4/T)^(k+1)
    kk = j-1
    ps = arb(factorial(kk-1))*(2/T)**kk+arb(factorial(kk))*(2/T)**(kk+1)/2+arb(factorial(kk+1))*(4/(3*T))*(4/T)**(kk+1)
    Dbound = 2/T**j+ps/(factorial(j-1)*2**j)
    K += abs(cc)/PI*Dbound*T      # Dbound <= const/T, so Dbound*T is the coefficient of 1/T
Finf_u = arb(7)/8-C1*(2*PI).log(); Finf_l = -arb(7)/8-C1*(2*PI).log()
if MODE == 'S':   # theta/pi + 1 - main = 7/8 + varpi/pi, |varpi(T)| <= (1/16+1/8+1/3)/T (Stirling, Olver's bound)
    Finf_u = -C1*(2*PI).log(); Finf_l = -C1*(2*PI).log(); K = K+(arb(1)/16+arb(1)/8+arb(1)/3)/PI
tu = Finf_u+K/T; tl = Finf_l+K/T
S = max(supu.upper(), supl.upper(), tu.upper(), tl.upper())
print('T>=T0: F_u <=', tu.upper().str(10, radius=False), ' F_l <=', tl.upper().str(10, radius=False), ' (K=', K.str(6), ')')
print('SUP over T>=1 of max(F_u,F_l) <=', S.str(12, radius=False))
json.dump({'A1': sys.argv[2], 'mode': MODE, 'Fsup_upper': S.str(15, radius=False)}, open(sys.argv[1].replace('.json', '_elem%s.json' % ('' if MODE == 'N' else 'S')), 'w'))
