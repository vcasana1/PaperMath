"""Figure 1 of the note: Ramsey contrast of a thermal mode and the sharp bound for its geometric visibility.

Python 3 with numpy, mpmath, matplotlib.  Run:  python3 fig_bound_v1.py
Output: fig_bound.png, fig_bound_v1_output.txt.
"""
import numpy as np
import mpmath as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 12, 'axes.labelsize': 13, 'legend.fontsize': 10.5})
mp.mp.dps = 25


def c1(m):
    """c_m(1) = int_1^inf cos(2 pi m u) u^-2 du = 1 + 2 pi m (Si(2 pi m) - pi/2)."""
    x = 2 * mp.pi * m
    return 1 + x * (mp.si(x) - mp.pi / 2)


def ratio(nbar):
    """V_1/p0 = exp(sum_m q^m c_m(1)/m)."""
    q = mp.mpf(nbar) / (mp.mpf(nbar) + 1)
    return mp.e ** mp.nsum(lambda m: q ** m * c1(m) / m, [1, mp.inf])


top = mp.e ** mp.nsum(lambda m: c1(m) / m, [1, mp.inf])          # exp(C_g)/2
s1 = mp.pi ** 2 / 12 - mp.mpf(3) / 4
nb = np.logspace(-2, 3, 61)
r = np.array([float(ratio(x)) for x in nb])
hot = np.array([float(top * (mp.mpf(x) / (x + 1)) ** s1) for x in nb])

fig, axs = plt.subplots(1, 2, figsize=(12, 4.6))
u = np.linspace(0, 3, 3001)
for n, col in [(0.1, 'tab:blue'), (1.0, 'tab:orange'), (5.0, 'tab:green')]:
    axs[0].plot(u, 1 / np.sqrt(1 + 4 * n * (n + 1) * np.sin(np.pi * u) ** 2), color=col, lw=1.8, label='mean occupation %g' % n)
axs[0].axvspan(1, 3, color='0.92', zorder=0)
axs[0].set_xlabel('reduced delay u'); axs[0].set_ylabel('contrast V(u)')
axs[0].set_xticks([0, 1, 2, 3]); axs[0].set_ylim(0, 1.05); axs[0].set_xlim(0, 3)
axs[0].legend(loc='lower center', bbox_to_anchor=(0.5, 1.01), ncol=3, frameon=False, columnspacing=1.2, handlelength=1.6)

axs[1].semilogx(nb, r, color='tab:red', lw=2.2, label='geometric visibility / vacuum probability')
axs[1].semilogx(nb[nb >= 0.6], hot[nb >= 0.6], 'k--', lw=1.3, label='hot expansion without remainder')
axs[1].axhline(1.0, color='0.35', lw=1.0, ls=':')
axs[1].axhline(float(top), color='0.35', lw=1.0, ls=':')
axs[1].text(0.012, float(top) + 0.0012, 'exp(C_g)/2 = %.5f' % float(top), fontsize=11)
axs[1].text(0.012, 0.9966, 'lower bound 1', fontsize=11)
axs[1].set_xlabel('mean occupation'); axs[1].set_ylabel('ratio')
axs[1].set_ylim(0.995, 1.060); axs[1].set_yticks([1.00, 1.01, 1.02, 1.03, 1.04, 1.05])
axs[1].legend(loc='lower center', bbox_to_anchor=(0.5, 1.01), ncol=2, frameon=False, columnspacing=1.2, handlelength=1.6)
fig.tight_layout(); fig.savefig('fig_bound.png', dpi=200)
with open('fig_bound_v1_output.txt', 'w') as f:
    f.write('exp(C_g)/2 = %s\n' % mp.nstr(top, 15))
    f.write('mean occupation, ratio V_1/p0, hot expansion without remainder\n')
    for a, b, cc in zip(nb, r, hot):
        f.write('%.6e  %.10f  %.10f\n' % (a, b, cc))
print('wrote fig_bound.png; exp(C_g)/2 =', mp.nstr(top, 15), '; ratio range', r.min(), r.max())
