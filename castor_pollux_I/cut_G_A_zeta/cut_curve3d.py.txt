#!/usr/bin/env python3
# Castor and Pollux I: data for the 3D view. Surfaces |G|, |A|, |zeta| on 0.05<=sigma<=0.95, 10<=t<=60;
# the curve where the surfaces |G| and |A| cut (|G| = |A|), lifted to the height |G|; the points s = 1/2 + i gamma_k.
import sys, json, time
sys.path.insert(0, '/home/claude/v3work')
import numpy as np, mpmath as mp, contourpy
from cp_eval import G_grid, A
t0 = time.time(); out = open('cut_curve3d_output.txt', 'w')
def log(s): print(s, flush=True); out.write(s + '\n')
SS = np.round(np.arange(0.05, 0.9501, 0.01), 2); TT = np.round(np.arange(10.0, 60.0001, 0.05), 2)
g = G_grid(SS, TT); a = A(SS[None, :] + 1j * TT[:, None])
F = np.abs(g) - np.abs(a)
gen = contourpy.contour_generator(SS, TT, F)
lines = gen.lines(0.0)
from scipy.interpolate import RegularGridInterpolator
Gi = RegularGridInterpolator((TT, SS), np.abs(g), bounds_error=False, fill_value=None)
curves = []
for L in lines:
    if len(L) < 3: continue
    z = Gi(np.c_[L[:, 1], L[:, 0]])
    curves.append([[round(float(x), 4) for x in L[:, 0]], [round(float(y), 3) for y in L[:, 1]], [round(float(v), 4) for v in z]])
log('|G| = |A| curve: %d pieces, %d points' % (len(curves), sum(len(c[0]) for c in curves)))
# surfaces on a coarser grid
SC = SS[::2]; TC = TT[::2]
gc = np.abs(g[::2, ::2]); ac = np.abs(a[::2, ::2])
mp.mp.dps = 15
zc = np.array([[abs(complex(mp.zeta(mp.mpc(float(sg), float(tt))))) for sg in SC] for tt in TC])
zeros = [float(mp.im(mp.zetazero(k))) for k in range(1, 15) if mp.im(mp.zetazero(k)) <= 60]
pts = []
for gm in zeros:
    gv = abs(G_grid([0.5], [gm])[0, 0]); dist = min(np.hypot(np.array(c[0]) - 0.5, np.array(c[1]) - gm).min() for c in curves)
    pts.append([gm, round(float(gv), 5)]); log('gamma=%.6f |G|=|A|=%.5f distance to the computed curve %.4f' % (gm, gv, dist))
r = lambda M: [[round(float(v), 4) for v in row] for row in M]
json.dump(dict(s=[float(x) for x in SC], t=[float(x) for x in TC], G=r(gc), A=r(ac), Z=r(zc), curves=curves, pts=pts),
          open('cut_curve3d.json', 'w'), separators=(',', ':'))
log('surfaces %d x %d; time %.1f s' % (len(SC), len(TC), time.time() - t0))
