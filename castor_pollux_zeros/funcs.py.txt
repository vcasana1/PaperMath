"""Evaluators for A(s) and G(s) (Castor-Pollux), mpmath.

A(s) = log(2pi)/s + 1/s^2 + sum_{k>=1} a_k / (k (2k - s)),  a_k = sum_n n^{-2k}
     = log(2pi)/s + 1/s^2 - (psi(1 - s/2) + gamma)/s + sum_k (a_k - 1)/(k (2k - s)).

G(s) = -(s+1)(s+2)/(4 pi^2) * H(s),  H(s) = int_1^inf K(u) u^{-s-3} du,
evaluated as H(s) = int_0^1 K(x) * HurwitzSum(s+3, 1+x) dx  (Gauss-Legendre on [0,1/2],[1/2,1]),
with K(x) = sum_m (1 - cos 2 pi m x)/m^3 = Sigma_3 - Re Li_3(e^{2 pi i x}).
"""
import mpmath as mp

mp.mp.dps = 20
KMAX = 60
_ak1 = [mp.nsum(lambda n: n ** (-2 * k), [1, mp.inf]) - 1 for k in range(1, KMAX + 1)]


def A(s):
    s = mp.mpc(s)
    val = mp.log(2 * mp.pi) / s + 1 / s ** 2 - (mp.digamma(1 - s / 2) + mp.euler) / s
    for k in range(1, KMAX + 1):
        val += _ak1[k - 1] / (k * (2 * k - s))
    return val


def A_integral(s):
    """Definition (eq:A), only for 0<Re s<2 (check)."""
    s = mp.mpc(s)
    f = lambda u: mp.log(mp.sin(mp.pi * u) / (mp.pi * u)) * u ** (-s - 1)
    return mp.log(2 * mp.pi) / s + 1 / s ** 2 - mp.quad(f, [0, 0.5, 1])


_S3 = mp.zeta(3)
_nodes = None


def _setup(n=48):
    global _nodes
    xs, ws = [], []
    gl = mp.calculus.quadrature.GaussLegendre(mp.mp)
    pts = gl.calc_nodes(6, mp.mp.prec)  # degree 6 -> 3*2^5 = 96 nodes on [-1,1]
    for a, b in ((mp.mpf(0), mp.mpf(0.5)), (mp.mpf(0.5), mp.mpf(1))):
        for x, w in pts:
            xx = a + (b - a) * (x + 1) / 2
            xs.append(xx)
            ws.append(w * (b - a) / 2)
    Ks = [_S3 - mp.re(mp.polylog(3, mp.exp(2j * mp.pi * x))) for x in xs]
    _nodes = list(zip(xs, ws, Ks))


def H(s):
    if _nodes is None:
        _setup()
    z = mp.mpc(s) + 3
    return mp.fsum(w * K * mp.zeta(z, 1 + x) for x, w, K in _nodes)


def G(s):
    s = mp.mpc(s)
    return -(s + 1) * (s + 2) / (4 * mp.pi ** 2) * H(s)


def G_direct(s):
    """Definition (eq:G), Re s > 0 (check)."""
    s = mp.mpc(s)
    f = lambda u: mp.log(abs(2 * mp.sin(mp.pi * u))) * u ** (-s - 1)
    return mp.quad(f, mp.linspace(1, 60, 60)) + mp.quad(f, [60, mp.inf])
