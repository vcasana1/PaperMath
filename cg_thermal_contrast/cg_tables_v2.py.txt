"""New numbers of Cg_Thermal_Contrast_v2 (Python 3, mpmath).  Run: python3 cg_tables_v2.py > cg_tables_v2_output.txt
b_m: coefficients of the compound Poisson form  sum p_n z^n = p0 exp(sum b_m z^m).
Displaced thermal state with thermal ratio q and coherent amplitude |xi|^2 = X:
  b_m = q^m/m + X (1-q)^2 q^(m-1),  p0 = (1-q) exp(-X (1-q)).
"""
import mpmath as mp
mp.mp.dps = 30


def c(m):
    x = 2 * mp.pi * m
    return 1 + x * (mp.si(x) - mp.pi / 2)


c1 = c(1)
print('Si(2 pi) =', mp.nstr(mp.si(2 * mp.pi), 15))
print('c_1(1) = 1 - pi^2 + 2 pi Si(2 pi) =', mp.nstr(1 - mp.pi ** 2 + 2 * mp.pi * mp.si(2 * mp.pi), 15), ' (series form', mp.nstr(c1, 15), ')')
print('1/(4 pi^2) =', mp.nstr(1 / (4 * mp.pi ** 2), 10), '  1 - c_1 =', mp.nstr(1 - c1, 10))
print()
print('Table: displaced thermal states (nbar_th = 0 means Poisson of mean |xi|^2)')
print(' nbar_th  |xi|^2   p0          V_1         logV1/logp0   V(1/2)       2V(1/2)/(1+V(1/2))   ratio to p0')
for nth, X in [(0, 1), (0.5, 0), (0.5, 0.25), (0.5, 1), (0.5, 2)]:
    nth = mp.mpf(nth); X = mp.mpf(X)
    q = nth / (nth + 1)
    p0 = (1 - q) * mp.e ** (-X * (1 - q))
    b = lambda m: (q ** m / m if q > 0 else 0) + X * (1 - q) ** 2 * q ** (m - 1)
    S = mp.nsum(lambda m: b(m) * c(m), [1, mp.inf]) if q > 0 else X * c1
    alt = mp.nsum(lambda m: b(m) * (-1) ** m, [1, mp.inf]) if q > 0 else -X
    V1 = p0 * mp.e ** S
    Vh = p0 * mp.e ** alt
    est = 2 * Vh / (1 + Vh)
    print(' %4s   %5s   %s  %s  %s   %s  %s   %s' % (mp.nstr(nth, 2), mp.nstr(X, 3), mp.nstr(p0, 7), mp.nstr(V1, 7),
          mp.nstr(mp.log(V1) / mp.log(p0), 6), mp.nstr(Vh, 7), mp.nstr(est, 7), mp.nstr(est / p0, 5)))
print()
print('Damping: largest kappa/chi with eps = 0.1, U = 20:  eps / (pi Lambda (2 nbar + 1) U)')
for nb in [0.1, 1, 20]:
    nb = mp.mpf(nb); Lam = 4 * nb * (nb + 1)
    k = mp.mpf('0.1') / (mp.pi * Lam * (2 * nb + 1) * 20)
    print('  nbar %5s  kappa/chi <= %s   (kappa/2pi <= %s Hz for chi/2pi = 1 MHz)' % (mp.nstr(nb, 3), mp.nstr(k, 4), mp.nstr(k * 1e6, 4)))
print('  kappa/2pi for a single-photon lifetime of 25.6 ms:', mp.nstr(1 / (2 * mp.pi * mp.mpf('0.0256')), 4), 'Hz')
print('Truncation, nbar = 20, s = 1, U = 20: bound L/U =', mp.nstr(mp.log(41) / 20, 4))
