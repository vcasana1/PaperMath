"""Real zeros of A on [-60, 200].

find_zeros.py shows (argument principle) that A has no zero with 0.2 <= Im s <= 200, -6 <= Re s <= 8,
and the check below extends this to -60 <= Re s <= 201, 0.001 <= Im s <= 200.  Since A(conj s) = conj A(s),
the zeros of A in that window are real.  A has poles at s = 0 and s = 2k (k >= 1).
This script brackets the sign changes of A between the poles, polishes them with mpmath, and tests
the even negative integers, where A may vanish without changing sign of the bracketing grid.
Output: zeros_A.txt (overwrites the empty file of find_zeros.py), zeros_A_check.txt
"""
import numpy as np
import mpmath as mp
from scipy.optimize import brentq
import fast
import funcs as F

mp.mp.dps = 25
fA = lambda x: fast.A(np.array([x + 0j]))[0].real

roots = []
# negative axis: grid avoiding s=0
xs = np.linspace(-60, -1e-3, 600001)
v = fast.A(xs + 0j).real
for i in np.where(np.sign(v[:-1]) != np.sign(v[1:]))[0]:
    roots.append(brentq(fA, xs[i], xs[i + 1], xtol=1e-14))
# even negative integers (double-zero test)
evens = [(n, float(abs(F.A(n)))) for n in range(-2, -61, -2)]
for n, val in evens:
    if val < 1e-15 and all(abs(n - r) > 1e-8 for r in roots):
        roots.append(float(n))
# (0,2): A is a sum of terms positive there?  scan it
xs = np.linspace(1e-4, 2 - 1e-4, 200001)
v = fast.A(xs + 0j).real
for i in np.where(np.sign(v[:-1]) != np.sign(v[1:]))[0]:
    roots.append(brentq(fA, xs[i], xs[i + 1], xtol=1e-14))
# between consecutive poles 2k and 2k+2
for k in range(1, 100):
    a, b = 2 * k + 1e-9, 2 * k + 2 - 1e-9
    if np.sign(fA(a)) != np.sign(fA(b)):
        roots.append(brentq(fA, a, b, xtol=1e-14))
roots = sorted(roots)
pol = []
for r in roots:
    z = mp.findroot(lambda s: mp.re(F.A(s)), mp.mpf(r))
    pol.append((float(z), float(abs(F.A(z)))))

with open('zeros_A.txt', 'w') as f:
    f.write('# zeros of A: all real in the window -60<=Re s<=200, 0<=Im s<=200 (see zeros_A_check.txt)\n# Re  Im  |A| at the polished zero\n')
    for z, r in pol:
        f.write('%.12f %.12f %.2e\n' % (z, 0.0, r))


def cnt(c, n=200000):
    path = np.concatenate([np.linspace(a, b, n, endpoint=False) for a, b in zip(c[:-1], c[1:])] + [np.array([c[0]])])
    ph = np.unwrap(np.angle(fast.A(path)))
    return (ph[-1] - ph[0]) / 2 / np.pi, np.abs(np.diff(ph)).max()


with open('zeros_A_check.txt', 'w') as f:
    c1 = cnt([-60 + 1e-3j, 201 + 1e-3j, 201 + 0.2j, -60 + 0.2j, -60 + 1e-3j])
    c2 = cnt([-60 + 0.2j, 201 + 0.2j, 201 + 200j, -60 + 200j, -60 + 0.2j])
    f.write('argument principle for A, -60<Re s<201, 0.001<Im s<0.2: %.6f (largest phase step %.3f)\n' % c1)
    f.write('argument principle for A, -60<Re s<201, 0.2<Im s<200:   %.6f (largest phase step %.3f)\n' % c2)
    f.write('|A(n)| at even negative integers: %s\n' % ', '.join('A(%d)=%.2e' % e for e in evens[:6]))
    f.write('number of real zeros found: %d; first ones: %s\n' % (len(pol), ', '.join('%.6f' % z for z, _ in pol[:8])))
print(open('zeros_A_check.txt').read())
