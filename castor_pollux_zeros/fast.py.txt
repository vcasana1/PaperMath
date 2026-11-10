"""Vectorised double-precision evaluators of G and A, for scanning.

G = -(s+1)(s+2)/(4pi^2) H,  H(s) = int_0^1 K(x) sum_{n>=1} (n+x)^{-s-3} dx,
sum over n<=N directly, n>N by Euler-Maclaurin (3 correction terms).
"""
import numpy as np
from scipy.special import digamma
import mpmath as mp

# Gauss-Legendre nodes on [0,1/2] and [1/2,1]
_g, _w = np.polynomial.legendre.leggauss(80)
X = np.concatenate([(_g + 1) / 4, 0.5 + (_g + 1) / 4])
W = np.concatenate([_w / 4, _w / 4])
S3 = float(mp.zeta(3))
KX = np.array([S3 - float(mp.re(mp.polylog(3, mp.exp(2j * mp.pi * x)))) for x in X])
AK1 = np.array([float(mp.zeta(2 * k)) - 1 for k in range(1, 61)])
KK = np.arange(1, 61)


def H(s, N=120):
    s = np.atleast_1d(np.asarray(s, dtype=complex))
    z = s[:, None] + 3.0
    tot = np.zeros(s.shape + X.shape, dtype=complex)
    for n in range(1, N + 1):
        tot += np.exp(-z * np.log(n + X)[None, :])
    y = (N + 1 + X)[None, :]
    ly = np.log(y)
    p = np.exp(-z * ly)
    tot += y * p / (z - 1) + p / 2 + z * p / (12 * y) - z * (z + 1) * (z + 2) * p / (720 * y ** 3) \
        + z * (z + 1) * (z + 2) * (z + 3) * (z + 4) * p / (30240 * y ** 5)
    return tot @ (W * KX)


def G(s, N=120):
    s = np.asarray(s, dtype=complex)
    return -(s + 1) * (s + 2) / (4 * np.pi ** 2) * H(s, N).reshape(s.shape)


def A(s):
    s = np.asarray(s, dtype=complex)
    v = np.log(2 * np.pi) / s + 1 / s ** 2 - (digamma(1 - s / 2) + np.euler_gamma) / s
    v = v + (AK1 / (KK * (2 * KK - s[..., None]))).sum(-1)
    return v
