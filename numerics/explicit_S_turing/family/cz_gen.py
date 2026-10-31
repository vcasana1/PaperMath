# Rigorous upper bound for C_zeta(c) = sum_n Lambda(n) n^(-sigma1) hypot(A0(log n), B0(log n)), any kernel basis
#   A0(L) = -(1/pi) sum_{(R,j)} c L^(j-1)/(j-1)!,   B0(L) = (1/pi)[ (e^(-dL)-2)/L - sum_{(I,j)} c L^(j-1)/(j-1)! ]
# Exact Arb sum over all prime powers n <= N0; tail n > N0 by partial summation with psi(x) < 1.03883 x
# (Rosser-Schoenfeld 1962, Thm 12) and certified monotonicity of g(x) = hypot(A0,B0)(log x) x^(-sigma1) on [N0, oo).
import sys, json, time, numpy as np
from fractions import Fraction as Fr
from math import factorial
from flint import arb, acb, ctx
ctx.prec = 256
def A(q): return arb(q.numerator)/arb(q.denominator) if isinstance(q, Fr) else arb(q)
sol = json.load(open(sys.argv[1])); N0 = int(float(sys.argv[2]))
d = Fr(sol['d']).limit_denominator(10**6); B = [tuple(b) for b in sol['B']]; c = [A(Fr(x)) for x in sol['c']]
PI = arb.pi(); dA = A(d); s1 = A(Fr(1, 2)+d); a = s1-1
# polynomial coefficients (in L) of pi*A0 and of the polynomial part of pi*B0
DEG = max(j for _, j in B)-1
pa = [arb(0)]*(DEG+1); pb = [arb(0)]*(DEG+1)
for (k, j), cc in zip(B, c):
    if k == 'R': pa[j-1] -= cc/factorial(j-1)
    else: pb[j-1] -= cc/factorial(j-1)
def poly(p, L): return sum((p[i]*L**i for i in range(len(p))), arb(0))
def h(L):
    A0 = poly(pa, L)/PI; B0 = (((-dA*L).exp()-2)/L+poly(pb, L))/PI
    return (A0*A0+B0*B0).sqrt()
t0 = time.time()
s = np.ones(N0+1, np.bool_); s[:2] = False
for i in range(2, int(N0**0.5)+1):
    if s[i]: s[i*i::i] = False
P = np.nonzero(s)[0]; del s
tot = arb(0); psi = arb(0)
for p in P.tolist():
    lp = arb(p).log(); n = p; k = 1
    while n <= N0:
        L = k*lp; tot += lp*h(L)*(-s1*L).exp(); psi += lp; n *= p; k += 1
print('primes', len(P), ' partial sum (n<=%d) =' % N0, tot.str(15), ' psi(N0) =', psi.str(15), ' %.0fs' % (time.time()-t0), flush=True)
L0 = arb(N0).log()
# monotonicity: d/dL log g = (A0 A0' + B0 B0')/h^2 - sigma1 < 0 on [L0, LB] (boxes), and for L >= LB by a crude ratio bound
def cpoly(p, Lb):   # centred form: p(m) + p'(Lb)(Lb - m)
    m = arb(Lb.mid()); dp = [p[i]*i for i in range(1, len(p))]
    return poly(p, m)+poly(dp, Lb)*(Lb-m)
def dlogg_upper(Lb):
    dpa = [pa[i]*i for i in range(1, len(pa))]; dpb = [pb[i]*i for i in range(1, len(pb))]
    e = (-dA*Lb).exp()
    A0 = cpoly(pa, Lb)/PI; B0 = ((e-2)/Lb+cpoly(pb, Lb))/PI
    A1_ = cpoly(dpa, Lb)/PI; B1_ = (-(e-2)/(Lb*Lb)-dA*e/Lb+cpoly(dpb, Lb))/PI
    return (A0*A1_+B0*B1_)/(A0*A0+B0*B0)-s1
LB = 2000.0; x = float(L0.upper()); nbox = 0
while x < LB:
    y = min(x*1.002+0.01, LB); v = dlogg_upper(arb(x).union(arb(y))); nbox += 1
    if not (v < 0):    # refine the box
        z = x
        while z < y:
            w = min(z+(y-x)/64, y); vv = dlogg_upper(arb(z).union(arb(w))); nbox += 1
            assert vv < 0, ('monotonicity fails near L=', z, vv)
            z = w
    x = y
# L >= LB: (log h)' <= (|A0'|+|B0'|)/h and h >= |P| for the one of A0, B0 of larger degree D.
# In u = 1/L in [0, 1/LB]: num/L^D and low/L^D are polynomials in u, evaluated on the u-ball.
DA = max([i for i in range(DEG+1) if pa[i] != 0], default=-1); DB = max([i for i in range(DEG+1) if pb[i] != 0], default=-1)
q = [abs(pa[i])+abs(pb[i]) for i in range(DEG+1)]
if DA >= DB: D, pp, extra = DA, pa, 0
else: D, pp, extra = DB, pb, 2
u = arb(0).union(1/arb(LB))
num = u*sum((i*q[i]*u**(D-i) for i in range(1, DEG+1)), arb(0))+2*u**(D+2)+dA*u**(D+1)
if DEG > D: raise SystemExit('degree bookkeeping')
low = abs(pp[D])-sum((abs(pp[i])*u**(D-i) for i in range(D)), arb(0))-extra*u**(D+1)
ratio = num/low
assert low > 0 and ratio < s1, ('crude ratio fails', ratio)
print('monotone: %d boxes on [log N0, %g], crude bound beyond: %s < sigma1' % (nbox, LB, ratio.str(6)))
# integral of g over [N0, oo) = int_{L0}^{oo} h(L) e^{(1-sigma1)L} dL
L1 = arb(800)
def fz(z, an):
    A0 = sum((acb(pa[i])*z**i for i in range(len(pa))), acb(0))/PI
    B0 = (((-acb(dA)*z).exp()-2)/z+sum((acb(pb[i])*z**i for i in range(len(pb))), acb(0)))/PI
    return (A0*A0+B0*B0).sqrt(analytic=an)*((1-acb(s1))*z).exp()
I1 = acb.integral(fz, acb(L0), acb(L1)).real
def inc(k, X): return (-a*X).exp()*sum((arb(factorial(k))/factorial(i)*X**i/a**(k-i+1) for i in range(k+1)), arb(0))
I2 = (sum(((abs(pa[i])+abs(pb[i]))*inc(i, L1) for i in range(DEG+1)), arb(0))+3*inc(0, L1))/PI
gN0 = h(L0)*(-s1*L0).exp()
tail = gN0*(arb('1.03883')*N0-psi)+arb('1.03883')*(I1+I2)
Cz = tot+tail
print('tail <=', tail.str(10), ' (integral', I1.str(10), ', far tail', I2.str(5), ')')
print('C_zeta <', Cz.upper().str(12, radius=False), '   time %.0fs' % (time.time()-t0))
json.dump({'Czeta_upper': Cz.upper().str(15, radius=False)}, open(sys.argv[1].replace('.json', '_cz.json'), 'w'))
