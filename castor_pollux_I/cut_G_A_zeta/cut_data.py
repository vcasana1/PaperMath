#!/usr/bin/env python3
# Castor and Pollux I: data for the HTML chart "Where G, A and zeta meet".
# G from cp_eval (kernel K only), A from cp_eval (digamma + partial fractions), zeta from mpmath (independent).
# Lines: G and A (real and imaginary parts), |G-A|, |zeta| on Re s = sigma, 1 <= t <= 60, step 0.02, for 17 values of sigma.
# Map: log10 |G-A| on 0.05 <= sigma <= 0.95 (step 0.01), 1 <= t <= 60 (step 0.1).
import sys, json, time
sys.path.insert(0, '/home/claude/v3work')
import numpy as np, mpmath as mp
from cp_eval import G_grid, A
t0 = time.time()
out = open('cut_data_output.txt', 'w')
def log(s): print(s, flush=True); out.write(s + '\n')
SIG = [round(0.1 + 0.05 * j, 2) for j in range(17)]          # 0.10 .. 0.90
T = np.round(np.arange(1.0, 60.0001, 0.02), 2)
g = G_grid(SIG, T)                                            # (nt, nsig)
S = np.array(SIG)[None, :] + 1j * T[:, None]
a = A(S)
mp.mp.dps = 15
z = np.array([[complex(mp.zeta(mp.mpc(sg, tt))) for sg in SIG] for tt in T])
ident = np.pi / S / np.tan(np.pi * S / 2) * z                 # (pi/s) cot(pi s/2) zeta(s)
log('lines: %d sigma x %d t; max |G-A-(pi/s)cot(pi s/2)zeta| = %.2e' % (len(SIG), len(T), np.abs(g - a - ident).max()))
zeros = [float(mp.im(mp.zetazero(k))) for k in range(1, 17)]
rows = []
for k, gm in enumerate(zeros, 1):
    s = complex(0.5, gm)
    gv = G_grid([0.5], [gm])[0, 0]; av = A(np.array([s]))[0]
    rows.append([k, gm, gv.real, gv.imag, av.real, av.imag, abs(gv - av), abs(complex(mp.zeta(s)))])
    log('k=%2d gamma=%.6f  G=%.6f%+.6fi  A=%.6f%+.6fi  |G-A|=%.1e |zeta|=%.1e' % tuple(rows[-1]))
SM = np.round(np.arange(0.05, 0.9501, 0.01), 2)
TM = np.round(np.arange(1.0, 60.0001, 0.1), 1)
gm_ = G_grid(SM, TM); am_ = A(SM[None, :] + 1j * TM[:, None])
L = np.log10(np.abs(gm_ - am_))
log('map: %d sigma x %d t; log10|G-A| from %.2f to %.2f' % (len(SM), len(TM), L.min(), L.max()))
r4 = lambda v: [float('%.4g' % x) for x in v]
data = dict(sig=SIG, t=[float(x) for x in T],
            Gr={str(s): r4(g[:, j].real) for j, s in enumerate(SIG)},
            Gi={str(s): r4(g[:, j].imag) for j, s in enumerate(SIG)},
            Ar={str(s): r4(a[:, j].real) for j, s in enumerate(SIG)},
            Ai={str(s): r4(a[:, j].imag) for j, s in enumerate(SIG)},
            D={str(s): r4(np.abs(g[:, j] - a[:, j])) for j, s in enumerate(SIG)},
            Z={str(s): r4(np.abs(z[:, j])) for j, s in enumerate(SIG)},
            zeros=zeros, rows=rows, msig=[float(x) for x in SM], mt=[float(x) for x in TM],
            map=[[round(float(v), 2) for v in row] for row in L])
json.dump(data, open('cut_data.json', 'w'), separators=(',', ':'))
log('time %.1f s' % (time.time() - t0))
