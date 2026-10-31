# Certified evaluation of the constants of the article by Arb ball arithmetic (python-flint).
# Every quantity is a ball [mid +/- rad] that contains the exact value (outward rounding);
# every inequality used in the proofs is checked on the whole ball with assert.
# Closed forms: hinge formulas (5.9) for the angular integrals; zeta at real points by Arb.
# Independent check: the angular integrals are also computed by rigorous Arb integration
# (acb.integral) on the subintervals where the integrand is analytic.
import sys, math, flint
from flint import arb, acb, ctx
from fractions import Fraction as Fr

ctx.prec = 256                      # bits (about 77 decimal digits; 40 are printed)
DIG = 40                            # printed significant digits
print('Python', sys.version.split()[0], ' python-flint', flint.__version__, ' precision', ctx.prec, 'bits')

def A(q):                           # exact rational -> ball
    q = Fr(q); return arb(q.numerator) / q.denominator
def show(name, x):
    print(name, '=', x.str(DIG, radius=True))
def lt(x, y):  return bool(x < A(y))         # True only if the whole ball is < y
def gt(x, y):  return bool(x > A(y))
PI, LOG2, HALF = arb.pi(), arb(2).log(), A(Fr(1, 2))

def closed_form(nodes, c, R):
    """int_0^pi e*(c+R cos th) dth by the hinge formulas (5.9); nodes (sigma_i, e_i) exact rationals."""
    n = len(nodes) - 1
    xs = [a for a, _ in nodes]; es = [b for _, b in nodes]
    s = [(es[i+1]-es[i]) / (xs[i+1]-xs[i]) for i in range(n)]
    hinges = [(xs[i], s[i]-s[i-1]) for i in range(1, n)] + [(Fr(1), -s[n-1])]
    th_h = ((HALF - c) / R).acos()
    e0, s0 = A(es[0]), A(s[0])
    I = (e0 + s0*(c-HALF))*th_h + s0*R*th_h.sin()
    I += ((1+s0)*(HALF-c) + e0)*(PI-th_h) + (1+s0)*R*th_h.sin()
    for a, coef in hinges:
        a, coef = A(a), A(coef)
        th_a = ((a-c)/R).acos();   I += coef*((c-a)*th_a + R*th_a.sin())
        th_b = ((1-a-c)/R).acos(); I += coef*((1-c-a)*(PI-th_b) + R*th_b.sin())
    return I

def rigorous_integral(nodes, c, R):
    """int_0^pi e*(c+R cos th) dth by acb.integral, split at every angle where e* has a kink."""
    xs = [a for a, _ in nodes]; es = [b for _, b in nodes]
    kinks = set([Fr(0), Fr(1, 2), Fr(1)] + xs + [1 - a for a in xs])
    cuts = [arb(0), PI]
    for a in kinks:
        x = (A(a) - c) / R
        if x > -1 and x < 1: cuts.append(x.acos())
    cuts = sorted(cuts, key=lambda z: float(z.mid()))
    def piece(sig_mid):                      # the affine formula valid on the piece containing sig_mid
        if sig_mid >= 1: return (Fr(0), Fr(0))           # e* = 0
        if sig_mid < 0:  return (Fr(1, 2), Fr(-1))        # e* = 1/2 - sigma
        if sig_mid >= Fr(1, 2): x = sig_mid; sgn = 1
        else: x = 1 - sig_mid; sgn = -1
        for (a, ea), (b, eb) in zip(nodes, nodes[1:]):
            if a <= x <= b:
                sl = (eb - ea) / (b - a)
                if sgn == 1: return (ea - sl*a, sl)                    # e(sigma) = ea + sl (sigma - a)
                return (Fr(1, 2) + ea + sl*(1 - a), -1 - sl)           # 1/2 - sigma + e(1 - sigma)
        return (Fr(0), Fr(0))
    total = arb(0)
    for lo, hi in zip(cuts, cuts[1:]):
        th_m = (float(lo.mid()) + float(hi.mid())) / 2
        sig_m = Fr(float(c.mid()) + float(R.mid())*math.cos(th_m)).limit_denominator(10**12)
        a0, a1 = piece(sig_m)
        A0, A1 = A(a0), A(a1)
        f = lambda th, analytic: A0 + A1*(acb(c) + acb(R)*th.cos())
        total += flint.acb.integral(f, acb(lo), acb(hi)).real
    return total

# ---------------- Bourgain profile: Lambda(e_B), Corollaries 1.2 and 1.4(a) ----------------
k, l = Fr(13, 84), Fr(55, 84); nodesB = []
for j in range(8):
    nodesB.append((l - k, k)); k, l = k/(2*k + 2), Fr(1, 2) + l/(2*k + 2)
nodesB.append((Fr(1), Fr(0)))
print('Bourgain nodes (1.6):', [(str(a), str(b)) for a, b in nodesB])
one = arb(1)
IB = closed_form(nodesB, one, one)
IB2 = rigorous_integral(nodesB, one, one)
LB = IB / (2*PI*LOG2)
show('Lambda(e_B) [closed form (5.9)]', LB)
show('Lambda(e_B) [Arb integration]   ', IB2 / (2*PI*LOG2))
assert (IB - IB2).abs_upper() < A(Fr(1, 10**60))
show('2 pi Lambda(e_B)', 2*PI*LB)
assert gt(LB, Fr('0.096816006')) and lt(LB, Fr('0.096816007'))
assert lt(2*PI*LB, Fr('0.60832'))
print('checked: 0.096816006 < Lambda(e_B) < 0.096816007,  2 pi Lambda(e_B) < 0.60832')
show('margin Lambda(e_B) - 0.096816006', LB - A(Fr('0.096816006')))

# ---------------- Lindelof profile: Lambda(0) ----------------
nodesL = [(Fr(1, 2), Fr(0)), (Fr(1), Fr(0))]
L0 = closed_form(nodesL, one, one) / (2*PI*LOG2)
show('Lambda(0)', L0); show('2 pi Lambda(0)', 2*PI*L0)

# ---------------- explicit profile: C_1, C_2 (Theorem 1.3) ----------------
nodesE = [(Fr(1, 2), Fr(27, 164))] + [(1 - Fr(m, 2**m - 2), Fr(1, 2**m - 2)) for m in range(4, 10)] + [(Fr(1), Fr(0))]
print('explicit nodes (4.5):', [(str(a), str(b)) for a, b in nodesE])
c, R = A(Fr('1.000002')), A(Fr('1.000005'))
sig1 = c + (c - HALF)**2 / R; delta = 2*c - sig1 - HALF
D = (R / (c - HALF)).log()
show('sigma#', sig1); show('delta#', delta); show('d = log(R/(c-1/2))', D)
assert gt(delta, Fr(1, 4)) and lt(delta, Fr(5, 8))
IE = closed_form(nodesE, c, R)
IE2 = rigorous_integral(nodesE, c, R)
show('I_{e_E*} [closed form (5.9)]', IE)
show('I_{e_E*} [Arb integration]   ', IE2)
assert (IE - IE2).abs_upper() < A(Fr(1, 10**60))
C1 = IE / (2*PI*D); C2 = 1 / (2*D)
show('C_1', C1); show('C_2', C2)
assert lt(C1, Fr('0.09783')) and lt(C2, Fr('0.7214'))
print('checked: C_1 < 0.09783,  C_2 < 0.7214')

# ---------------- zeta values ----------------
lzs = sig1.zeta().log()
lzr = (c.zeta() / (2*c).zeta()).log()
show('log zeta(sigma#)', lzs); show('log(zeta(c)/zeta(2c))', lzr)
assert lt(lzs, Fr('1.52499'))
print('checked: log zeta(sigma#) < 1.52499')

# ---------------- constant term C_3(100) ----------------
t0 = A(98)
eps_chi = (A(Fr(1, 3)) + A(Fr('2.0005'))/6)/t0 + A(Fr('0.87'))/t0**2
chi_fac = eps_chi.exp()
K1 = 2*(1 + A(Fr('84.5'))/t0**2)**(1 + A(Fr(27, 164))) * (1 + (A(Fr('84.5'))/t0**2 + PI/2)/t0.log())
K = chi_fac*K1
show('factor chi', chi_fac); show('K_1', K1); show('K = chi K_1', K)
assert lt(K, Fr('2.74')) and lt(K1, Fr('2.74'))
T = A(100); Kr = A(Fr('2.74'))
Eterm = ((640*delta - 112)/(1536*(3*T - 1)) + A(Fr(1, 1024)))/2
assert lt(Eterm, Fr('0.00055'))
C3base = C2*(lzr + (1 + 3/T).log() + Kr.log()) + (lzs + (sig1 - HALF)/T)/PI + Eterm + A(Fr(1, 4))
C3T = C3base + 2*C1/T + 2*C2/(T*T.log())
C3ex = C3base + C1*((T + 2).log() - T.log()) + C2*((T + 2).log().log() - T.log().log())
show('E/(2 pi)', Eterm); show('C_3(100)', C3T); show('C_3(100) with exact differences', C3ex)
assert lt(C3T, Fr('10.6')) and lt(C3ex, Fr('10.6'))
print('checked: K, K_1 < 2.74,  E/(2pi) < 0.00055,  C_3(100) < 10.6')

# ---------------- crossing points ----------------
def bw_diff(L):   # ours - Bellotti-Wong (Cor. 1.5), L = log T, first branch of their minimum
    return A(Fr('0.09783'))*L + A(Fr('0.7214'))*L.log() + A(Fr('10.6')) - (A(Fr('0.10076'))*L + A(Fr('0.24460'))*L.log() + A(Fr('7.20844')))
def bw_diff2(L):  # ours - Bellotti-Wong, second branch
    return A(Fr('0.09783'))*L + A(Fr('0.7214'))*L.log() + A(Fr('10.6')) - (A(Fr('0.10076'))*L + A(Fr('1.68845'))*L.log() + A(Fr('1.50956')))
def bisect(f, lo, hi, n=400):
    lo, hi = A(lo), A(hi)
    assert f(lo) > 0 and f(hi) < 0
    for _ in range(n):
        mid = (lo + hi)/2
        v = f(mid)
        if v > 0: lo = mid
        elif v < 0: hi = mid
        else: break
    return lo, hi
lo, hi = bisect(bw_diff, 2000, 3000)
show('crossing with Bellotti-Wong, log T in [lo', lo); show('                                    hi]', hi)
# ours < BW for every L > hi: on L >= 52 the first branch is the minimum (log L >= 3.95),
# and d/dL bw_diff = -0.00293 + 0.4768/L < 0 for L > 163; bw_diff(hi) < 0.
# ours > BW for 1 <= L <= 163: checked on a cover of [1, 163] by balls, using both branches.
def cover_positive(lo_, hi_, steps):
    a = A(lo_); h = (hi_ - a)/steps
    for i in range(steps):
        x = arb((a + i*h + h/2).mid(), (h/2).mid() + A(Fr(1, 10**30)).mid())   # ball covering [a+ih, a+(i+1)h]
        assert bw_diff(x) > 0 or bw_diff2(x) > 0       # ours exceeds one branch, hence their minimum
cover_positive(1, 163, 20000)   # on [163, lo) bw_diff is decreasing and bw_diff(lo) = 0, so it is > 0 there
assert bool(A(Fr(52)).log() > A(Fr('3.95'))) and bool(A(Fr('5.69888'))/A(Fr('1.44385')) < A(Fr('3.95')))   # first branch is the minimum for L >= 52
print('checked: (1.7) is smaller than Bellotti-Wong exactly for log T > 2425.8386...')
def yang(L):      # Yang (4.29) without 0.2/t0  minus  (1.8)
    return A(Fr('0.11'))*L + A(Fr('0.29'))*L.log() + A(Fr('2.29')) - (A(Fr('0.09783'))*L + A(Fr('0.7214'))*L.log() + A(Fr('10.7')))
ylo, yhi = bisect(lambda L: -yang(L), 900, 1000)
show('crossing with Yang (4.29), log t in [lo', ylo); show('                              hi]', yhi)
assert yang(A(Fr('933.5'))) > 0      # increasing for L > 35.5, since 0.01217 - 0.4314/L > 0
print('checked: (1.8) is smaller than Yang (4.29) for log t > 933.5')
print('all checks passed')
