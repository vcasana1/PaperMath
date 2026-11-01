# Rigorous upper bound (Arb ball arithmetic, 256 bits) for the Euler-product constant of a kernel,
#   C_zeta = sum_{p <= P0} M_p + sum_{n = p^k, p > P0} Lambda(n) n^(-sigma1) h(log n) + tail,
# with h(L) = sqrt(a(L)^2 + b(L)^2),  a(L) = -(1/pi) sum_{(R,j)} c_{R,j} L^(j-1)/(j-1)!,
# b(L) = (1/pi) [ (e^(-dL) - 2)/L - sum_{(I,j)} c_{I,j} L^(j-1)/(j-1)! ],  and M_p the maximum over the phase x of
#   f_p(x) = sum_{k: p^k <= N0} (log p) p^(-k sigma1) [ a(k log p) cos(kx) + b(k log p) sin(kx) ]
# (per-prime phase maximum, Lemma "The contribution of one prime"), bounded by the maximum on a grid of M points plus a
# Lipschitz correction.  The sum over the prime powers n <= N0 is exact; the tail n > N0 uses Lemma "The tail" with the
# non-increasing step majorant G of g(x) = h(log x) x^(-sigma1) on [N0, e^LB], the certified monotonicity of g beyond e^LB
# (Lemma "Monotonicity of g") and psi(x) < 1.03883 x (Rosser-Schoenfeld 1962, Thm 12).
#
# Usage:  python3 cz_gen_pp.py <solution.json> <N0> [P0]      (the article uses N0 = 1e8, P0 = 1000)
# Output: <solution>_czpp.json with the upper bound 'Czeta_upper' (decimal rounded upwards).
import sys, os, json, time, numpy as np
from fractions import Fraction as Fr
from math import factorial
from flint import arb, acb
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'hybrid_asymptotic'))   # certutil.py lives there (or next to this file in the flat archive)
from certutil import A, up_str

sol = json.load(open(sys.argv[1])); N0 = int(float(sys.argv[2])); P0 = int(sys.argv[3]) if len(sys.argv) > 3 else 1000
d = Fr(sol['d']).limit_denominator(10**6); B = [tuple(b) for b in sol['B']]; c = [A(Fr(x)) for x in sol['c']]
assert len(c) == len(B) and B[0] == ('R', 1) and ('I', 1) not in B and d > Fr(1, 2) and P0 <= N0
PI = arb.pi(); dA = A(d); s1 = A(Fr(1, 2)+d); alpha = s1-1                 # alpha = sigma1 - 1 > 0
# polynomial coefficients (in L) of pi*a and of the polynomial part of pi*b
DEG = max(j for _, j in B)-1
pa = [arb(0)]*(DEG+1); pb = [arb(0)]*(DEG+1)
for (k, j), cc in zip(B, c):
    if k == 'R': pa[j-1] -= cc/factorial(j-1)
    else: pb[j-1] -= cc/factorial(j-1)
def poly(p, L): return sum((p[i]*L**i for i in range(len(p))), arb(0))
def h(L):
    a0 = poly(pa, L)/PI; b0 = (((-dA*L).exp()-2)/L+poly(pb, L))/PI
    return (a0*a0+b0*b0).sqrt()

t0 = time.time()
# primes up to N0 (sieve of Eratosthenes)
s = np.ones(N0+1, np.bool_); s[:2] = False
for i in range(2, int(N0**0.5)+1):
    if s[i]: s[i*i::i] = False
P = np.nonzero(s)[0]; del s
# exact sum over the prime powers n <= N0, with the per-prime phase maximum for p <= P0
M = 4096
xs = [2*PI*i/M for i in range(M)]; hx = PI/M                              # grid points and half-spacing
tot = arb(0); psi = arb(0); gain = arb(0)
for p in P.tolist():
    lp = arb(p).log(); n = p; k = 1; coef = []; hyp = arb(0)
    while n <= N0:
        L = k*lp; w = lp*(-s1*L).exp(); a0 = poly(pa, L)/PI; b0 = (((-dA*L).exp()-2)/L+poly(pb, L))/PI
        coef.append((k, w*a0, w*b0)); hyp += w*(a0*a0+b0*b0).sqrt(); psi += lp; n *= p; k += 1
    if p <= P0:
        # max_x f_p(x) <= max_i f_p(x_i) + hx * sum_k k |(a_k, b_k)|   (Lipschitz constant of f_p)
        Lip = sum((kk*(a*a+b*b).sqrt() for kk, a, b in coef), arb(0))
        best = None
        for x in xs:
            v = sum((a*(kk*x).cos()+b*(kk*x).sin() for kk, a, b in coef), arb(0))
            best = v.upper() if best is None or v.upper() > best else best
        mb = best+hx*Lip
        mb = mb if mb < hyp else hyp                                       # the trivial bound sum_k |(a_k,b_k)| is always valid
        gain += hyp-mb; tot += mb
    else:
        tot += hyp
print('per-prime phase maximum for p <=', P0, ': gain', gain.str(8), flush=True)
print('primes', len(P), ' partial sum (n<=%d) =' % N0, tot.str(15), ' psi(N0) =', psi.str(15), ' %.0fs' % (time.time()-t0), flush=True)

# monotonicity of g on [e^LB, oo) (Lemma "Monotonicity of g"): in u = 1/L in [0, 1/LB], num(u)/low(u) < sigma1 with
#   num(u) = u sum_{i>=1} i q_i u^(D-i) + 2 u^(D+2) + d u^(D+1),   low(u) = |p_D| - sum_{i<D} |p_i| u^(D-i) - eps_P u^(D+1),
# where P is the one of pi*a, pi*b of larger degree D (pi*a if equal), q_i = |a_i| + |b_i|, eps_P = 2 if P = pi*b else 0.
L0 = arb(N0).log()
DA = max([i for i in range(DEG+1) if pa[i] != 0], default=-1); DB = max([i for i in range(DEG+1) if pb[i] != 0], default=-1)
q = [abs(pa[i])+abs(pb[i]) for i in range(DEG+1)]
if DA >= DB: D, pp, extra = DA, pa, 0
else: D, pp, extra = DB, pb, 2
assert D == DEG, 'the top coefficient of the kernel vanishes'
LB = None
for LBc in [2000.0, 5000.0, 2e4, 1e5, 1e6, 1e7]:
    u = arb(0).union(1/arb(LBc))
    num = u*sum((i*q[i]*u**(D-i) for i in range(1, DEG+1)), arb(0))+2*u**(D+2)+dA*u**(D+1)
    low = abs(pp[D])-sum((abs(pp[i])*u**(D-i) for i in range(D)), arb(0))-extra*u**(D+1)
    if low > 0 and num/low < s1: LB = LBc; ratio = num/low; break
assert LB is not None, 'monotonicity of g could not be certified'
print('g monotone on [%g, oo): crude bound %s < sigma1' % (LB, ratio.str(6)))

# step majorant G >= g on [N0, e^LB]: on [e^u_i, e^u_{i+1}] the running maximum, from the right, of upper bounds of g on
# the small boxes, started at g(e^LB) (g is non-increasing beyond e^LB), so that G is non-increasing on [N0, oo)
def cpoly(p, Lb):   # centred form of a polynomial on a ball: p(m) + p'(Lb)(Lb - m)
    m = arb(Lb.mid()); dp = [p[i]*i for i in range(1, len(p))]
    return poly(p, m)+poly(dp, Lb)*(Lb-m)
def h_up(Lb):
    a0 = cpoly(pa, Lb)/PI; b0 = (((-dA*Lb).exp()-2)/Lb+cpoly(pb, Lb))/PI
    au = abs(a0).upper(); bu = abs(b0).upper()
    return (au*au+bu*bu).sqrt().upper()
edges = [float(L0.lower())-1e-9]
while edges[-1] < LB: edges.append(min(edges[-1]+max(0.003, 0.0002*edges[-1]), LB))
gup = []
for i in range(len(edges)-1):
    Lb = arb(edges[i]).union(arb(edges[i+1])); gup.append(h_up(Lb)*(-s1*arb(edges[i])).exp())
run = h(arb(LB))*(-s1*arb(LB)).exp(); G = [None]*len(gup)
for i in range(len(gup)-1, -1, -1):
    run = run if run > gup[i] else (gup[i] if gup[i] > run else run.union(gup[i]).upper()); G[i] = run.upper()
Istep = sum((G[i]*(arb(edges[i+1]).exp()-arb(edges[i]).exp()) for i in range(len(G))), arb(0))   # int_{N0}^{e^LB} G dx

# int_{e^LB}^oo g dx  <=  int_{e^LB}^{e^L1} g dx + int_{e^L1}^oo gtilde dx   with L1 = 800 and the majorant
#   gtilde = (1/pi) (sum_i q_i L^i + 3) e^(-sigma1 L) >= g on [e^L1, oo)   (from h <= |a| + |b| and 2/L <= 3);
# when LB > L1 the first integral is negative, and the inequality holds because gtilde >= g on [e^L1, e^LB] as well.
L1 = arb(800)
assert LB >= 800
def fz(z, analytic):
    a0 = sum((acb(pa[i])*z**i for i in range(len(pa))), acb(0))/PI
    b0 = (((-acb(dA)*z).exp()-2)/z+sum((acb(pb[i])*z**i for i in range(len(pb))), acb(0)))/PI
    return (a0*a0+b0*b0).sqrt(analytic=analytic)*((1-acb(s1))*z).exp()
Icancel = acb.integral(fz, acb(L1), acb(LB))                               # int_{L1}^{LB} h(L) e^{(1-sigma1) L} dL = int_{e^L1}^{e^LB} g dx
assert Icancel.is_finite() and Icancel.imag.contains(0)
def inc(k, X): return (-alpha*X).exp()*sum((arb(factorial(k))/factorial(i)*X**i/alpha**(k-i+1) for i in range(k+1)), arb(0))   # int_X^oo L^k e^{-alpha L} dL
Ifar = (sum((q[i]*inc(i, L1) for i in range(DEG+1)), arb(0))+3*inc(0, L1))/PI   # int_{e^L1}^oo gtilde dx
Itail = Istep-Icancel.real+Ifar                                            # >= int_{N0}^oo G dx
# Lemma "The tail": sum_{n > N0} Lambda(n) g(n) <= G(N0) (1.03883 N0 - psi(N0)) + 1.03883 int_{N0}^oo G dx
tail = G[0]*(arb('1.03883')*N0-psi)+arb('1.03883')*Itail
Cz = tot+tail
print('tail <=', tail.str(10), ' (int_{N0}^{e^LB} G =', Istep.str(10), ', int_{e^L1}^{e^LB} g =', Icancel.real.str(10), ', far tail <=', Ifar.str(5), ')')
print('C_zeta <', up_str(Cz, 12), '   time %.0fs' % (time.time()-t0))
json.dump({'Czeta_upper': up_str(Cz, 15), 'N0': N0, 'P0': P0}, open(sys.argv[1].replace('.json', '_czpp.json'), 'w'))
