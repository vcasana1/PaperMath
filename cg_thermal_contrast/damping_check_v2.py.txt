import numpy as np, mpmath as mp
from scipy import integrate
import sys; sys.path.insert(0, '.')
from lst_common import coherence_damped, contrast
mp.mp.dps = 25
c1 = 1 - mp.pi**2 + 2*mp.pi*mp.si(2*mp.pi)
print('Si(2pi) =', mp.nstr(mp.si(2*mp.pi), 12), ' c_1(1) = 1 - pi^2 + 2 pi Si(2 pi) =', mp.nstr(c1, 12), ' 1-c1 =', mp.nstr(1-c1, 10), ' 1/(4 pi^2) =', mp.nstr(1/(4*mp.pi**2), 6))
def c(m):
    x = 2*mp.pi*m
    return float(1 + x*(mp.si(x) - mp.pi/2))
# general class: b = (0.3, 0.5, 0, 0.2)
b = np.array([0.3, 0.5, 0.0, 0.2])
p0 = np.exp(-b.sum())
def logV(u):
    return np.log(p0) + sum(bm*np.cos(2*np.pi*(m+1)*u) for m, bm in enumerate(b))
# check that D(u) = p0 exp(sum b_m z^m) really is a probability generating function: Taylor coefficients >= 0, sum 1
z = np.exp(2j*np.pi*np.arange(4096)/4096)
P = p0*np.exp(sum(bm*z**(m+1) for m, bm in enumerate(b)))
coef = np.fft.fft(P).real/4096
print('min coefficient', coef.min(), ' sum', coef.sum(), ' p0', coef[0], p0)
tot = 0.0
for N in range(1, 4000):
    v, _ = integrate.quad(lambda u: logV(u)/u**2, N, N+1, limit=200)
    tot += v
tot += np.log(p0)/4000        # tail: periodic part averages to log p0
pred = np.log(p0) + sum(bm*c(m+1) for m, bm in enumerate(b))
print('log V_1 numeric', tot, ' formula', pred, ' bounds', np.log(p0), (1-float(c1))*np.log(p0))
print('half-period: log V(1/2) =', logV(0.5), ' formula', np.log(p0)+sum(bm*(-1)**(m+1) for m, bm in enumerate(b)), ' range [2 log p0, 0] =', 2*np.log(p0))
# damping bound |V_kappa - V| <= pi Lambda (kappa/chi) u ; rho = kappa/(2 chi)
worst = 0
for nb in [0.05, 1.0, 5.0, 20.0]:
    Lam = 4*nb*(nb+1)
    for rho in [1e-5, 1e-4, 1e-3, 1e-2]:
        u = np.linspace(0.01, 6, 6000)
        dv = np.abs(np.abs(coherence_damped(u, nb, rho)) - contrast(u, nb))
        dD = np.abs(coherence_damped(u, nb, rho)*np.exp(-1j*np.pi*u*0) - (nb+1)**-1/(1-nb/(nb+1)*np.exp(-2j*np.pi*u)))
        bound = np.pi*Lam*2*rho*u
        r = (dv/bound).max()
        worst = max(worst, r)
        print('nbar %5.2f rho %.0e  max |dV|/bound = %.4f' % (nb, rho, r))
print('worst ratio', worst)
