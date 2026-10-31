# Certified (Arb ball arithmetic, python-flint) check of the numerical claims of
# casanya_ordinal_primes_v47.tex that are NOT already covered by constants_arb.py
# (and re-checks of the digits that the paper prints for the constants certified there).
#
# Conventions.
#  * Every quantity is an Arb ball containing the exact value (outward rounding).
#  * check(line, label, ok): ok must be a bool obtained from a comparison of WHOLE balls
#    (Arb comparisons return True only when they hold for every point of the balls).
#  * Decimal constants of the paper are exact rationals (Fraction('0.09783')).
#  * "x = d..." in the paper (digits followed by an ellipsis) is read as TRUNCATION:
#    d <= x < d + 10^-k for x > 0 (and d - 10^-k < x <= d for x < 0); a display without ellipsis
#    that is used as an upper bound is checked as an upper bound.
#  * A claim that FAILS is certified as failing: the program asserts the negation on the ball
#    and prints 'FAILS (certified)'; it is then listed in inventory.md under FAILURES.
#  * Statements on a range of t are certified by an analytic monotonicity argument (stated in a
#    comment) plus endpoint checks on balls, or by covering the range with balls; never by sampling.
#  * Polynomial identities in one variable of degree <= n are certified by exact rational
#    evaluation at n+1 distinct points (a nonzero polynomial of degree <= n has at most n roots).
import sys, math, flint
from flint import arb, acb, ctx
from fractions import Fraction as Fr

ctx.prec = 256
DIG = 40
print('Python', sys.version.split()[0], ' python-flint', flint.__version__, ' precision', ctx.prec, 'bits')

def A(q):
    q = Fr(q); return arb(q.numerator) / q.denominator
def show(name, x):
    print('    ', name, '=', x.str(DIG, radius=True))
PI, LOG2, HALF = arb.pi(), arb(2).log(), A(Fr(1, 2))
E = arb(1).exp()

RESULTS = []          # (line, label, status)
def check(line, label, ok):
    assert ok is True, 'FAILED: line %s: %s' % (line, label)
    RESULTS.append((line, label, 'CERTIFIED'))
    print('[line %s] CERTIFIED: %s' % (line, label))
def check_fails(line, label, neg_ok, true_value):
    """the paper's claim is false; neg_ok certifies the negation on the whole ball"""
    assert neg_ok is True, 'could not certify the failure: line %s: %s' % (line, label)
    RESULTS.append((line, label, 'FAILS'))
    print('[line %s] FAILS (certified): %s ; true value %s' % (line, label, true_value.str(DIG, radius=True)))

def ulp(s):
    s = s.lstrip('-')
    k = len(s.split('.')[1]) if '.' in s else 0
    return Fr(1, 10**k)
def trunc_ok(x, s):          # x = s... (truncated display)
    d = Fr(s); u = ulp(s)
    if d >= 0: return bool(x >= A(d)) and bool(x < A(d + u))
    return bool(x <= A(d)) and bool(x > A(d - u))
def trunc_fails(x, s):       # certified negation of trunc_ok
    d = Fr(s); u = ulp(s)
    if d >= 0: return bool(x < A(d)) or bool(x >= A(d + u))
    return bool(x > A(d)) or bool(x <= A(d - u))
def le(x, q): return bool(x <= A(q))
def lt(x, q): return bool(x < A(q))
def gt(x, q): return bool(x > A(q))
def ge(x, q): return bool(x >= A(q))
def tiny(x, eps=Fr(1, 10**60)): return bool(x.abs_upper() < A(eps))

# ======================================================================================
# 1. Exact integrals of piecewise-linear reflected profiles over Backlund's circle.
#    Third independent evaluation (constants_arb.py has the hinge closed form (5.9) and
#    acb.integral).  For e*(sigma) = a0 + a1 sigma on sigma in [lo, hi], with sigma = c + R cos(theta),
#    int a0 + a1 (c + R cos th) dth = (a0 + a1 c)(th2 - th1) + a1 R (sin th2 - sin th1), exactly,
#    with th = arccos((sigma - c)/R) and sin th = sqrt(1 - ((sigma - c)/R)^2).
# ======================================================================================
def acos_clip(u):            # u exact rational; returns (theta, sin theta) as balls
    if u >= 1:  return arb(0), arb(0)
    if u <= -1: return PI, arb(0)
    a = A(u); return a.acos(), (1 - a*a).sqrt()

def pieces_reflected(nodes, left=None):
    """pieces (lo, hi, a0, a1) of e* on R; nodes = [(1/2, e0), ..., (1, 0)] exact.
    left: None -> exact reflection (eq:reflected); otherwise (a0, a1) of an affine function used on [0, 1/2]."""
    P = [(None, Fr(0), Fr(1, 2), Fr(-1))]                               # sigma < 0: 1/2 - sigma
    for (x0, e0), (x1, e1) in zip(nodes, nodes[1:]):
        s = (e1 - e0) / (x1 - x0)
        P.append((x0, x1, e0 - s*x0, s))                                 # sigma in [x0, x1]
        if left is None:
            P.append((1 - x1, 1 - x0, Fr(1, 2) + e0 + s*(1 - x0), -1 - s))  # 1/2 - sigma + e(1 - sigma)
    if left is not None:
        P.append((Fr(0), Fr(1, 2), left[0], left[1]))
    P.append((Fr(1), None, Fr(0), Fr(0)))                                # sigma > 1: 0
    return P

def circle_integral(P, c, R):
    c, R = Fr(c), Fr(R); tot = arb(0)
    cb, Rb = A(c), A(R)
    for lo, hi, a0, a1 in P:
        th1, s1 = (arb(0), arb(0)) if hi is None else acos_clip((hi - c) / R)
        th2, s2 = (PI, arb(0)) if lo is None else acos_clip((lo - c) / R)
        tot += (A(a0) + A(a1)*cb)*(th2 - th1) + A(a1)*Rb*(s2 - s1)
    return tot

# --- hinge closed form (5.9), copied from constants_arb.py (independent code path) ---
def closed_form(nodes, c, R):
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

print('\n=== Bourgain profile (eq:bourgain_nodes), Corollary cor:bourgain, Corollary cor:distance(a) ===')
k_, l_ = Fr(13, 84), Fr(55, 84); nodesB = []; kap = []
for j in range(8):
    nodesB.append((l_ - k_, k_)); kap.append(k_); k_, l_ = k_/(2*k_ + 2), Fr(1, 2) + l_/(2*k_ + 2)
nodesB.append((Fr(1), Fr(0)))
displayed = [(Fr(1,2),Fr(13,84)),(Fr(139,194),Fr(13,194)),(Fr(173,207),Fr(13,414)),(Fr(773,854),Fr(13,854)),
             (Fr(820,867),Fr(13,1734)),(Fr(3387,3494),Fr(13,3494)),(Fr(1149,1169),Fr(13,7014)),
             (Fr(13921,14054),Fr(13,14054)),(Fr(1),Fr(0))]
check(387, 'the nine displayed nodes equal (lambda_j-kappa_j, kappa_j), (kappa_j,lambda_j)=A^j(13/84,55/84), then (1,0) (exact)', nodesB == displayed)
xsB = [a for a, _ in nodesB]
check(925, 'at eps\'=0 the nodes varsigma\'_j increase, varsigma\'_7 < 1, all >= 1/2, kappa_j decrease (exact)',
      all(x < y for x, y in zip(xsB, xsB[1:])) and xsB[7] < 1 and all(x >= Fr(1,2) for x in xsB)
      and all(a > b for a, b in zip(kap, kap[1:])))
PB = pieces_reflected(nodesB)
IB_pl = circle_integral(PB, 1, 1)
IB_cf = closed_form(nodesB, arb(1), arb(1))
check(937, 'Lambda(e_B): exact piecewise antiderivative and hinge closed form (5.9) agree to 1e-60', tiny(IB_pl - IB_cf))
LB = IB_pl / (2*PI*LOG2); show('Lambda(e_B)', LB); show('2 pi Lambda(e_B)', 2*PI*LB)
check(937, 'theta_h = arccos((1/2-c)/R) = 2pi/3 at c=R=1', tiny(((HALF - 1)/1).acos() - 2*PI/3))
check(394, 'Lambda(e_B) = 0.0968160063...', trunc_ok(LB, '0.0968160063'))
check(937, 'Lambda(e_B) = 0.0968160063238...', trunc_ok(LB, '0.0968160063238'))
check(305, 'abstract: limsup |S|/log T <= 0.0968160... (value of Lambda(e_B))', trunc_ok(LB, '0.0968160'))
check(939, '0.096816006 <= Lambda(e_B) <= 0.096816007', ge(LB, Fr('0.096816006')) and le(LB, Fr('0.096816007')))
check(413, '2 pi Lambda(e_B) = 0.6083129... < 0.60832', trunc_ok(2*PI*LB, '0.6083129') and lt(2*PI*LB, Fr('0.60832')))
check(998, '2 pi * 0.0968160063238... = 0.6083129...', trunc_ok(2*PI*LB, '0.6083129'))
check(1634, 'margins >= 3e-10: Lambda(e_B)-0.096816006, 0.096816007-Lambda(e_B), 0.60832-2piLambda(e_B)',
      ge(LB - A(Fr('0.096816006')), Fr(3, 10**10)) and ge(A(Fr('0.096816007')) - LB, Fr(3, 10**10))
      and ge(A(Fr('0.60832')) - 2*PI*LB, Fr(3, 10**10)))
show('margin Lambda(e_B) - 0.096816006', LB - A(Fr('0.096816006')))

print('\n=== Lindelof profile, Remark rem:lindelof, Proposition prop:distance_sharp ===')
PL = pieces_reflected([(Fr(1, 2), Fr(0)), (Fr(1), Fr(0))])
IL = circle_integral(PL, 1, 1)
L0 = IL / (2*PI*LOG2)
L0_closed = (3*arb(3).sqrt() - PI) / (12*PI*LOG2)
show('Lambda(0)', L0); show('2 pi Lambda(0)', 2*PI*L0)
check(921, 'int_{2pi/3}^{pi} (-1/2 - cos th) dth = sqrt3/2 - pi/6 (equals the circle integral of 0*)',
      tiny(IL - (arb(3).sqrt()/2 - PI/6)))
check(917, 'Lambda(0) = (3 sqrt3 - pi)/(12 pi log 2) (agreement to 1e-60 with the exact circle integral)', tiny(L0 - L0_closed))
check(917, 'Lambda(0) = 0.0786252...', trunc_ok(L0, '0.0786252'))
check(525, 'Lambda(0) = 0.0786252...', trunc_ok(L0, '0.0786252'))
check(920, 'Lindelof would give a <= 0.0786253 (Lambda(0) <= 0.0786253)', le(L0, Fr('0.0786253')))
check(1002, '2 pi Lambda(0) = 0.49401...', trunc_ok(2*PI*L0, '0.49401'))

print('\n=== Explicit profile (eq:explicit_nodes), Lemma lem:explicit_zeta nodes ===')
sig_m = {m: 1 - Fr(m, 2**m - 2) for m in range(4, 10)}
check(815, 'sigma_m = 1 - m/(2^m-2), 4<=m<=9, equal 5/7, 5/6, 28/31, 17/18, 123/127, 167/170 and 1/(2^m-2) = 1/14,...,1/510 (exact)',
      [sig_m[m] for m in range(4, 10)] == [Fr(5,7),Fr(5,6),Fr(28,31),Fr(17,18),Fr(123,127),Fr(167,170)]
      and [Fr(1, 2**m - 2) for m in range(4, 10)] == [Fr(1,14),Fr(1,30),Fr(1,62),Fr(1,126),Fr(1,254),Fr(1,510)])
nodesE = [(Fr(1, 2), Fr(27, 164))] + [(sig_m[m], Fr(1, 2**m - 2)) for m in range(4, 10)] + [(Fr(1), Fr(0))]
vs = [a for a, _ in nodesE] + [Fr(3)]; es = [b for _, b in nodesE] + [Fr(0)]
check(822, 'varsigma_0<...<varsigma_8 increase, e_i = 1/(2^{i+3}-2) (1<=i<=6), e_i nonincreasing, max e_i = 27/164, Q=10 > 1-varsigma_i (exact)',
      all(x < y for x, y in zip(vs, vs[1:])) and all(es[i] == Fr(1, 2**(i+3) - 2) for i in range(1, 7))
      and all(x >= y for x, y in zip(es, es[1:])) and max(es) == Fr(27, 164) and all(10 > 1 - v for v in vs))

print('\n=== Theorem thm:explicit: disc parameters c = 1.000002, R = 1.000005 ===')
cF, RF = Fr('1.000002'), Fr('1.000005')
sigF = cF + (cF - Fr(1, 2))**2 / RF          # exact rational
delF = 2*cF - sigF - Fr(1, 2)
cB, RB = A(cF), A(RF)
sig1, delta = A(sigF), A(delF)
show('sigma#', sig1); show('delta#', delta)
check(942, 'c - R = -3e-6 (exact)', cF - RF == Fr(-3, 10**6))
check(942, 'sigma# = 1.25000275... and delta# = 0.2500012499... (sigma#, delta# exact rationals)',
      trunc_ok(sig1, '1.25000275') and trunc_ok(delta, '0.2500012499'))
check(942, 'conditions (eq:backlund_conditions): c-R<1/2<1<c<sigma#<c+R, c<R, 0<delta#<1/2, and delta# in [1/4,5/8], c<=2, R<=2 (exact)',
      cF - RF < Fr(1,2) < 1 < cF < sigF < cF + RF and cF < RF and 0 < delF < Fr(1,2) and Fr(1,4) <= delF <= Fr(5,8)
      and cF <= 2 and RF <= 2)
check(942, '[c-R, c+R] in [-0.01, 3] (exact)', cF - RF >= Fr('-0.01') and cF + RF <= 3)
D = (RB / (cB - HALF)).log()
PE = pieces_reflected(nodesE)
IE_pl = circle_integral(PE, cF, RF)
IE_cf = closed_form(nodesE, cB, RB)
check(957, 'I_{e_E*}: exact piecewise antiderivative and hinge closed form (5.9) agree to 1e-60', tiny(IE_pl - IE_cf))
# count of the arccos arguments in the closed form: theta_h and, for the 7 hinges (6 interior nodes and sigma=1),
# theta_varsigma and theta'_varsigma
args = set([(Fr(1, 2) - cF) / RF])
for a, _ in nodesE[1:]:
    args.add((a - cF) / RF); args.add((1 - a - cF) / RF)
check(957, 'the closed form uses exactly fifteen distinct arccos values at rational points in (-1,1) (and fifteen square roots)',
      len(args) == 15 and all(-1 < u < 1 for u in args))
C1 = IE_pl / (2*PI*D); C2 = 1 / (2*D)
lzr = (cB.zeta() / (2*cB).zeta()).log()
lzs = sig1.zeta().log()
show('I_{e_E*}', IE_pl); show('C_1', C1); show('C_2', C2); show('log(zeta(c)/zeta(2c))', lzr); show('log zeta(sigma#)', lzs)
check(959, 'C_1 = 0.0978292318785...', trunc_ok(C1, '0.0978292318785'))
check(405, 'Backlund quotient 0.0978292318... for e_E', trunc_ok(C1, '0.0978292318'))
check(959, 'C_2 = 1/(2d) = 0.7213464797...', trunc_ok(C2, '0.7213464797'))
check(959, 'log(zeta(c)/zeta(2c)) = 12.6246665...', trunc_ok(lzr, '12.6246665'))
check(965, 'log(zeta(c)/zeta(2c)) <= 12.62467 (rounded up in eq:explicit_assembled)', le(lzr, Fr('12.62467')))
check(966, 'sigma# - 1/2 <= 0.7501 (term 0.7501/(pi T))', le(sig1 - HALF, Fr('0.7501')))
check(970, 'log zeta(sigma#) = 1.52498... and <= 1.52499', trunc_ok(lzs, '1.52498') and le(lzs, Fr('1.52499')))
# footnote: zeta(s) <= sum_{n<N} n^-s + (N-1/2)^{1-s}/(s-1), N = 10^4 (Arb sum of 9999 terms)
N = 10**4
ssum = arb(0)
for n in range(1, N):
    ssum += (-sig1*arb(n).log()).exp()
zbound = ssum + ((1 - sig1)*A(Fr(2*N - 1, 2)).log()).exp() / (sig1 - 1)
show('footnote bound for zeta(sigma#) with N=10^4', zbound); show('its log', zbound.log())
check(970, 'footnote: zeta(sigma#) <= sum_{n<N} n^-s + (N-1/2)^{1-s}/(s-1) (consistency) and its log <= 1.5249836',
      bool(sig1.zeta() <= zbound) and le(zbound.log(), Fr('1.5249836')))
m640 = 640*delta - 112
show('640 delta# - 112', m640)
check(974, '640 delta# - 112 > 0 (majorant of E/(2pi) decreasing in T)', gt(m640, 0))
if trunc_ok(m640, '48.0008'):
    check(974, '640 delta# - 112 = 48.0008...', True)
else:
    check_fails(974, "'640 delta# - 112 = 48.0008...' read as truncated digits (true value 48.000799999..., i.e. 48.0007...; rounded 48.0008)",
                trunc_fails(m640, '48.0008'), m640)
Emaj = (m640 / (1536*299) + A(Fr(1, 1024))) / 2
show('majorant of E(100, delta#)/(2 pi)', Emaj)
check(970, 'E(T,delta#)/(2pi) <= (1/2)((640 delta# -112)/(1536*299) + 2^-10) < 0.00055 at T = 100 (3T-1 = 299)', lt(Emaj, Fr('0.00055')))

print('\n=== constant term C_3(100) (Section subsec:proof_explicit) ===')
T = A(100); K274 = A(Fr('2.74'))
def C3_of(c1, c2, lz_ratio, lz_sig, sig_term):
    base = c2*(lz_ratio + (1 + 3/T).log() + K274.log()) + lz_sig/PI + sig_term/(PI*T) + Emaj + A(Fr(1, 4))
    return base + 2*c1/T + 2*c2/(T*T.log()), base + c1*((T + 2).log() - T.log()) + c2*((T + 2).log().log() - T.log().log())
C3T, C3ex = C3_of(C1, C2, lzr, lzs, sig1 - HALF)                                      # exact values
C3disp, _ = C3_of(C1, C2, A(Fr('12.62467')), lzs, A(Fr('0.7501')))                    # eq:explicit_assembled as displayed
C3up, _ = C3_of(A(Fr('0.0978292318786')), A(Fr('0.7213464798')), A(Fr('12.62467')),
                A(Fr('1.52499')), A(Fr('0.7501')))                                    # every displayed value rounded up
show('C_3(100) (exact constants)', C3T); show('C_3(100) with exact differences', C3ex)
show('C_3(100) with 12.62467 and 0.7501 (eq:explicit_assembled)', C3disp)
show('C_3(100) with all displayed values rounded up', C3up)
check(976, 'C_3(100) = 10.598602... (exact constants, costs 2C_1/T + 2C_2/(T log T))', trunc_ok(C3T, '10.598602'))
check(976, 'same sum with exact differences log102-log100, loglog102-loglog100 = 10.598545...', trunc_ok(C3ex, '10.598545'))
check(1628, 'C_3(100) = 10.5986... and 10.5985... (appendix)', trunc_ok(C3T, '10.5986') and trunc_ok(C3ex, '10.5985'))
check(974, 'with the rounded values displayed, C_3(100) <= 10.5987 (12.62467, 0.7501, and also with C_1, C_2, log zeta(sigma#) rounded up)',
      le(C3disp, Fr('10.5987')) and le(C3up, Fr('10.5987')))
check(978, '10.6 > C_3(100) (all variants), 0.09783 > C_1, 0.7214 > C_2',
      lt(C3T, Fr('10.6')) and lt(C3ex, Fr('10.6')) and lt(C3disp, Fr('10.6')) and lt(C3up, Fr('10.6'))
      and lt(C1, Fr('0.09783')) and lt(C2, Fr('0.7214')))
check(1634, 'margins >= 3e-10 for C_1<0.09783, C_2<0.7214, C_3(100)<10.6, log zeta(sigma#)<=1.52499',
      ge(A(Fr('0.09783')) - C1, Fr(3, 10**10)) and ge(A(Fr('0.7214')) - C2, Fr(3, 10**10))
      and ge(A(Fr('10.6')) - C3T, Fr(3, 10**10)) and ge(A(Fr('1.52499')) - lzs, Fr(3, 10**10)))
show('margin 1.52499 - log zeta(sigma#)', A(Fr('1.52499')) - lzs)
# C_3(T) is nonincreasing on [100, oo): log((T+3)/T), 0.7501/(pi T), 2C_1/T, 2C_2/(T log T) and the majorant
# (640 delta#-112)/(1536(3T-1)) (numerator > 0, certified above) decrease; the other terms are constant.
# Small heights: for e <= T <= 100 the right side of (eq:explicit_S) is >= its value at T = e (log T, loglog T increase).
rhs_e = A(Fr('0.09783'))*E.log() + A(Fr('0.7214'))*E.log().log() + A(Fr('10.6'))
check(978, 'for e <= T <= 100: 2.5167 < 0.09783 log T + 0.7214 loglog T + 10.6 (value at T=e, RHS increasing); 100 <= 30 610 046 000',
      gt(rhs_e, Fr('2.5167')) and 100 <= 30610046000)
check(978, '|varpi(T)|/pi <= 0.53/(pi e) < 0.07 for T >= e', lt(A(Fr('0.53'))/(PI*E), Fr('0.07')))

print('\n=== Backlund quotients in the limit c, R -> 1 (Section subsec:literature) ===')
LE1 = circle_integral(PE, 1, 1) / (2*PI*LOG2)
PBW = pieces_reflected(nodesE, left=(Fr(1, 2), -1 + 2*Fr(27, 164)))   # BW: chord from (0,1/2) to (1/2,27/164) on [0,1/2]
LBW1 = circle_integral(PBW, 1, 1) / (2*PI*LOG2)
show('Lambda(e_E) (reflected explicit profile, c=R=1)', LE1); show('BW linear-left profile, c=R=1', LBW1)
check(519, 'BW-profile quotient at c,R->1 = 0.10073687...', trunc_ok(LBW1, '0.10073687'))
check(519, 'reflected-profile quotient at c,R->1 = 0.09782899...', trunc_ok(LE1, '0.09782899'))
# the disc at c=R=1 covers sigma in [0,2], so the BW profile is only needed on [0,2]; the chord lies above the reflection:
check(516, 'the reflected profile lies below the chord on [0,1/2]: checked at the reflected nodes (both piecewise linear, chord affine)',
      all(Fr(1,2) - (1 - a) + b <= Fr(1,2) + (-1 + 2*Fr(27,164))*(1 - a) for a, b in nodesE))

print('\n=== Lemma lem:chi: |chi(sigma+it)| <= 1.0070 (t/2pi)^{1/2-sigma}, -0.01<=sigma<=1/2, t>=98 ===')
check(793, 'omega_1=(1-sigma)/2 in [1/4,0.505], omega_2=sigma/2 in [-0.005,1/4], omega_1-omega_2=1/2-sigma; y=t/2>=49 (exact, affine in sigma)',
      (1 - Fr('-0.01'))/2 == Fr('0.505') and (1 - Fr(1,2))/2 == Fr(1,4) and Fr('-0.01')/2 == Fr('-0.005') and Fr(98, 2) == 49)
# |(omega-1/2)/2 log(1+omega^2/y^2)| <= |omega-1/2| omega^2/(2 y^2) <= 0.505*0.256/(2y^2)   (log(1+x) <= x)
# |y arctan(omega/y) - omega| <= |omega|^3/(3y^2) <= 0.043/y^2                         (alternating Taylor series)
check(806, '0.505^2 <= 0.256, 0.505^3/3 <= 0.043, 0.505*0.256/2 + 0.043 <= 0.108, 0.108*4 <= 0.435 (|phi| <= 0.108/y^2 <= 0.435/t^2)',
      Fr('0.505')**2 <= Fr('0.256') and Fr('0.505')**3/3 <= Fr('0.043') and Fr('0.505')*Fr('0.256')/2 + Fr('0.043') <= Fr('0.108')
      and 4*Fr('0.108') <= Fr('0.435'))
ph2 = PI/2 + (A(Fr('0.005'))/49).atan()            # upper bound for ph z_2 (omega_2 >= -0.005, y >= 49)
sec2 = 1 / ((ph2/2).cos())**2
show('sec^2(ph z_2 / 2) upper', sec2)
check(806, 'sec^2(1/2 ph z_i) <= 2.0005 (ph z_2 <= pi/2 + arctan(0.005/49); sec^2 increasing on [0,pi/2))', le(sec2, Fr('2.0005')))
check(806, '|R(z_1)|+|R(z_2)| <= 2*2.0005/(6t) <= 0.6669/t and 2*0.435/t^2 = 0.87/t^2', 2*Fr('2.0005')/6 <= Fr('0.6669') and 2*Fr('0.435') == Fr('0.87'))
epsc = A(Fr('0.6669'))/98 + A(Fr('0.87'))/98**2
show('0.6669/98 + 0.87/98^2', epsc)
check(806, '0.6669/t + 0.87/t^2 <= 0.00690 for t >= 98 (decreasing in t; value at 98)', le(epsc, Fr('0.00690')))
check(806, 'e^{0.0069} < 1.0070', lt(A(Fr('0.0069')).exp(), Fr('1.0070')))
show('e^0.0069', A(Fr('0.0069')).exp())

print('\n=== Lemma lem:explicit_zeta ===')
check(829, '1/6 - 27/164 = 1/492 (exact)', Fr(1,6) - Fr(27,164) == Fr(1,492))
check(829, 'sigma=1/2, |t|<=e^105: e^{105/492} < 2/0.618', bool(A(Fr(105,492)).exp() < A(2)/A(Fr('0.618'))))
check(829, 'sigma=1/2, |t|>e^105: log|t| > 105 > 66.7/2', 105 > Fr('66.7')/2)
check(829, 'Yang lines: 1.546 <= 2 (|t|>=T_m) and 1.878 <= 2 (3<=|t|<=T_m, Remark rem:robust(ii)); 1-line: constant 1 <= 2',
      Fr('1.546') <= 2 and Fr('1.878') <= 2)
check(829, 'sigma=3: zeta(3) < 2 log 3 (<= 2 log|t| for |t|>3)', bool(arb(3).zeta() < 2*arb(3).log()))
# |t|<=3, 1/2<=sigma<=3: |s| <= sqrt(3^2+3^2) = sqrt 18, |s-1| <= sqrt(2^2+3^2) = sqrt 13; int_1^oo {u}u^{-sigma-1} <= 1/sigma <= 2
check(829, '|t|<=3: sqrt18 <= 4.243, sqrt13 <= 3.606, 4.243 + 2*4.243*3.606 < 34.9',
      le(arb(18).sqrt(), Fr('4.243')) and le(arb(13).sqrt(), Fr('3.606'))
      and Fr('4.243') + 2*Fr('4.243')*Fr('3.606') < Fr('34.9'))
check(829, '|t|<=3: right side of (eq:boundary) >= 2*10.5*log 10.5 > 49 (|Q+s| >= Q+1/2 = 10.5 > 1, exponent >= 1)',
      gt(2*A(Fr('10.5'))*A(Fr('10.5')).log(), 49))
# t >= 98, sigma in [-0.01,3]: |Q+s|^2 <= 13^2 + t^2 (Q+sigma in [9.99,13]); sqrt(t^2+169) <= t + 169/(2t) = t(1+84.5/t^2);
# |Log(Q+s)| <= log|Q+s| + pi/2 <= log t + 84.5/t^2 + pi/2 (log(1+x) <= x); |s-1| >= t.
# Each factor of K_1(t) = 2(1+84.5/t^2)^{1+27/164}(1+(84.5/t^2+pi/2)/log t) decreases in t, so K_1(98) bounds t >= 98.
t0 = A(98)
K1 = 2*(1 + A(Fr('84.5'))/t0**2)**(1 + A(Fr(27, 164))) * (1 + (A(Fr('84.5'))/t0**2 + PI/2)/t0.log())
show('K_1(98)', K1)
check(836, '13^2 = 169 and 169/2 = 84.5 (exact)', 13**2 == 169 and Fr(169, 2) == Fr('84.5'))
check(840, '2(1+84.5/98^2)^{1+27/164}(1+(84.5/98^2+pi/2)/log 98) <= 2.7167', le(K1, Fr('2.7167')))
show('margin 2.7167 - K_1(98)', A(Fr('2.7167')) - K1)
check(845, 'reflection: 1.0070 * 2.7167 <= 2.74; 1 - sigma in (1/2, 1.01] for sigma in [-0.01, 1/2)', Fr('1.0070')*Fr('2.7167') <= Fr('2.74'))

print('\n=== Remark rem:robust ===')
check(849, '(i) |t|^{1/492} <= e^{577/492} < 2/0.618 for 3 < |t| <= e^577', bool(A(Fr(577,492)).exp() < A(2)/A(Fr('0.618'))))
show('2/0.618 - e^{577/492}', A(2)/A(Fr('0.618')) - A(Fr(577,492)).exp())
check(849, '(i) above e^577 any C <= 1154 = 2*577 suffices (C t^{27/164} <= 2 t^{27/164} log t)', 2*577 == 1154)
# (ii) the constant 1.87781 is certified by yang_smallt_arb.py (Arb, 120 bits); re-run separately, output recorded in inventory.md.
check(1644, '(ii) Yang exponent split (1-sigma_m)/3 = 1/(2K-2) + (m-3)/(6K-6), K = 2^{m-1}, and (m-3)/(6K-6) > 0, 4<=m<=9 (exact)',
      all(Fr(m, 2**m - 2)/3 == Fr(1, 2*2**(m-1) - 2) + Fr(m - 3, 6*2**(m-1) - 6) and Fr(m - 3, 6*2**(m-1) - 6) > 0 for m in range(4, 10)))
check(853, '(ii) 1.87781 <= 1.878 <= 2', Fr('1.87781') <= Fr('1.878') <= 2)

print('\n=== Lemma lem:varpi and the Riemann-von Mangoldt main term (Sections 1, 4, 5, 6) ===')
check(776, '1/16 + 1/8 + 1/3 = 25/48 < 0.53 (exact)', Fr(1,16) + Fr(1,8) + Fr(1,3) == Fr(25,48) < Fr('0.53'))
def N0(t): return t/(2*PI)*(t/(2*PI*E)).log() + A(Fr(7, 8))
check(354, 'N_0(2 pi) = -1/8 (ball contains -1/8, radius < 1e-60)', tiny(N0(2*PI) + A(Fr(1, 8))))
check(439, 'N_0(2 pi e) = 7/8 (ball contains 7/8, radius < 1e-60)', tiny(N0(2*PI*E) - A(Fr(7, 8))))
check(439, 'k >= 2 iff tau_k >= 2 pi e: N_0(tau_1) = 1/2 < 7/8 <= 3/2 = N_0(tau_2), N_0 increasing on (2pi,oo)', Fr(1,2) < Fr(7,8) <= Fr(3,2))
def theta(t):            # Riemann-Siegel theta; Arb's lgamma is the branch real on (0,oo), continuous off (-oo,0]
    return acb(A(Fr(1, 4)), t/2).lgamma().imag - t/2*PI.log()
def dtheta(t):           # theta'(t) = (1/2) Re psi(1/4 + it/2) - (1/2) log pi
    return acb(A(Fr(1, 4)), t/2).digamma().real/2 - PI.log()/2
a_, b_ = A(Fr('9.66')), A(Fr('9.67'))
def dtheta_pos(lo, hi, n):
    """theta' > 0 on [lo, hi]: |theta''| = |Im psi'(1/4+it/2)|/4 <= M on 40 sub-balls covering [lo, hi] (Arb trigamma),
    theta'(x_i) > M h at the n+1 grid points x_i (spacing 2h); every x in [lo,hi] is within h of a grid point."""
    lo, hi = A(lo), A(hi); M = arb(0)
    for i in range(40):
        x0 = lo + (hi - lo)*i/40; x1 = lo + (hi - lo)*(i + 1)/40
        b = arb(((x0 + x1)/2).mid(), ((x1 - x0)/2).upper())
        v = arb((acb(A(Fr(1, 4)), b/2).polygamma(1).imag/4).abs_upper())
        if bool(v > M): M = v
    h = (hi - lo)/(2*n)
    return all(bool(dtheta(lo + (hi - lo)*i/n) > M*h) for i in range(n + 1))
show('theta(9.66) + pi', theta(a_) + PI); show('theta(9.67) + pi', theta(b_) + PI); show('theta(6.5) + pi', theta(A(Fr('6.5'))) + PI)
check(359, "g_{-1} = 9.66...: theta' > 0 on [6.5, 9.67] (grid of 4001 points + Arb bound on theta''), theta(9.66) < -pi < theta(9.67): the root of theta = -pi on the increasing branch lies in [9.66, 9.67)",
      dtheta_pos(Fr('6.5'), Fr('9.67'), 4000) and bool(theta(a_) + PI < 0) and bool(theta(b_) + PI > 0))
check(359, '|varpi|/pi < 1/2 at the Gram points g_m, m >= -1 (t >= g_{-1} > 9.66: 0.53/(9.66 pi) < 1/2)', lt(A(Fr('0.53'))/(A(Fr('9.66'))*PI), Fr(1,2)))
g1 = acb.zeta_zero(1).imag
show('gamma_1 (Arb acb.zeta_zero, rigorous isolation)', g1)
check(994, 'gamma_1 > 14 > 2 pi > e (Arb rigorous first zero)', gt(g1, 14) and bool(A(14) > 2*PI) and bool(2*PI > E))
check(1185, '|s_k + Delta_k| < 1 for gamma_k >= 14: |varpi(gamma_k)|/pi <= 0.53/(14 pi) < 1/2', lt(A(Fr('0.53'))/(14*PI), Fr(1,2)))

print('\n=== Section sec:sublevel (construction, Proposition prop:ordered, proofs) ===')
check(1028, '(1/pi) arcsin(2^{-1/2}) = 1/4', tiny((1/arb(2).sqrt()).asin()/PI - A(Fr(1, 4))))
def m_of(j):             # m_j = floor(2^{j/2}), certified floor via ball comparisons
    if j % 2 == 0: return int(math.floor(Fr(2)**(j//2)))      # exact rational power of 2
    x = (A(Fr(j, 2))*LOG2).exp(); f = int(math.floor(float(x.mid())))   # irrational: the ball decides the floor
    assert bool(x > f) and bool(x < f + 1); return f
check(1045, 'block containing 2 pi is [4,8] (4 <= 2pi <= 8), m_2 = m_3 = 2 (floor of 2 and 2^{3/2})',
      bool(A(4) <= 2*PI) and bool(2*PI <= A(8)) and m_of(2) == 2 and m_of(3) == 2)
check(1045, 'F(2pi) <= N_0(2pi) + 2/4 = -1/8 + 1/2 = 3/8 < 1/2', bool(N0(2*PI) + A(Fr(2, 4)) < A(Fr(1, 2))) and Fr(-1,8) + Fr(1,2) == Fr(3,8))
check(1033, 'm_j = 0 for j <= -2 and m_{-1} = 0 (so m_j = m_{j+1} = 0 on blocks with t < 1/2); m_j nondecreasing, m_j <= 2 for j <= 3',
      all(m_of(j) == 0 for j in range(-6, 0)) and all(m_of(j) <= m_of(j + 1) for j in range(-6, 12)) and max(m_of(j) for j in range(-6, 4)) == 2)
check(547, 'on (0, 2pi]: F < 7/8 + 1/2 = 11/8 < 3/2 (N_0 < 7/8 on (0, 2 pi e), |Phi| <= m/4 <= 1/2)', Fr(7,8) + Fr(1,2) < Fr(3,2))
check(1047, '4 pi e > 2 pi^2 (so t/(4pi) > sqrt(2t)/4 for t >= 4 pi e, the two being equal at t = 2 pi^2)', bool(4*PI*E > 2*PI**2))
# N_0(t) - sqrt(2t)/4 has derivative L(t) - 1/(4 sqrt(2t)); L increases and 1/sqrt(2t) decreases, so it suffices at t = 2 pi e.
dd = (1/(2*PI)) * ((2*PI*E)/(2*PI)).log() - 1/(4*(2*(2*PI*E)).sqrt())
show("d/dt [N_0(t) - sqrt(2t)/4] at t = 2 pi e", dd)
check(1163, 'N_0(t) - sqrt(2t)/4 increases for t >= 2 pi e (derivative at 2 pi e > 0, derivative increasing)', bool(dd > 0))
check(1178, '2 log 2 - log(2 pi e) = -1.45...', trunc_ok(2*LOG2 - (2*PI*E).log(), '-1.45'))
show('2 log 2 - log(2 pi e)', 2*LOG2 - (2*PI*E).log())
# Fujii side condition: T >= 9 -> H >= sqrt T >= 3; H - H^{1/8} increasing for H >= 1 (derivative 1 - H^{-7/8}/8 > 0)
check(727, 'Fujii: H >= 3 implies H - H^{1/8} >= 3 - 3^{1/8} >= 1 (increasing in H)', bool(3 - (arb(3).log()/8).exp() >= 1))
# log(3+x)/log(2+x) decreases on x >= 0: derivative sign = (2+x)log(2+x) - (3+x)log(3+x) < 0 since u log u increases for u >= 1.
# line 737: log(3+x) <= (log3/log2) log(2+x) for x >= 0 is analytic (equality at x = 0, ratio decreasing); no numerical content.
# log(2 + h log 4T) <= 2 log(2 + h L_T), L_T = log(T/2pi), log 4T = L_T + log(8 pi), v = h L_T >= 1, 0 < h <= 1:
# (2+v)^2 - (2 + v + h log 8pi) >= v^2 + 3v + 2 - log 8pi >= 6 - log 8pi > 0.
check(1114, 'log(2+h log 4T) <= 2 log(2+h L_T) for h L_T >= 1, h <= 1: 6 > log(8 pi)', bool(A(6) > (8*PI).log()))

print('\n=== Proof of Theorem thm:asymptotic: the family c = 1+eta, R = 1+2eta, 0 < eta < 1/100 ===')
# every quantity is affine in eta (sigma# = c + (c-1/2)^2/R = 1+eta + (1/2+eta)/2 since (1/2+eta)^2/(1+2eta) = (1/2+eta)/2);
# an affine function is positive on (0, 1/100) iff it is >= 0 at both ends and > 0 at one of them (or > 0 at both).
def aff(f):  # f(eta) exact at eta = 0 and eta = 1/100
    return f(Fr(0)), f(Fr(1, 100))
def pos_open(f): a, b = aff(f); return a >= 0 and b >= 0 and (a > 0 or b > 0)
def sig_eta(e): return 1 + e + (Fr(1, 2) + e)**2 / (1 + 2*e)
check(899, 'sigma# = 5/4 + 3eta/2, delta# = 1/4 + eta/2, R/(c-1/2) = 2 (exact identities checked at eta = 0, 1/100, 1/7: affine/constant)',
      all(sig_eta(e) == Fr(5, 4) + Fr(3, 2)*e and 2*(1 + e) - sig_eta(e) - Fr(1, 2) == Fr(1, 4) + e/2 and (1 + 2*e)/(Fr(1, 2) + e) == 2
          for e in (Fr(0), Fr(1, 100), Fr(1, 7))))
check(899, 'conditions (eq:backlund_conditions) and delta# in [1/4,5/8], [c-R,c+R] = [-eta, 2+3eta] in [-0.01,3] for all eta in (0,1/100)',
      pos_open(lambda e: Fr(1, 2) - (1 + e - (1 + 2*e))) and pos_open(lambda e: (1 + e) - 1)
      and pos_open(lambda e: Fr(5, 4) + Fr(3, 2)*e - (1 + e)) and pos_open(lambda e: (2 + 3*e) - (Fr(5, 4) + Fr(3, 2)*e))
      and pos_open(lambda e: (1 + 2*e) - (1 + e)) and pos_open(lambda e: Fr(1, 4) + e/2) and pos_open(lambda e: Fr(1, 2) - Fr(1, 4) - e/2)
      and all(Fr(1, 4) <= Fr(1, 4) + e/2 <= Fr(5, 8) for e in aff(lambda e: e))
      and all(-e >= Fr('-0.01') and 2 + 3*e <= 3 for e in aff(lambda e: e)))

print('\n=== crossing points (Abstract, Section subsec:results, subsec:literature, Conclusion, Appendix) ===')
def bw_diff(L):
    return A(Fr('0.09783'))*L + A(Fr('0.7214'))*L.log() + A(Fr('10.6')) - (A(Fr('0.10076'))*L + A(Fr('0.24460'))*L.log() + A(Fr('7.20844')))
def yang(L):
    return A(Fr('0.11'))*L + A(Fr('0.29'))*L.log() + A(Fr('2.29')) - (A(Fr('0.09783'))*L + A(Fr('0.7214'))*L.log() + A(Fr('10.7')))
def bisect(f, lo, hi, n=200):
    lo, hi = A(lo), A(hi); assert f(lo) > 0 and f(hi) < 0
    for _ in range(n):
        mid = (lo + hi)/2; v = f(mid)
        if v > 0: lo = mid
        elif v < 0: hi = mid
        else: break
    return arb((lo + hi)/2, ((hi - lo)/2).upper())     # ball containing the root
xBW = bisect(bw_diff, 2000, 3000)
xY = bisect(lambda L: -yang(L), 900, 1000)
show('crossing with Bellotti-Wong, log T', xBW); show('crossing with Yang (4.29), log t', xY)
# the sign structure on [1, oo) (ours > BW below the root, < BW above it) is certified in constants_arb.py
if trunc_ok(xBW, '2425.8386'):
    check(314, 'crossing log T = 2425.8386... (abstract, lines 314, 409, 1628)', True)
else:
    check_fails(314, "'log T > 2425.8386...' (lines 314, 409, 1628) read as truncated digits: the crossing is 2425.83858..., "
                "i.e. 2425.8385... (2425.8386 is a rounding up; 'smaller only/exactly for log T > 2425.8386' is false on (2425.83858..., 2425.8386])",
                trunc_fails(xBW, '2425.8386'), xBW)
check(314, 'the crossing lies in (2425.8385, 2425.8386) (rounded to 4 decimals: 2425.8386)', gt(xBW, Fr('2425.8385')) and lt(xBW, Fr('2425.8386')))
check_fails(330, "'the complete estimate improves upon theirs only for log T > 2425.84' (also line 1622): the crossing is "
            "2425.83858... < 2425.84, so (1.7) is already smaller on (2425.83858..., 2425.84]; a correct 'only for' threshold "
            "must be <= the crossing, e.g. 2425.83 or 2425.8385", bool(xBW < A(Fr('2425.84'))), xBW)
check(1622, "(eq:explicit_N) smaller than Yang (4.29) 'as soon as log t > 933.5' (933.5 above the crossing; +0.2/t0 only helps)",
      bool(xY < A(Fr('933.5'))))
if trunc_ok(xY, '933.47'):
    check(1628, 'crossing log t = 933.47...', True)
else:
    check_fails(1628, "'crossing point log t = 933.47...' read as truncated digits: the value is 933.4679..., i.e. 933.46... (933.47 is a rounding)",
                trunc_fails(xY, '933.47'), xY)

print('\n=== Table tab:records and Section subsec:literature: conversions and rounding direction (upper bounds) ===')
# (stated table entry, value from the source) ; an upper bound may only be rounded UP
conv = [('492 vM A1', '0.4320', Fr('0.43200')), ('492 vM A2', '1.9167', Fr('1.91662')), ('492 vM A3', '13.0788', Fr('13.07873')),
        ('493 Grossmann A1', '0.2907', Fr('0.29062')), ('493 Grossmann A2', '1.7862', Fr('1.7862')),
        ('493 Grossmann A3', '7.0120', Fr('6.13695') + Fr(7, 8)), ('494 Backlund A3', '5.2250', Fr('4.350') + Fr(7, 8)),
        ('496 Trudgian 2012 A3', '2.8730', Fr('1.998') + Fr(7, 8)), ('500 BW A3', '8.08344', Fr('7.20844') + Fr(7, 8)),
        ('501 this work A3', '11.55', Fr('10.6') + Fr(7, 8) + Fr('0.07'))]
for lab, stated, src in conv:
    check(int(lab.split()[0]), 'table %s: stated %s >= source value %s (correct rounding direction)' % (lab, stated, src), Fr(stated) >= src)
check(504, '10.6 + 7/8 + 0.07 = 11.545 < 11.55', Fr('10.6') + Fr(7, 8) + Fr('0.07') == Fr('11.545') < Fr('11.55'))
check(508, '8.08344 - 7.20844 = 7/8', Fr('8.08344') - Fr('7.20844') == Fr(7, 8))
check(510, 'N-bound from BW Cor 1.5 and |varpi|/pi < 0.07: 7.20844 + 0.07 <= 7.28', Fr('7.20844') + Fr('0.07') <= Fr('7.28'))
check(525, 'reduction 0.10076 - 0.09783 = 0.00293; previous step 0.1038 - 0.10076 = 0.00304', Fr('0.10076') - Fr('0.09783') == Fr('0.00293') and Fr('0.1038') - Fr('0.10076') == Fr('0.00304'))
check(405, '0.09783 is the smallest A_1 in Table tab:records', all(Fr('0.09783') < Fr(x) for x in ['0.4320','0.2907','0.1370','0.1700','0.1120','0.1100','0.1038','0.10076']))
check(978, '(eq:explicit_N): 10.6 + 0.07 <= 10.7', Fr('10.6') + Fr('0.07') <= Fr('10.7'))
check(416, 'Corollary cor:distance(b): 10.2 = 10.7 - 1/2', Fr('10.7') - Fr(1, 2) == Fr('10.2'))

print('\n=== polynomial and rational identities (Section sec:meansquare, Theorem thm:recovered_simple_certificate, Fujii parameters) ===')
def poly_id(f, g, deg, pts=None):
    pts = pts or [Fr(i, 3) for i in range(deg + 1)]
    return len(set(pts)) >= deg + 1 and all(f(x) == g(x) for x in pts)
check(1204, 'Psi_1(u) = ((1/2+u)^3 + (1/2-u)^3)/3 = u^2 + 1/12 (cubic identity, 4 exact points)',
      poly_id(lambda u: ((Fr(1,2) + u)**3 + (Fr(1,2) - u)**3)/3, lambda u: u*u + Fr(1, 12), 3))
from math import comb
check(1201, 'Psi_j(u) = u^{2j} + sum_{l<j} C(2j+1,2l) 4^{l-j}/(2j+1) u^{2l}, j = 1..8 (degree 2j+1 identities, exact points)',
      all(poly_id(lambda u, j=j: ((Fr(1,2) + u)**(2*j+1) + (Fr(1,2) - u)**(2*j+1))/(2*j+1),
                  lambda u, j=j: u**(2*j) + sum(Fr(comb(2*j+1, 2*l)) * Fr(4)**(l-j) / (2*j+1) * u**(2*l) for l in range(j)), 2*j+1)
          for j in range(1, 9)))
check(1228, '1/12 = int_{-1/2}^{1/2} x^2 dx (antiderivative x^3/3, exact)', (Fr(1,2)**3 - (-Fr(1,2))**3)/3 == Fr(1, 12))
check(1547, 'sum_{i<m} (i-(m-1)/2)^2 = m(m^2-1)/12 (cubic identity in m, checked at m = 1..6; both sides polynomial in m via Faulhaber)',
      all(sum((i - Fr(m - 1, 2))**2 for i in range(m)) == Fr(m*(m*m - 1), 12) for m in range(1, 7)))
check(1549, '(m^2-1)/3 >= 1 for m >= 2 (increasing; m = 2 gives 1)', Fr(2*2 - 1, 3) == 1)
check(1140, 'Fujii parameters: alpha=1/5, k=2: 1/2+alpha = 7/10, alpha/(20k) = 1/200 <= 1/2; line 549: alpha=1/2, k=1: 1/40',
      Fr(1,2) + Fr(1,5) == Fr(7,10) and Fr(1,5)/40 == Fr(1,200) <= Fr(1,2) and Fr(1,2)/20 == Fr(1,40))
check(1316, 'Selberg constant (2k)!/(k!(2pi)^{2k}) at k=1 is 1/(2pi^2), and 4pi^2 * 1/(2pi^2) = 2 (eq:meansquare)',
      tiny(A(2)/(2*PI)**2 - 1/(2*PI**2)) and tiny(4*PI**2/(2*PI**2) - 2))

nf = sum(1 for r in RESULTS if r[2] == 'FAILS'); nc = sum(1 for r in RESULTS if r[2] == 'CERTIFIED')
print('\nSUMMARY: %d checks certified, %d claims certified to FAIL' % (nc, nf))
for r in RESULTS:
    if r[2] == 'FAILS': print('  FAILS: line', r[0], ':', r[1])
print('all checks done')
