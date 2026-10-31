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
LB = 2000.0
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
print('g monotone on [%g, oo): crude bound %s < sigma1' % (LB, ratio.str(6)))
# On [L0, LB] no monotonicity is assumed: G(L) = sup_{L' >= L} g(L') is majorized by a non-increasing step function,
# the running maximum (from the right) of upper bounds of g on small boxes, started at g(LB) (g decreasing beyond LB).
def h_up(Lb):
    A0 = cpoly(pa, Lb)/PI; B0 = (((-dA*Lb).exp()-2)/Lb+cpoly(pb, Lb))/PI
    au = abs(A0).upper(); bu = abs(B0).upper()
    return (au*au+bu*bu).sqrt().upper()
edges = [float(L0.lower())-1e-9]
while edges[-1] < LB: edges.append(min(edges[-1]+max(0.003, 0.0002*edges[-1]), LB))
gup = []
for i in range(len(edges)-1):
    Lb = arb(edges[i]).union(arb(edges[i+1])); gup.append(h_up(Lb)*(-s1*arb(edges[i])).exp())
run = h(arb(LB))*(-s1*arb(LB)).exp(); G = [None]*len(gup)
for i in range(len(gup)-1, -1, -1):
    run = run if run > gup[i] else (gup[i] if gup[i] > run else run.union(gup[i]).upper()); G[i] = run.upper()
# int_{N0}^{oo} G(x) dx = sum_i G_i (e^{L_{i+1}} - e^{L_i}) + int_{LB}^{oo} g(x) dx
Istep = sum((G[i]*(arb(edges[i+1]).exp()-arb(edges[i]).exp()) for i in range(len(G))), arb(0))
L1 = arb(800)
def fz(z, an):
    A0 = sum((acb(pa[i])*z**i for i in range(len(pa))), acb(0))/PI
    B0 = (((-acb(dA)*z).exp()-2)/z+sum((acb(pb[i])*z**i for i in range(len(pb))), acb(0)))/PI
    return (A0*A0+B0*B0).sqrt(analytic=an)*((1-acb(s1))*z).exp()
I1 = Istep+acb.integral(fz, acb(LB), acb(L1)).real
def inc(k, X): return (-a*X).exp()*sum((arb(factorial(k))/factorial(i)*X**i/a**(k-i+1) for i in range(k+1)), arb(0))
I2 = (sum(((abs(pa[i])+abs(pb[i]))*inc(i, L1) for i in range(DEG+1)), arb(0))+3*inc(0, L1))/PI
gN0 = G[0]
tail = gN0*(arb('1.03883')*N0-psi)+arb('1.03883')*(I1+I2)
Cz = tot+tail
print('tail <=', tail.str(10), ' (integral', I1.str(10), ', far tail', I2.str(5), ')')
print('C_zeta <', Cz.upper().str(12, radius=False), '   time %.0fs' % (time.time()-t0))
json.dump({'Czeta_upper': Cz.upper().str(15, radius=False)}, open(sys.argv[1].replace('.json', '_cz.json'), 'w'))
