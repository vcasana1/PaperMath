# Floating-point helpers shared by the search programs (explore_discs.py, kernel_only.py, opt_line.py).
# Nothing here is used by the certification programs.
import numpy as np
from fractions import Fraction as Fr

def f(b, t, d):
    # f(b,t) = 2 atan((d+b)/t) + 2 atan((d-b)/t) - atan((2d+b)/t) - atan((2d-b)/t)
    return 2*np.arctan((b+d)/t)+2*np.arctan((d-b)/t)-np.arctan((b+2*d)/t)-np.arctan((2*d-b)/t)

def F(x, t, k, j):
    # F_Rj = Re (x+it)^-j,  F_Ij = -Im (x+it)^-j
    z = (x+1j*t)**(-j); return z.real if k == 'R' else -z.imag

def basis(m): return [('R', j) for j in range(1, m+1)]+[('I', j) for j in range(2, m+1)]

def tgrid(tmax, ngeom=700, nlin=400):
    # symmetric grid of heights t: geometric on [1e-4, tmax] plus a linear part on (0, 4], and a point near 0
    p = np.unique(np.concatenate([[1e-9], np.geomspace(1e-4, tmax, ngeom), np.linspace(0, 4, nlin)[1:]])); return np.concatenate([-p[::-1], p])

def bourgain_nodes():
    # piecewise linear profile through (lambda_j - kappa_j, kappa_j), (kappa_j, lambda_j) = A^j (13/84, 55/84), j = 0..7, and (1, 0)
    k, l = Fr(13, 84), Fr(55, 84); nodes = []
    for _ in range(8):
        nodes.append((l-k, k)); k, l = k/(2*k+2), Fr(1, 2)+l/(2*k+2)
    nodes.append((Fr(1), Fr(0))); return nodes

def J_float(nodes, c, R, n=40001):
    # (1/pi) int_0^pi e(c + R cos th) dth, e piecewise linear through nodes on [1/2, 1], e = 0 for sigma >= 1 (trapezoidal rule)
    xs = np.array([float(a) for a, _ in nodes]); es = np.array([float(e) for _, e in nodes])
    th = np.linspace(0, np.pi, n); s = c+R*np.cos(th); v = np.where(s >= 1, 0, np.interp(s, xs, es))
    return np.trapezoid(v, th)/np.pi
