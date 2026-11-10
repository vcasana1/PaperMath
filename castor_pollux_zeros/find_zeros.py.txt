"""Zeros of G and of A in a rectangle of the upper half-plane.

Scan log|F| on a grid, polish each local minimum by Newton (numerical derivative),
re-polish with the mpmath evaluators of funcs.py, and count the zeros in the rectangle
by the argument principle to check that none is missed.
Output: zeros_G.txt, zeros_A.txt, count_check.txt
"""
import numpy as np
import mpmath as mp
import fast
import funcs as F

T = 200.0
RECT = {'G': (-1.5, 3.0, 0.2, T), 'A': (-6.0, 8.0, 0.2, T)}
FAST = {'G': fast.G, 'A': fast.A}
PREC = {'G': F.G, 'A': F.A}


def scan(name):
    s0, s1, t0, t1 = RECT[name]
    sig = np.arange(s0, s1 + 1e-9, 0.05)
    ts = np.arange(t0, t1 + 1e-9, 0.05)
    S, Tt = np.meshgrid(sig, ts)
    vals = np.empty(S.shape)
    for i in range(0, S.shape[0], 200):
        blk = S[i:i + 200] + 1j * Tt[i:i + 200]
        vals[i:i + 200] = np.log(np.abs(FAST[name](blk.ravel()).reshape(blk.shape)) + 1e-300)
    cand = []
    for i in range(1, S.shape[0] - 1):
        for j in range(1, S.shape[1] - 1):
            v = vals[i, j]
            if v <= vals[i - 1:i + 2, j - 1:j + 2].min():
                cand.append(S[i, j] + 1j * Tt[i, j])
    return cand


def newton(f, z, it=40):
    for _ in range(it):
        h = 1e-6
        fz = f(np.array([z]))[0]
        d = (f(np.array([z + h]))[0] - f(np.array([z - h]))[0]) / (2 * h)
        dz = fz / d
        z = z - dz
        if abs(dz) < 1e-13:
            break
    return z, abs(f(np.array([z]))[0])


def arg_count(name, n=40000):
    """Number of zeros in RECT by the argument principle, minus poles (A has none off the real axis)."""
    s0, s1, t0, t1 = RECT[name]
    corners = [s0 + 1j * t0, s1 + 1j * t0, s1 + 1j * t1, s0 + 1j * t1, s0 + 1j * t0]
    path = np.concatenate([np.linspace(a, b, n, endpoint=False) for a, b in zip(corners[:-1], corners[1:])] + [np.array([corners[0]])])
    vals = np.concatenate([FAST[name](path[i:i + 4000]) for i in range(0, len(path), 4000)])
    ph = np.unwrap(np.angle(vals))
    return (ph[-1] - ph[0]) / (2 * np.pi), np.max(np.abs(np.diff(ph)))


def main():
    out = open('count_check.txt', 'w')
    for name in ('G', 'A'):
        zs = []
        for c in scan(name):
            z, r = newton(FAST[name], c)
            s0, s1, t0, t1 = RECT[name]
            if r < 1e-9 and s0 < z.real < s1 and t0 < z.imag < t1 and all(abs(z - w) > 1e-6 for w in zs):
                zs.append(z)
        mp.mp.dps = 20
        pol = []
        for z in sorted(zs, key=lambda w: w.imag):
            try:
                zz = mp.findroot(PREC[name], mp.mpc(z), tol=1e-24)
            except ValueError:
                zz = mp.findroot(PREC[name], mp.mpc(z), tol=1e-16, maxsteps=100)
            if abs(complex(zz) - z) > 1e-6:      # mpmath jumped to another zero: keep the scanned one
                zz = mp.mpc(z)
            pol.append((complex(zz), float(abs(PREC[name](zz)))))
        with open('zeros_%s.txt' % name, 'w') as f:
            f.write('# zeros of %s in Re s in [%g,%g], Im s in [%g,%g]\n# Re  Im  |F| at the polished zero\n' % ((name,) + RECT[name]))
            for z, r in pol:
                f.write('%.12f %.12f %.2e\n' % (z.real, z.imag, r))
        cnt, jump = arg_count(name)
        msg = '%s: %d zeros found; argument principle on the rectangle gives %.4f (largest phase step %.3f rad)\n' % (name, len(pol), cnt, jump)
        print(msg, end='')
        out.write(msg)
    out.close()


if __name__ == '__main__':
    main()
