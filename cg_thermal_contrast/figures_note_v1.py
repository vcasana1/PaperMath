"""Figures of G and A for the note on C_g (version 1 of this script).

Python 3 with numpy, scipy, mpmath, matplotlib.  Run:  python3 figures_note_v1.py
G and A are evaluated with cp_eval.py.  Input: zeros_G.txt, zeros_A.txt.
Output: fig_G_real.png, fig_G_surface.png, fig_A_surface.png, fig_A_real_surface.png, fig_zero_map.png,
        figures_note_v1_output.txt.
The surfaces show |F| on a linear vertical axis that is inverted (0 at the top), so that a zero of F is a peak.
Each red marker uses the computed modulus at its mesh vertex.
"""
import time
import numpy as np
import mpmath as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patheffects import Normal, Stroke
import cp_eval as E

plt.rcParams.update({'font.size': 12, 'axes.labelsize': 13, 'legend.fontsize': 11})
out = open('figures_note_v1_output.txt', 'w')


def log(s=''):
    print(s, flush=True)
    out.write(s + '\n')


# ---------------------------------------------------------------- data
zg = np.loadtxt('zeros_G.txt')
zG = zg[:, 0] + 1j * zg[:, 1]
zG40 = zG[zG.imag <= 40]
mp.mp.dps = 20
zD = np.array([0.5 + 1j * float(mp.zetazero(k).imag) for k in range(1, 7)])      # points 1/2 + i t
log('zeros of G with Im s <= 40: ' + '  '.join('%.6f+%.6fi' % (z.real, z.imag) for z in zG40))
log('points 1/2 + i t with G = A: t = ' + '  '.join('%.6f' % z.imag for z in zD))

OFF_S = np.array([-0.018, -0.009, -0.003, -0.001, 0.0, 0.001, 0.003, 0.009, 0.018])
OFF_T = 12 * OFF_S
pts = np.concatenate([zG40, zD])
sig = np.concatenate([np.round(np.arange(0.05, 1.9501, 0.01), 2)] + [z.real + OFF_S for z in pts])
sig = np.unique(sig[(sig >= 0.05) & (sig <= 1.95)])
t_grid = np.concatenate([np.round(np.arange(1.0, 40.0001, 0.05), 2)] + [z.imag + OFF_T for z in pts])
tt = np.unique(t_grid[(t_grid >= 1.0) & (t_grid <= 40.0)])
S, T = np.meshgrid(sig, tt)
t0 = time.time()
Gv = E.G_grid(sig, tt)
Av = E.A(S + 1j * T)
log('grid: %d (Re s) x %d (Im s) points, %.0f s' % (len(sig), len(tt), time.time() - t0))
k = np.unravel_index(np.abs(Av).argmin(), Av.shape)
log('min |A| on the grid = %.6f at s = %.2f + %.2f i;  max |A| = %.4f' % (np.abs(Av).min(), sig[k[1]], tt[k[0]], np.abs(Av).max()))
log('max |G| on the grid = %.4f' % np.abs(Gv).max())
log('|G - A| at the six points 1/2 + i t: ' + ' '.join('%.1e' % v for v in np.abs(E.G(zD) - E.A(zD))))
log('|G| at the six zeros of G: ' + ' '.join('%.1e' % v for v in np.abs(E.G(zG40))))


def surface(V, fname, zlabel, marks, marklabel, Sg, Tg, xticks, yticks, zticks, elev, azim, top=None,
            figsize=(10, 7.6), aspect=(1.0, 1.55, 0.62), xlabel='Re s', ylabel='Im s', xpad=16, ypad=26):
    Zs = np.abs(V)
    if top is not None:
        Zs = np.minimum(Zs, top)
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0.0, 0.02, 0.92, 0.98], projection='3d', computed_zorder=False)
    ax.plot_surface(Sg, Tg, Zs, cmap='viridis_r', zorder=1, linewidth=0, antialiased=False,
                    rcount=Sg.shape[0], ccount=Sg.shape[1])
    if len(marks):
        columns = np.searchsorted(Sg[0], marks.real)
        rows = np.searchsorted(Tg[:, 0], marks.imag)
        if not (np.array_equal(Sg[rows, columns], marks.real) and np.array_equal(Tg[rows, columns], marks.imag)):
            raise ValueError(fname + ': each marked zero must be a mesh vertex')
        ax.scatter(marks.real, marks.imag, Zs[rows, columns], color='#d21d2c', edgecolor='white', linewidth=0.6,
                   s=55, depthshade=False, label=marklabel, zorder=10)
        ax.legend(loc='upper left', bbox_to_anchor=(0.04, 0.95), frameon=True)
        log('%s: %d marked mesh vertices, largest plotted marker height %.3e' % (fname, len(marks), Zs[rows, columns].max()))
    else:
        log('wrote %s' % fname)
    ax.set_xticks(xticks); ax.set_yticks(yticks); ax.set_zticks(zticks)
    ax.tick_params(axis='x', pad=2); ax.tick_params(axis='y', pad=4); ax.tick_params(axis='z', pad=8)
    ax.set_xlabel(xlabel, labelpad=xpad); ax.set_ylabel(ylabel, labelpad=ypad); ax.set_zlabel(zlabel, labelpad=16)
    ax.set_zlim(0, max(zticks[-1], Zs.max())); ax.invert_zaxis()
    ax.set_box_aspect(aspect)
    ax.view_init(elev=elev, azim=azim)
    fig.savefig(fname, dpi=200)


none = np.array([], complex)
surface(Gv, 'fig_G_surface.png', '|G(s)|', zG40, 'computed zeros of G', S, T,
        [0.5, 1.0, 1.5], [10, 20, 30, 40], [0.0, 0.2, 0.4], elev=38, azim=-52)
surface(Av, 'fig_A_surface.png', '|A(s)|', none, '', S, T,
        [0.5, 1.0, 1.5], [10, 20, 30, 40], [0.0, 1.0, 2.0], elev=38, azim=-52)

# ---------------------------------------------------------------- A near the real axis
zA_all = np.loadtxt('zeros_A.txt')[:, 0]
zA = zA_all[(zA_all > -3.5) & (zA_all < 9.5)]
OFF_A = np.array([-0.03, -0.015, -0.006, -0.002, 0.0, 0.002, 0.006, 0.015, 0.03])
sa = np.unique(np.concatenate([np.arange(-3.495, 9.5, 0.01)] + [z + OFF_A for z in zA]))
ta = np.unique(np.concatenate([np.round(np.arange(-2.0, 2.0001, 0.01), 2), OFF_A]))
Sa, Ta = np.meshgrid(sa, ta)
Aa = E.A(Sa + 1j * Ta)
log('A near the real axis: %d x %d points; real zeros shown: %s' % (len(sa), len(ta), ' '.join('%.4f' % v for v in zA)))
surface(Aa, 'fig_A_real_surface.png', '|A(s)|', zA.astype(complex), 'computed real zeros of A', Sa, Ta,
        [-2, 0, 2, 4, 6, 8], [-2, 0, 2], [0.0, 0.5, 1.0, 1.5], elev=40, azim=-72, top=1.5,
        figsize=(11, 6.6), aspect=(2.2, 1.0, 0.6), xpad=22, ypad=14)

# ---------------------------------------------------------------- G on the real axis
sr = np.linspace(-1.9, 3.0, 99)
Gr = E.G_grid(sr, [0.0])[0].real
G1 = E.G_grid([1.0], [0.0])[0, 0].real
log('G(1) = %.12f,  C_g = log 2 - G(1) = %.12f,  exp(-G(1)) = %.10f' % (G1, np.log(2) - G1, np.exp(-G1)))
fig, ax = plt.subplots(figsize=(8, 4.6))
ax.plot(sr, Gr, lw=2)
ax.axhline(0, color='k', lw=0.6)
ax.plot([-1], [0], 'o', color='tab:red', ms=8, label='zero at s = -1')
ax.plot([1], [G1], 's', color='tab:green', ms=8, label='G(1) = log 2 - C_g')
ax.set_xlabel('s (real)'); ax.set_ylabel('G(s)'); ax.legend(loc='upper right')
ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig('fig_G_real.png', dpi=200)
log('wrote fig_G_real.png')

# ---------------------------------------------------------------- zero map
Psi = Gv / Av
fig, ax = plt.subplots(figsize=(6.4, 9))
background = LinearSegmentedColormap.from_list('light_gray', ['#ffffff', '#d2d9e3'])
log_modulus = np.log10(np.maximum(np.abs(Gv), np.finfo(float).tiny))
pc = ax.pcolormesh(S, T, log_modulus, cmap=background, shading='auto')
cb = fig.colorbar(pc, ax=ax, pad=0.03)
cb.set_label('log10 |G(s)|')
arc_color = '#0055ae'
arcs = ax.contour(S, T, np.where((Psi.real > 0) & (Psi.real < 1), Psi.imag, np.nan), levels=[0], colors=[arc_color], linewidths=2.0)
arcs.set_path_effects([Stroke(linewidth=3.6, foreground='white'), Normal()])
ax.plot(zG40.real, zG40.imag, 'o', color='tab:red', ms=8, label='zeros of G')
ax.plot(zD.real, zD.imag, 'x', color='tab:green', ms=10, mew=2.5, label='points with G = A')
ax.plot([], [], color=arc_color, linewidth=2.0, label='Im(G/A) = 0, 0 < Re(G/A) < 1')
ax.set_xticks([0.5, 1.0, 1.5]); ax.set_yticks([5, 10, 15, 20, 25, 30, 35, 40])
ax.set_xlabel('Re s'); ax.set_ylabel('Im s'); ax.legend(loc='lower right', fontsize=10)
fig.tight_layout(); fig.savefig('fig_zero_map.png', dpi=200)
log('wrote fig_zero_map.png')
out.close()
