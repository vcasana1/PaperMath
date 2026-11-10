# Castor-Pollux I v3: surfaces on a fine grid (all labels in English).
# The surfaces show -log10|F(s)| on the vertical axis, so that a zero of F is a peak.  The grid is a tensor grid that
# contains the real and imaginary parts of the zeros as grid lines; values are clipped at CLIP.
# G and A are evaluated with cp_eval.py (kernel K only; no zeta function).  zeta is used only for its own figure,
# for the six points 1/2 + i t and for the check of the grid relation.
import time
import numpy as np
import mpmath as mp
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cp_eval as E

CLIP = 6.0
out = open('figures_v3_output.txt', 'w')


def log(s=''):
    print(s, flush=True)
    out.write(s + '\n')


def zeta_grid(sig, t):
    try:
        from flint import acb, ctx
        ctx.prec = 64
        f = lambda a, b: complex(acb(a, b).zeta())
    except ImportError:
        f = lambda a, b: complex(mp.zeta(mp.mpc(a, b)))
    return np.array([[f(float(a), float(b)) for a in sig] for b in t])


# ---------------------------------------------------------------- data
zg = np.loadtxt('zeros_G.txt')
zG = zg[:, 0] + 1j * zg[:, 1]
zG40 = zG[zG.imag <= 40]
mp.mp.dps = 20
zD = np.array([0.5 + 1j * float(mp.zetazero(k).imag) for k in range(1, 7)])      # points 1/2 + i t
log('zeros of G with Im s <= 40: %d;  points 1/2 + i t: %d' % (len(zG40), len(zD)))

# local refinement: grid lines through every zero and at these distances from it, so that each peak is resolved
OFF_S = np.array([-0.006, -0.003, -0.0015, -0.0005, 0.0, 0.0005, 0.0015, 0.003, 0.006])
OFF_T = 5 * OFF_S
pts = np.concatenate([zG40, zD])
sig = np.concatenate([np.round(np.arange(0.05, 1.9501, 0.01), 2)] + [z.real + OFF_S for z in pts])
sig = np.unique(sig[(sig >= 0.05) & (sig <= 1.95)])
tt = np.unique(np.concatenate([np.round(np.arange(1.0, 40.0001, 0.05), 2)] + [z.imag + OFF_T for z in pts]))
S, T = np.meshgrid(sig, tt)
t0 = time.time()
Gv = E.G_grid(sig, tt)
Av = E.A(S + 1j * T)
Zv = zeta_grid(sig, tt)
log('fine grid: %d (Re s) x %d (Im s) points, %.0f s' % (len(sig), len(tt), time.time() - t0))
sc = S + 1j * T
chk = np.abs(Gv - Av - (np.pi / sc) / np.tan(np.pi * sc / 2) * Zv).max()
log('max |G - A - (pi/s) cot(pi s/2) zeta| on the fine grid = %.3e' % chk)
k = np.unravel_index(np.abs(Av).argmin(), Av.shape)
log('min |A| on the fine grid = %.6f at s = %.2f + %.2f i;  max |A| = %.4f' % (np.abs(Av).min(), sig[k[1]], tt[k[0]], np.abs(Av).max()))
gd = np.abs(E.G(zD) - E.A(zD))
log('|G - A| at the six points 1/2 + i t: ' + ' '.join('%.1e' % v for v in gd))
log('|G| at the six zeros of G (double precision evaluator): ' + ' '.join('%.1e' % v for v in np.abs(E.G(zG40))))
np.savez_compressed('grid_values_v3.npz', sigma=sig, t=tt, G=Gv, A=Av, zeta=Zv)


def surface(V, title, fname, zlabel, marks, marklabel, Sg=S, Tg=T, elev=32, azim=-62, lo=None, figsize=(9, 7)):
    """-log10|F| is the vertical axis, so a zero of F is a peak."""
    Zs = -np.log10(np.abs(V) + 1e-300)
    Zs = np.clip(Zs, lo, CLIP)
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(Sg, Tg, Zs, cmap='viridis', linewidth=0, antialiased=False, rcount=Sg.shape[0], ccount=Sg.shape[1])
    if len(marks):
        # the section of the surface along Im s through each zero, drawn as a line so that the thin peak is visible
        sv, tv = Sg[0], Tg[:, 0]
        for z in marks:
            j = np.argmin(np.abs(sv - z.real))
            m = np.abs(tv - z.imag) <= 0.6
            ax.plot(np.full(m.sum(), sv[j]), tv[m], Zs[m, j], color='gold', lw=0.9, zorder=5)
        ax.scatter(marks.real, marks.imag, np.full(len(marks), CLIP), color='red', s=22, depthshade=False, label=marklabel, zorder=6)
        ax.legend(loc='upper left', fontsize=9)
    ax.set_xlabel('Re s'); ax.set_ylabel('Im s'); ax.set_zlabel(zlabel); ax.set_title(title, fontsize=10)
    ax.view_init(elev=elev, azim=azim)
    fig.tight_layout(); fig.savefig(fname, dpi=200); plt.close(fig)
    log('wrote %s' % fname)


none = np.array([], complex)
surface(Gv, 'G(s): the zeros are the peaks of -log10 |G(s)| (clipped at %g)' % CLIP, 'fig_G_surface.png', '-log10 |G(s)|', zG40, 'zeros of G')
surface(Av, 'A(s) on the same rectangle: no zero of A here', 'fig_A_surface.png', '-log10 |A(s)|', none, '')
surface(Gv - Av, 'G(s) - A(s): peaks of -log10 |G(s) - A(s)| (clipped at %g)' % CLIP, 'fig_GminusA_surface.png', '-log10 |G(s) - A(s)|', zD, 'points with G = A')
surface(Zv, 'Riemann zeta function: the zeros are the peaks of -log10 |zeta(s)| (clipped at %g)' % CLIP, 'fig_zeta_surface.png', '-log10 |zeta(s)|', zD, 'zeros of zeta')

# ---------------------------------------------------------------- A near the real axis: real zeros and poles
zA_all = np.loadtxt('zeros_A.txt')[:, 0]
zA = zA_all[(zA_all > -3.5) & (zA_all < 9.5)]
OFF_A = np.array([-0.03, -0.015, -0.006, -0.002, 0.0, 0.002, 0.006, 0.015, 0.03])
sa = np.unique(np.concatenate([np.arange(-3.495, 9.5, 0.01)] + [z + OFF_A for z in zA]))
ta = np.unique(np.concatenate([np.round(np.arange(-2.0, 2.0001, 0.01), 2), OFF_A]))
Sa, Ta = np.meshgrid(sa, ta)
Aa = E.A(Sa + 1j * Ta)
log('A near the real axis: %d x %d points; real zeros shown: %s' % (len(sa), len(ta), ' '.join('%.4f' % v for v in zA)))
surface(Aa, 'A(s) near the real axis: real zeros (peaks) at -2, -1 and in (2,4), (4,6), (6,8), (8,10); poles (pits) at 0, 2, 4, 6, 8',
        'fig_A_real_surface.png', '-log10 |A(s)|', zA.astype(complex), 'real zeros of A', Sg=Sa, Tg=Ta, elev=38, azim=-75, lo=-2.0, figsize=(11, 6.5))

# ---------------------------------------------------------------- zero map on the fine grid
Psi = Gv / Av
fig, ax = plt.subplots(figsize=(6, 9))
pc = ax.pcolormesh(S, T, np.log10(np.abs(Gv)), cmap='Greys', shading='auto'); fig.colorbar(pc, ax=ax, label='log10 |G(s)|')
ax.contour(S, T, np.where((Psi.real > 0) & (Psi.real < 1), Psi.imag, np.nan), levels=[0], colors='tab:blue', linewidths=1.5)
ax.plot(zG40.real, zG40.imag, 'o', color='tab:red', label='zeros of G')
ax.plot(zD.real, zD.imag, 'x', color='tab:green', ms=9, mew=2, label='points with G = A')
ax.plot([], [], color='tab:blue', label='Im(G/A) = 0 with 0 < Re(G/A) < 1')
ax.set_xlabel('Re s'); ax.set_ylabel('Im s'); ax.set_title('Zeros of G, points with G = A, and the arcs joining them'); ax.legend(loc='lower left', fontsize=8)
fig.tight_layout(); fig.savefig('fig_zero_map.png', dpi=200); plt.close(fig)
log('wrote fig_zero_map.png')
out.close()
