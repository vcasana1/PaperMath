#!/usr/bin/env python3
# Castor and Pollux I -- certify_ImA_v1
# Ball-arithmetic certificate (python-flint / Arb) that Im A(s) > 0 on the two compact boxes
# left open by the analytic part of the proof (t >= 5):
#   B1 = [-38.2, 2] x [5, 40.2]      (sigma <= 2, |s-2| <= 40.1)
#   B2 = [2, 8.4]   x [5, 8.4]       (sigma >= 2, |s| <= 8.33)
# A(s) = log(2pi)/s + 1/s^2 - (psi(1-s/2) + gamma)/s + sum_{k>=1} (Sigma_{2k}-1)/(k(2k-s)),
# Sigma_{2k} = sum_n n^{-2k}. The k-sum is cut at K = 60; tail <= (2/(3t)) 4^{-K}, added as a ball.
# Adaptive bisection: a box is accepted when the lower end of Im A(box) is > 0.
import sys, time
from flint import arb, acb, ctx
ctx.prec = 80
K = 60
two_pi = 2 * arb.pi()
lg2pi = two_pi.log()
eg = arb.const_euler()
zm1 = [(arb(2 * k).zeta() - 1) / k for k in range(1, K + 1)]

def ImA_box(s0, s1, t0, t1):
    sm, sr = (s0 + s1) / 2, (s1 - s0) / 2
    tm, tr = (t0 + t1) / 2, (t1 - t0) / 2
    s = acb(arb(sm, sr), arb(tm, tr))
    val = lg2pi / s + 1 / s**2 - ((1 - s / 2).digamma() + eg) / s
    for k in range(1, K + 1):
        val += zm1[k - 1] / (2 * k - s)
    tail = arb(0, 2.0 / (3 * t0) * 4.0**(-K))
    return val.imag + tail

def certify(s0, s1, t0, t1, h0=1.0, maxdepth=22):
    stack, n_ok, n_eval, worst = [], 0, 0, None
    s = s0
    while s < s1 - 1e-12:
        t = t0
        while t < t1 - 1e-12:
            stack.append((s, min(s + h0, s1), t, min(t + h0, t1), 0)); t += h0
        s += h0
    while stack:
        a, b, c, d, dep = stack.pop()
        v = ImA_box(a, b, c, d); n_eval += 1
        lo = float(v.lower())
        if lo > 0:
            n_ok += 1
            if worst is None or lo < worst[0]: worst = (lo, a, b, c, d)
            continue
        if dep >= maxdepth:
            return False, n_eval, (a, b, c, d, lo)
        ms, mt = (a + b) / 2, (c + d) / 2
        stack += [(a, ms, c, mt, dep + 1), (ms, b, c, mt, dep + 1), (a, ms, mt, d, dep + 1), (ms, b, mt, d, dep + 1)]
    return True, n_eval, worst

out = open('certify_ImA_v1_output.txt', 'w')
def log(x):
    print(x, flush=True); out.write(x + '\n')
log('python-flint %s, precision %d bits, K = %d' % (__import__('flint').__version__, ctx.prec, K))
for name, box in [('B1', (-38.2, 2.0, 5.0, 40.2)), ('B2', (2.0, 8.4, 5.0, 8.4))]:
    T0 = time.time()
    ok, ne, info = certify(*box)
    if ok:
        log('%s %s: CERTIFIED Im A > 0;  %d ball evaluations;  smallest certified lower bound %.4e on box '
            'sigma in [%.4f, %.4f], t in [%.4f, %.4f];  %.1f s' % (name, box, ne, info[0], *info[1:], time.time() - T0))
    else:
        log('%s %s: FAILED at box %s' % (name, box, info))
