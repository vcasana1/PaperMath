"""Common functions for the log-sine thermometry paper (Python 3, numpy, scipy, mpmath).

Notation as in the paper:
  nbar  mean thermal occupation,  q = nbar/(nbar+1),  tau = log(1/q),  A = 4 nbar (nbar+1)
  u     reduced delay, u = chi t / pi
  V(u)  Ramsey contrast of the probe, V = (1 + A sin^2(pi u))^(-1/2)
  c_m   = int_1^inf cos(2 pi m u) u^(-2) du = 1 + 2 pi m (Si(2 pi m) - pi/2)
  S(q)  = sum_m q^m c_m / m,  S(1) = C_g - log 2,  sum_m c_m = pi^2/12 - 3/4
"""
import numpy as np
import mpmath as mp
from scipy import integrate, optimize

mp.mp.dps = 30


def c_coef(a):
    """c(a) = int_1^inf cos(2 pi a u) u^-2 du for real a > 0 (mpmath)."""
    a = mp.mpf(a)
    x = 2 * mp.pi * a
    return mp.cos(x) + x * (mp.si(x) - mp.pi / 2)


def S_series(q, U=None):
    """S(q) = sum q^m c_m/m ; with integer U >= 2 the window series sum q^m (c_m - c_{mU}/U)/m."""
    q = mp.mpf(q)
    if U is None:
        return mp.nsum(lambda m: q ** m * c_coef(m) / m, [1, mp.inf])
    return mp.nsum(lambda m: q ** m * (c_coef(m) - c_coef(m * U) / U) / m, [1, mp.inf])


def log_Vinf(nbar):
    """Exact log of the geometric visibility on [1, inf)."""
    nbar = mp.mpf(nbar)
    q = nbar / (nbar + 1)
    return mp.log(1 - q) + S_series(q)


def log_VU(nbar, U):
    """Exact log of the geometric visibility on the window [1, U], U integer >= 2."""
    nbar = mp.mpf(nbar)
    q = nbar / (nbar + 1)
    return mp.log(1 - q) + S_series(q, U) * U / (U - 1)


def contrast(u, nbar):
    A = 4.0 * nbar * (nbar + 1.0)
    return 1.0 / np.sqrt(1.0 + A * np.sin(np.pi * u) ** 2)


def coherence_damped(u, nbar, rho):
    """Exact coherence of the probe for a damped thermal mode; rho = kappa/(2 chi), u = chi t/pi."""
    u = np.asarray(u, dtype=float)
    al = np.sqrt((1 - 1j * rho) ** 2 - 4j * rho * nbar + 0j)
    qk = (2 * nbar + 1 - 1j * rho - al) / (2 * nbar + 1 - 1j * rho + al)
    return np.exp(np.pi * u * (rho + 1j * (1 - al))) * (1 - qk) / (1 - qk * np.exp(-2j * np.pi * al * u))


def log_VU_damped(nbar, rho, U):
    """log geometric visibility on [1, U] computed by quadrature from the damped contrast."""
    f = lambda u: np.log(np.abs(coherence_damped(u, nbar, rho))) / u ** 2
    tot = 0.0
    for N in range(1, U):
        v, _ = integrate.quad(f, N, N + 1, points=[N + 0.5], limit=400, epsabs=1e-13, epsrel=1e-12)
        tot += v
    return tot * U / (U - 1)


def invert_VU(logv, U):
    """Occupation nbar such that log_VU(nbar, U) = logv (the map is strictly decreasing)."""
    f = lambda x: float(log_VU(mp.e ** x, U)) - logv
    x = optimize.brentq(f, np.log(1e-9), np.log(1e7), xtol=1e-13)
    return float(np.exp(x))


def eta_ramsey_u(u, nbar):
    """Per-shot Fisher information of a Ramsey shot at delay u (best quadrature), in units of 1/(nbar(nbar+1))."""
    A = 4.0 * nbar * (nbar + 1.0)
    z = A * np.sin(np.pi * u) ** 2
    return z / (1 + z) ** 2 + (1 + 1 / A) * z / (1 + z) ** 3


def eta_ramsey(nbar):
    """Maximum over the delay; returns (efficiency, z)."""
    A = 4.0 * nbar * (nbar + 1.0)
    b = 1 + 1 / A
    z = min(-b + np.sqrt(b * b + b + 1), A)
    return z / (1 + z) ** 2 + b * z / (1 + z) ** 3, z


def eta_line(nbar, n):
    """Efficiency of the number-selective test on line n."""
    q = nbar / (nbar + 1.0)
    p = (1 - q) * q ** n
    return p * (n - nbar) ** 2 / (nbar * (nbar + 1) * (1 - p))


def eta_threshold(nbar):
    """Best threshold test {n >= L}; returns (efficiency, L)."""
    q = nbar / (nbar + 1.0)
    L = np.arange(1, int(40 * nbar + 40))
    e = L ** 2 * q ** (L - 1) * (1 - q) ** 2 / (1 - q ** L)
    i = int(np.argmax(e))
    return float(e[i]), int(L[i])


def I1_constant():
    """I_1 = int_1^inf |sin(pi u)| u^-2 du."""
    return mp.nsum(lambda N: mp.quad(lambda u: mp.sin(mp.pi * (u - N)) / u ** 2, [N, N + mp.mpf(1) / 2, N + 1]), [1, mp.inf])


def e_geometric(nbar, I1):
    """Efficiency of the geometric visibility with the best allocation of shots."""
    nbar = mp.mpf(nbar)
    q = nbar / (nbar + 1)
    Sp = mp.nsum(lambda m: q ** (m - 1) * c_coef(m), [1, mp.inf])
    return (1 - q) ** 2 * (1 - (1 - q) * Sp) ** 2 / (4 * I1 ** 2)
