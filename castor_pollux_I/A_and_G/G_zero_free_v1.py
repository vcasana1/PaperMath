#!/usr/bin/env python3
# Castor and Pollux I -- G_zero_free_v1
# Zero-free criterion for G from its own singular structure (one-sided singularity of h at u = 1,
# two-sided singularities at u = n >= 2):  for sigma > 1
#     G(s) = B(s) + C(s) D(s),   B = A + C,   C = (pi/s) cot(pi s/2),   D(s) = sum_{n>=2} n^{-s},
# hence  G(s) != 0  whenever  d(sigma) := sum_{n>=2} n^{-sigma} < |B(s)/C(s)|.
# This script computes, for 10 <= t <= 300, the abscissa
#     sigma_G(t) = inf{ s0 > 1 : d(sigma) < |B/C|(sigma+it) for all sigma in [s0, 8] }
# and compares it with the zeros of G (zeros_G.txt and zeros_G_200_300_v1.txt) and with 1 + pi/l(t),
# l(t) = log(t/2pi) + gamma.
# Usage: python3 G_zero_free_v1.py <castor_pollux_I dir> <zeros_G_200_300_v1.txt>
import sys, numpy as np, mpmath as mp
sys.path.insert(0, sys.argv[1])
from cp_eval import A
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

out = open('G_zero_free_v1_output.txt', 'w')
def log(x):
    print(x, flush=True); out.write(x + '\n')

sg = np.round(np.arange(1.001, 8.0, 0.001), 4)
d = np.array([float(mp.zeta(x) - 1) for x in sg])
ts = np.arange(10.0, 300.0 + 1e-9, 0.25)
sigG = []
for t in ts:
    s = sg + 1j * t
    C = (np.pi / s) / np.tan(np.pi * s / 2)
    ratio = np.abs((A(s) + C) / C)
    ok = d < ratio
    # last index where the criterion fails; sigma_G just above it
    bad = np.where(~ok)[0]
    sigG.append(sg[bad[-1] + 1] if len(bad) else sg[0])
sigG = np.array(sigG)
zg = np.r_[np.loadtxt(sys.argv[1] + '/zeros_G.txt')[:, :2], np.loadtxt(sys.argv[2])[:, :2]]
x, y = zg[:, 0], zg[:, 1]
m = (y >= 10) & (y <= 300)
sG_at = np.interp(y[m], ts, sigG)
log('zero-free abscissa sigma_G(t) for 10 <= t <= 300 (criterion d(sigma) < |B/C|):')
for t0 in [10, 15, 25, 50, 100, 150, 200, 250, 300]:
    i = np.argmin(abs(ts - t0))
    l = np.log(t0 / (2 * np.pi)) + np.euler_gamma
    log('  t = %5.0f   sigma_G = %.3f    1 + pi/l(t) = %.3f' % (t0, sigG[i], 1 + np.pi / l))
log('zeros of G with 10 <= t <= 300: %d;  all satisfy Re z < sigma_G(Im z): %s;  smallest gap sigma_G - Re z = %.3f (at %.4f%+.4fi)'
    % (m.sum(), bool(np.all(x[m] < sG_at)), (sG_at - x[m]).min(), x[m][np.argmin(sG_at - x[m])], y[m][np.argmin(sG_at - x[m])]))
log('max Re of zeros of G: %.4f' % x[m].max())

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(ts, sigG, color='k', lw=1.2, label='sigma_G(t): G has no zeros to the right (proved criterion)')
l = np.log(ts / (2 * np.pi)) + np.euler_gamma
ax.plot(ts, 1 + np.pi / l, '--', color='gray', label='1 + pi / (log(t/2pi) + gamma)')
ax.scatter(y[m], x[m], marker='x', color='blue', s=18, label='zeros of G (Re vs Im)')
ax.axhline(0.5, color='red', lw=0.6, ls=':')
ax.set_xlabel('t = Im s'); ax.set_ylabel('sigma = Re s')
ax.set_title('Zero-free region of G from its own singular structure')
ax.legend(fontsize=8); fig.tight_layout(); fig.savefig('fig_G_zero_free_v1.png', dpi=150)
