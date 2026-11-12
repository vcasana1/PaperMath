#!/usr/bin/env python3
# Castor and Pollux I -- tongues_v1
# Tongues of U = {|G| < |A|}: the level curve |G| = |A| on -1 <= sigma <= 3 in two windows
#   W1: 10 <= t <= 60      W2: 268 <= t <= 300  (around the first failure of Gram's law, g_125..g_127)
# For every closed loop of the curve: winding of Q = G/A (degree), zeros of G inside, points with G = A
# (phi in 2piZ), crossings of sigma = 1/2 and their type:
#   (I)  G = A                     (phi = 0)
#   (II) G = -exp(2 i alpha(t)) A  (phi = pi + 2 alpha(t)),
#        alpha(t) = arg[(pi/s) cot(pi s/2) / A(s)] - theta(t),  s = 1/2 + i t,  theta = Riemann-Siegel theta.
# G and A from cp_eval.py (no zeta). Zeros of G for t <= 200 from zeros_G.txt (taken as given);
# for 200 < t <= 300 located here from G only. Zeros of zeta from mpmath only for comparison.
# Usage: python3 tongues_v1.py <path to castor_pollux_I>
import sys, time
import numpy as np
base = sys.argv[1]
sys.path.insert(0, base)
from cp_eval import G_grid, A
import mpmath as mp
import contourpy
from scipy.interpolate import RegularGridInterpolator
from matplotlib.path import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

T0 = time.time()
out = open('tongues_v1_output.txt', 'w')
def log(s=''):
    print(s, flush=True); out.write(s + '\n')
TWO_PI = 2 * np.pi
mp.mp.dps = 20

# ------------------------------------------------------------------ zeros of G with 200 < t <= 300
def Gpt(z):
    return G_grid([z.real], [z.imag])[0, 0]

def newton(z, it=50):
    for _ in range(it):
        h = 1e-6
        f = Gpt(z); d = (Gpt(z + h) - Gpt(z - h)) / (2 * h)
        dz = f / d; z = z - dz
        if abs(dz) < 1e-12: break
    return z, abs(Gpt(z))

S0, S1, TA, TB = -1.0, 2.5, 200.0, 300.0
log('zeros of G in %.1f <= sigma <= %.1f, %.0f < t <= %.0f' % (S0, S1, TA, TB))
ss = np.round(np.arange(S0, S1 + 1e-9, 0.025), 4); ts = np.round(np.arange(TA - 0.5, TB + 0.5 + 1e-9, 0.02), 4)
LG = np.log(np.abs(G_grid(ss, ts)) + 1e-300)
cand = []
for i in range(1, LG.shape[0] - 1):
    for j in range(1, LG.shape[1] - 1):
        if LG[i, j] <= LG[i - 1:i + 2, j - 1:j + 2].min():
            cand.append(ss[j] + 1j * ts[i])
zn = []
for c in cand:
    z, r = newton(c)
    if r < 1e-12 and S0 < z.real < S1 and TA < z.imag <= TB and all(abs(z - w) > 1e-6 for w in zn):
        zn.append(z)
zn = np.array(sorted(zn, key=lambda z: z.imag))
# argument principle on the rectangle (path: bottom, right side up, top, left side down)
up = G_grid([S1], np.linspace(TA, TB, 40000, endpoint=False))[:, 0]
dn = G_grid([S0], np.linspace(TB, TA, 40000, endpoint=False))[:, 0]
bot = G_grid(np.linspace(S0, S1, 4000, endpoint=False), [TA])[0, :]
top = G_grid(np.linspace(S1, S0, 4000, endpoint=False), [TB])[0, :]
ph = np.unwrap(np.angle(np.concatenate([bot, up, top, dn, bot[:1]])))
nap = (ph[-1] - ph[0]) / TWO_PI
log('  found %d zeros; argument principle on the rectangle: %.4f; largest phase step %.3f rad'
    % (len(zn), nap, np.abs(np.diff(ph)).max()))
np.savetxt('zeros_G_200_300_v1.txt', np.c_[zn.real, zn.imag, [abs(Gpt(z)) for z in zn]],
           fmt=['%.12f', '%.12f', '%.2e'], header='zeros of G with 200 < Im s <= 300 (Re s in [-1, 2.5])\nRe  Im  |G| at the polished zero')
zg = np.loadtxt(base + '/zeros_G.txt'); zG = np.r_[zg[:, 0] + 1j * zg[:, 1], zn]
zG = zG[np.argsort(zG.imag)]

# ------------------------------------------------------------------ zeros of zeta and Gram data (comparison only)
gam = []
k = 1
while True:
    g = float(mp.im(mp.zetazero(k)))
    if g > TB: break
    gam.append(g); k += 1
gam = np.array(gam)
th = np.array([float(mp.siegeltheta(x)) for x in gam])
xg = np.mod(th / np.pi - np.arange(1, len(gam) + 1), 2.0)

def alpha(t):
    s = mp.mpc(0.5, t)
    c = (mp.pi / s) * mp.cot(mp.pi * s / 2)
    a = complex(A(np.array([complex(0.5, t)]))[0])
    return float(mp.arg(c)) - np.angle(a) - float(mp.siegeltheta(t))

# ------------------------------------------------------------------ tongues in the two windows
def window(name, t0, t1, dt):
    log(); log('window %s: -1 <= sigma <= 3, %g <= t <= %g (steps 0.01 x %g)' % (name, t0, t1, dt))
    S = np.round(np.arange(-1.0, 3.0 + 1e-9, 0.01), 4); Tt = np.round(np.arange(t0, t1 + 1e-9, dt), 4)
    g = G_grid(S, Tt); a = A(S[None, :] + 1j * Tt[:, None])
    D = np.abs(g) - np.abs(a)
    log('  sign of |G| - |A| on sigma = 3: min %.3e max %.3e;  on sigma = -1: min %.3e max %.3e'
        % (D[:, -1].min(), D[:, -1].max(), D[:, 0].min(), D[:, 0].max()))
    q = g / a
    iR = RegularGridInterpolator((Tt, S), q.real, bounds_error=False, fill_value=None); iI = RegularGridInterpolator((Tt, S), q.imag, bounds_error=False, fill_value=None)
    lines = contourpy.contour_generator(S, Tt, D).lines(0.0)
    loops = []
    for L in lines:
        if len(L) < 5: continue
        closed = np.allclose(L[0], L[-1])
        P = np.c_[L[:, 1], L[:, 0]]
        Q = iR(P) + 1j * iI(P)
        phi = np.unwrap(np.angle(Q))
        rec = dict(L=L, closed=closed, phi=phi)
        rec['wind'] = (phi[-1] - phi[0]) / TWO_PI
        # open loops are closed by the straight segment joining their two ends (on sigma = 3 when both ends lie there)
        Lc = L if closed else np.vstack([L, L[:1]])
        inside = [z for z in zG if t0 < z.imag < t1 and Path(Lc).contains_point((z.real, z.imag))]
        rec['inside'] = inside
        rec['ends_right'] = (not closed) and np.isclose(L[0, 0], 3.0) and np.isclose(L[-1, 0], 3.0)
        hits = []
        for kk in np.arange(np.ceil(phi.min() / TWO_PI), np.floor(phi.max() / TWO_PI) + 1):
            v = phi - kk * TWO_PI
            for jj in np.where(v[:-1] * v[1:] <= 0)[0]:
                if v[jj] == v[jj + 1]: continue
                w = v[jj] / (v[jj] - v[jj + 1]); hits.append(L[jj] + w * (L[jj + 1] - L[jj]))
        rec['hits'] = hits
        cr = []
        v = L[:, 0] - 0.5
        for jj in np.where(v[:-1] * v[1:] <= 0)[0]:
            if v[jj] == v[jj + 1]: continue
            w = v[jj] / (v[jj] - v[jj + 1]); tc = L[jj, 1] + w * (L[jj + 1, 1] - L[jj, 1])
            pc = (phi[jj] + w * (phi[jj + 1] - phi[jj]))
            pm = (pc + np.pi) % TWO_PI - np.pi
            if abs(pm) < 0.02:
                typ, err = 'I', abs(pm)
            else:
                pred = (np.pi + 2 * alpha(tc) + np.pi) % TWO_PI - np.pi
                typ, err = 'II', abs((pm - pred + np.pi) % TWO_PI - np.pi)
            cr.append((tc, typ, pm, err))
        rec['cross'] = sorted({round(c[0], 3): (round(c[0], 4), c[1], round(c[2], 4), c[3]) for c in cr}.values())
        loops.append(rec)
    loops.sort(key=lambda r: r['L'][:, 1].min())
    ok_all = True
    for n_, r in enumerate(loops):
        L = r['L']
        ztxt = ' '.join('%.4f%+.4fi' % (z.real, z.imag) for z in r['inside'])
        zz = [h for h in r['hits']]
        tag = 'closed' if r['closed'] else ('OPEN, both ends on sigma=3' if r['ends_right'] else 'OPEN, cut by the window')
        log('  loop %2d: %s, sigma in [%.3f, %.3f], t in [%.3f, %.3f]; winding of Q %.4f; G = A points %d; zeros of G inside %d %s'
            % (n_, tag, L[:, 0].min(), L[:, 0].max(), L[:, 1].min(), L[:, 1].max(),
               r['wind'], len(zz), len(r['inside']), ztxt))
        if r['closed'] or r['ends_right']:
            ok = (round(r['wind']) == len(r['inside']) == len(zz)) or (round(-r['wind']) == len(r['inside']) == len(zz))
            ok_all &= ok
        for h in zz:
            log('           G = A at sigma=%.5f t=%.5f   (|t - gamma| = %.1e)' % (h[0], h[1], np.abs(gam - h[1]).min()))
        for (tc, typ, pm, err) in r['cross']:
            log('           meets sigma=1/2 at t=%.4f  type %-2s  phi=%+.4f  %s'
                % (tc, typ, pm, ('|phi| = %.1e' % err) if typ == 'I' else ('|phi - (pi + 2 alpha)| = %.1e' % err)))
    log('  closed loops and loops with both ends on sigma = 3: round|winding| = #zeros of G inside = #(G = A on the loop): %s' % ok_all)
    return S, Tt, D, loops

W1 = window('W1', 10.0, 60.0, 0.05)
W2 = window('W2', 268.0, 300.0, 0.02)

# ------------------------------------------------------------------ pairing up to 300
log()
yG = zG.imag
n = min(len(yG), len(gam))
log('pairing: zeros of G with 0 < Im <= 300: %d; zeros of zeta with 0 < gamma <= 300: %d' % (len(yG), len(gam)))
msp = 2 * np.pi / np.log(gam[:n] / (2 * np.pi))
lo = (yG[:n] - gam[:n]) / msp
hi = (np.r_[gam[1:n], np.nan] - yG[:n]) / msp
bad = [k for k in range(n) if not (lo[k] > 0 and (k == n - 1 or hi[k] > 0))]
log('  strict interlacing gamma_k < Im zG_k < gamma_{k+1}: fails for k = %s' % [k + 1 for k in bad])
log('  Gram positions x_k = (theta(gamma_k)/pi - k) mod 2 outside [0,1): k = %s'
    % [k + 1 for k in range(len(gam)) if xg[k] >= 1])
log('  corr(x_k, (Im zG_k - gamma_k)/spacing) for k <= %d: %.3f' % (n, np.corrcoef(xg[:n], lo)[0, 1]))
log('    k    gamma_k        Im zG_k       Re zG_k    (Im zG_k-gamma_k)/sp   x_k')
for k in range(max(0, 110), n):
    log('   %3d  %11.6f  %11.6f  %9.5f   %+8.4f          %.4f' % (k + 1, gam[k], yG[k], zG[k].real, lo[k], xg[k]))
log('time %.1f s' % (time.time() - T0))

# ------------------------------------------------------------------ figures
fig, ax = plt.subplots(1, 2, figsize=(15, 9))
for a_, (S, Tt, D, loops), (t0, t1) in zip(ax, [W1, W2], [(10, 60), (268, 300)]):
    a_.contourf(S, Tt, np.sign(D), levels=[-1.5, 0, 1.5], colors=['#cfe3f5', 'white'])
    for r in loops:
        a_.plot(r['L'][:, 0], r['L'][:, 1], color='k' if r['closed'] else 'orange', lw=1)
    gg = gam[(gam >= t0) & (gam <= t1)]
    a_.plot(0.5 * np.ones_like(gg), gg, 'o', mfc='none', mec='red', ms=7, label='zeros of zeta')
    m = (zG.imag >= t0) & (zG.imag <= t1)
    a_.plot(zG[m].real, zG[m].imag, 'x', color='blue', ms=7, mew=2, label='zeros of G')
    a_.axvline(0.5, color='k', ls='--', lw=0.7)
    a_.set_xlim(-1, 3); a_.set_ylim(t0, t1)
    a_.set_xlabel('sigma = Re s'); a_.set_ylabel('t = Im s')
    a_.set_title('Tongues |G| < |A| (shaded), %g <= t <= %g' % (t0, t1))
    a_.legend(loc='upper right', fontsize=8)
fig.tight_layout(); fig.savefig('fig_tongues_v1.png', dpi=150)

fig2, ax2 = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
ax2[0].plot(np.arange(1, n + 1), lo, 'o-', ms=3); ax2[0].axhline(0, color='k', lw=0.8)
ax2[0].set_ylabel('(Im zG_k - gamma_k) / mean spacing')
ax2[0].set_title('k-th zero of G against the k-th zero of zeta (t <= 300)')
ax2[1].plot(np.arange(1, len(gam) + 1), xg, 'o-', ms=3, color='C1'); ax2[1].axhline(1, color='k', lw=0.8)
ax2[1].set_ylabel('x_k = (theta(gamma_k)/pi - k) mod 2'); ax2[1].set_xlabel('k')
fig2.tight_layout(); fig2.savefig('fig_pairing_v2.png', dpi=150)
