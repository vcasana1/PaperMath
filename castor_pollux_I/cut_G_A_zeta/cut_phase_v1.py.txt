#!/usr/bin/env python3
# Castor and Pollux I -- cut_phase_v1
# The curve C = {|G| = |A|} of cut_curve3d.json (v5 data, 0.05<=sigma<=0.95, 10<=t<=60):
#   (1) phase phi = arg(G/A) along each piece, points with phi in 2piZ (G = A), crossings of sigma = 1/2;
#   (2) the tongues of {|G| < |A|} bounded by C and the zeros of G (zeros_G.txt) inside each tongue;
#   (3) pairing of the k-th zero of G with the k-th zero of zeta up to height 200.
# G and A from cp_eval.py (no zeta function). Lists of zeros of G taken as given (zeros_G.txt).
# Ordinates of zeta: t <= 100 from vertical_cut_output.txt (G = A located from G and A only);
# 100 < t <= 200 from mpmath.zetazero, used only for the comparison in (3).
# Usage: python3 cut_phase_v1.py <path to castor_pollux_I>
import sys, json, time, re
import numpy as np
base = sys.argv[1]
sys.path.insert(0, base)
from cp_eval import G_grid, A
import mpmath as mp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

t0 = time.time()
out = open('cut_phase_v1_output.txt', 'w')
def log(s=''):
    print(s, flush=True); out.write(s + '\n')

TWO_PI = 2 * np.pi
d = json.load(open(base + '/cut_G_A_zeta/cut_curve3d.json'))
zg = np.loadtxt(base + '/zeros_G.txt'); zG = zg[:, 0] + 1j * zg[:, 1]
# ordinates G = A on sigma = 1/2 found from G and A only (t <= 100)
tstar = []
for line in open(base + '/cut_G_A_zeta/vertical_cut_output.txt'):
    m = re.match(r'\s+(\d+\.\d+)\s+\S+\s+(\d+\.\d+)\s', line)
    if m: tstar.append(float(m.group(1)))
tstar = np.array(tstar)
mp.mp.dps = 20
gam = [float(mp.im(mp.zetazero(k))) for k in range(1, 81)]
gam = np.array(gam)
nz200 = int((gam <= 200).sum())

# ---------------------------------------------------------------- (1) phase along the pieces
res = []
log('(1) curve |G| = |A|: %d pieces in 0.05<=sigma<=0.95, 10<=t<=60; phi = arg(G/A) unwrapped' % len(d['curves']))
for i, c in enumerate(d['curves']):
    sg = np.array(c[0]); tt = np.array(c[1])
    g = np.array([G_grid([a], [b])[0, 0] for a, b in zip(sg, tt)])
    q = g / A(sg + 1j * tt)
    phi = np.unwrap(np.angle(q)); dphi = np.diff(phi)
    sgn = np.sign(np.median(dphi))
    back = np.where(np.sign(dphi) == -sgn)[0]   # repeated contour points give dphi = 0 and are not counted
    hits = []
    for k in np.arange(np.ceil(phi.min() / TWO_PI), np.floor(phi.max() / TWO_PI) + 1):
        v = phi - k * TWO_PI
        for jj in np.where(v[:-1] * v[1:] <= 0)[0]:
            w = v[jj] / (v[jj] - v[jj + 1]) if v[jj] != v[jj + 1] else 0.0
            hits.append((sg[jj] + w * (sg[jj + 1] - sg[jj]), tt[jj] + w * (tt[jj + 1] - tt[jj])))
    cross = []
    v = sg - 0.5
    idx = np.where(np.abs(v) < 1e-9)[0].tolist()
    idx += [j for j in np.where(v[:-1] * v[1:] < 0)[0]]
    for jj in sorted(set(idx)):
        if abs(v[jj]) < 1e-9:
            tc, ph = tt[jj], phi[jj]
        else:
            w = v[jj] / (v[jj] - v[jj + 1]); tc = tt[jj] + w * (tt[jj + 1] - tt[jj]); ph = phi[jj] + w * (phi[jj + 1] - phi[jj])
        cross.append((tc, (ph + np.pi) % TWO_PI - np.pi))
    im = int(np.argmin(sg))
    r = dict(i=i, sg=sg, tt=tt, phi=phi, hits=hits, cross=cross, smin=sg[im], tmin=tt[im],
             left=bool(np.isclose(sg[0], 0.05) or np.isclose(sg[-1], 0.05)))
    res.append(r)
    log('piece %2d: (%.3f,%.3f) -> (%.3f,%.3f); leftmost sigma %.4f at t %.3f; max||G/A|-1| %.1e; turn %.4f x 2pi'
        % (i, sg[0], tt[0], sg[-1], tt[-1], r['smin'], r['tmin'], np.abs(np.abs(q) - 1).max(), (phi[-1] - phi[0]) / TWO_PI))
    if len(back):
        j = back[np.argmax(np.abs(dphi[back]))]
        log('          phi not monotone at %d steps; largest backward step %.2e rad at sigma=%.3f t=%.3f'
            % (len(back), abs(dphi[j]), sg[j], tt[j]))
    else:
        log('          phi strictly monotone')
    for (s_, t_) in hits:
        log('          G = A (phi in 2piZ) at sigma=%.4f t=%.4f   |t-gamma| = %.1e' % (s_, t_, np.abs(gam - t_).min()))
    for (tc, ph) in cross:
        log('          meets sigma=1/2 at t=%.4f, phi mod 2pi = %+.4f' % (tc, ph))

# ---------------------------------------------------------------- (2) tongues and zeros of G
# a tongue = one piece with both ends on sigma = 0.95, or two consecutive pieces joined through sigma < 0.05
tongues, i = [], 0
while i < len(res):
    if res[i]['left'] and i + 1 < len(res) and res[i + 1]['left']:
        tongues.append([i, i + 1]); i += 2
    else:
        tongues.append([i]); i += 1
log()
log('(2) tongues of {|G| < |A|} cut out by C (open towards sigma > 0.95; "via sigma<0.05" = the two pieces join outside the box)')
def branch_span(ps):
    s = np.concatenate([res[p]['sg'] for p in ps]); t = np.concatenate([res[p]['tt'] for p in ps])
    return s, t
rows = []
for T in tongues:
    s, t = branch_span(T)
    tlo, thi = t.min(), t.max()
    nz = sum(len(res[p]['hits']) for p in T)
    # zeros of G between the two branches: for each zero (x+iy) with y in (tlo,thi) check that C passes
    # below and above it at abscissa min(x, 0.95)
    inside = []
    for z in zG:
        if not (tlo < z.imag < thi): continue
        x = min(z.real, 0.95)
        near = np.abs(s - x) < 0.006
        if near.sum() < 2: continue
        if t[near].min() < z.imag < t[near].max(): inside.append(z)
    closed = res[T[0]]['left'] is False
    vtx = ('vertex sigma %.4f at t %.3f' % (res[T[0]]['smin'], res[T[0]]['tmin'])) if len(T) == 1 and not res[T[0]]['left'] else 'via sigma<0.05'
    complete = not (len(T) == 1 and res[T[0]]['left'])
    rows.append((T, tlo, thi, nz, inside, vtx, complete))
    log('tongue pieces %-7s t in [%.3f, %.3f]  %s:  G = A points %d,  zeros of G inside %d  %s%s'
        % (str(T), tlo, thi, vtx, nz, len(inside), ' '.join('(%.4f%+.4fi)' % (z.real, z.imag) for z in inside),
           '' if complete else '   [cut by t = 60]'))
ok = all(r[3] == len(r[4]) for r in rows if r[6])
log('complete tongues with (#G = A points on the border) = (#zeros of G inside): %s' % ok)

# ---------------------------------------------------------------- (3) pairing by order up to height 200
log()
yG = np.sort(zG.imag)
log('(3) zeros of G with 0.2 <= Im s <= 200: %d;  zeros of zeta with 0 < gamma <= 200: %d' % (len(yG), nz200))
log('    ordinates of zeta for t <= 100 taken from G = A on sigma = 1/2 (vertical_cut): %d values, max |t* - gamma| = %.1e'
    % (len(tstar), np.abs(tstar - gam[:len(tstar)]).max()))
n = min(len(yG), nz200)
dl = yG[:n] - gam[:n]
msp = 2 * np.pi / np.log(gam[:n] / (2 * np.pi))
rel = dl / msp
log('    k   gamma_k        Im zG_k        Re zG_k   Im zG_k - gamma_k   / mean spacing 2pi/log(gamma/2pi)')
zs = zG[np.argsort(zG.imag)]
for k in range(n):
    log('   %2d  %12.6f  %12.6f  %9.6f  %+10.6f   %+8.4f' % (k + 1, gam[k], yG[k], zs[k].real, dl[k], rel[k]))
log('    Im zG_k - gamma_k: min %+.4f  max %+.4f;  normalised: min %+.4f  max %+.4f  mean %+.4f'
    % (dl.min(), dl.max(), rel.min(), rel.max(), rel.mean()))
log('    interlacing gamma_k < Im zG_k < gamma_{k+1} for all k <= %d: %s' % (n - 1, bool(np.all((dl[:-1] > 0) & (yG[:n - 1] < gam[1:n])))))
log('time %.1f s' % (time.time() - t0))

# ---------------------------------------------------------------- figures
fig, ax = plt.subplots(1, 2, figsize=(14, 8))
for r in res:
    sc = ax[0].scatter(r['sg'], r['tt'], c=np.mod(r['phi'], TWO_PI), cmap='twilight', vmin=0, vmax=TWO_PI, s=4)
    ax[1].plot(r['tt'], np.mod(r['phi'] + np.pi, TWO_PI) - np.pi, '.', ms=2, color='0.3')
ax[0].axvline(0.5, color='k', ls='--', lw=0.8)
g60 = gam[gam <= 60]
ax[0].plot(0.5 * np.ones_like(g60), g60, 'o', mfc='none', mec='red', ms=8, label='zeros of zeta  1/2 + i gamma_k')
m = (zG.imag >= 10) & (zG.imag <= 60)
ax[0].plot(np.minimum(zG[m].real, 0.95), zG[m].imag, 'x', color='blue', ms=8, mew=2,
           label='zeros of G (drawn at sigma = 0.95 if Re > 0.95)')
ax[0].set_xlim(0.05, 0.95); ax[0].set_ylim(10, 60)
ax[0].set_xlabel('sigma = Re s'); ax[0].set_ylabel('t = Im s')
ax[0].set_title('Curve |G| = |A| coloured by arg(G/A) mod 2 pi')
ax[0].legend(loc='lower left', fontsize=8)
cb = fig.colorbar(sc, ax=ax[0]); cb.set_label('arg(G/A) mod 2 pi')
ax[1].axhline(0, color='k', lw=0.8)
for gm in g60: ax[1].axvline(gm, color='red', lw=0.6, alpha=0.7)
ax[1].set_xlim(10, 60)
ax[1].set_xlabel('t along the curve'); ax[1].set_ylabel('arg(G/A) in (-pi, pi]')
ax[1].set_title('Phase along the curve (red lines: gamma_k)')
fig.tight_layout(); fig.savefig('fig_cut_phase_v1.png', dpi=150)

fig2, ax2 = plt.subplots(figsize=(9, 5))
ax2.plot(np.arange(1, n + 1), rel, 'o-', ms=4)
ax2.axhline(0, color='k', lw=0.8)
ax2.set_xlabel('k'); ax2.set_ylabel('(Im zG_k - gamma_k) / (2 pi / log(gamma_k / 2 pi))')
ax2.set_title('k-th zero of G against the k-th zero of zeta, in units of the mean spacing')
fig2.tight_layout(); fig2.savefig('fig_pairing_v1.png', dpi=150)

json.dump(dict(pieces=[dict(sigma=r['sg'].round(4).tolist(), t=r['tt'].round(4).tolist(), phi=r['phi'].round(6).tolist())
                       for r in res],
               pairing=[dict(k=k + 1, gamma=gam[k], ImzG=yG[k], RezG=zs[k].real) for k in range(n)]),
          open('cut_phase_v1.json', 'w'), separators=(',', ':'))
