# Castor-Pollux I: figures (all labels in English).  G is computed from the positive kernel K only:
#   G(s) = -(s+1)(s+2) H(s)/(4 pi^2),  H(s) = int_0^1 K(x) sum_{n>=1} (n+x)^{-s-3} dx  (midpoint rule + Euler-Maclaurin tail).
import numpy as np, math, mpmath as mp
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.special import digamma, bernoulli, factorial
M, N, L = 2000, 24, 8192
x = (np.arange(L) + 0.5)/L
K = np.zeros(L)
for m0 in range(1, M+1, 200):
    m = np.arange(m0, min(m0+200, M+1))[:, None]
    K += ((1 - np.cos(2*np.pi*m*x[None, :]))/m**3).sum(axis=0)
def H(s):
    a = s + 3; tot = 0j
    for n in range(1, N+1): tot += (K*(n + x)**(-a)).sum()
    b = N + 1 + x
    tot += (K*(b**(1-a)/(a-1) + b**(-a)/2 + a*b**(-a-1)/12 - a*(a+1)*(a+2)*b**(-a-3)/720)).sum()
    return tot/L
def G(s): return -(s+1)*(s+2)*H(s)/(4*np.pi**2)
kk = np.arange(1, 41); Bn = bernoulli(80)
ZK = np.array([(-1)**(k+1)*Bn[2*k]*(2*np.pi)**(2*k)/(2*factorial(2*k)) for k in kk])   # Taylor coefficients of -log(sin x/x)
def A(s):   # A(s) = log(2pi)/s + 1/s^2 - int_0^1 log(sin(pi u)/(pi u)) u^{-s-1} du
    return np.log(2*np.pi)/s + 1/s**2 + ((ZK-1)/(kk*(2*kk-s))).sum() + (-digamma(1-s/2) - np.euler_gamma)/s
sig = np.linspace(0.05, 1.95, 39); tt = np.linspace(1, 40, 157)
S, T = np.meshgrid(sig, tt)
Gv = np.zeros(S.shape, complex); Av = np.zeros(S.shape, complex); Zv = np.zeros(S.shape, complex)
for i in range(S.shape[0]):
    for j in range(S.shape[1]):
        s = complex(S[i, j], T[i, j]); Gv[i, j] = G(s); Av[i, j] = A(s); Zv[i, j] = complex(mp.zeta(s))
chk = np.abs(Gv - Av - (np.pi/(S+1j*T))/np.tan(np.pi*(S+1j*T)/2)*Zv).max()
print("grid:", S.shape, " max |G - A - (pi/s) cot(pi s/2) zeta| on the grid =", chk)
np.savez('grid_values.npz', sigma=sig, t=tt, G=Gv, A=Av, zeta=Zv)
def surface(V, title, fname, zlabel):
    fig = plt.figure(figsize=(8, 6)); ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(S, T, np.log10(np.abs(V)), cmap='viridis', linewidth=0, antialiased=True, rcount=157, ccount=39)
    ax.set_xlabel('Re s'); ax.set_ylabel('Im s'); ax.set_zlabel(zlabel); ax.set_title(title); ax.view_init(elev=35, azim=-60)
    fig.tight_layout(); fig.savefig(fname, dpi=200)
surface(Gv, 'Modulus of G(s), logarithmic scale', 'fig_G_surface.png', 'log10 |G(s)|')
surface(Av, 'Modulus of A(s), logarithmic scale', 'fig_A_surface.png', 'log10 |A(s)|')
surface(Zv, 'Modulus of the Riemann zeta function, logarithmic scale', 'fig_zeta_surface.png', 'log10 |zeta(s)|')
surface(Gv - Av, 'Modulus of G(s) - A(s), logarithmic scale', 'fig_GminusA_surface.png', 'log10 |G(s) - A(s)|')
# zero map
zG = [(1.127313, 15.001263), (0.533572, 21.763255), (0.894731, 25.624837), (0.227688, 30.975963), (0.950507, 33.599088), (0.430900, 38.054886)]
zD = [(0.5, float(mp.zetazero(k).imag)) for k in range(1, 7)]
Psi = Gv/Av
fig, ax = plt.subplots(figsize=(6, 9))
pc = ax.pcolormesh(S, T, np.log10(np.abs(Gv)), cmap='Greys', shading='auto'); fig.colorbar(pc, ax=ax, label='log10 |G(s)|')
ax.contour(S, T, np.where((Psi.real > 0) & (Psi.real < 1), Psi.imag, np.nan), levels=[0], colors='tab:blue', linewidths=1.5)
ax.plot(*zip(*zG), 'o', color='tab:red', label='zeros of G'); ax.plot(*zip(*zD), 'x', color='tab:green', ms=9, mew=2, label='points with G = A')
ax.plot([], [], color='tab:blue', label='Im(G/A) = 0 with 0 < Re(G/A) < 1')
ax.set_xlabel('Re s'); ax.set_ylabel('Im s'); ax.set_title('Zeros of G, points with G = A, and the arcs joining them'); ax.legend(loc='lower left', fontsize=8)
fig.tight_layout(); fig.savefig('fig_zero_map.png', dpi=200)
# kernel
u = np.linspace(0.002, 0.998, 2000)
fig, axs = plt.subplots(1, 2, figsize=(10, 4))
axs[0].plot(u, np.log(2*np.sin(np.pi*u))); axs[0].axhline(0, color='k', lw=0.5); axs[0].set_title('h(u) = log|2 sin(pi u)| on one period'); axs[0].set_xlabel('u'); axs[0].set_ylabel('h(u)')
axs[1].plot(x, K); axs[1].set_title('Positive kernel K(x) = sum (1 - cos(2 pi m x))/m^3'); axs[1].set_xlabel('x'); axs[1].set_ylabel('K(x)')
fig.tight_layout(); fig.savefig('fig_kernel.png', dpi=200)
# G on the real axis
sr = np.linspace(-1.9, 3, 99); Gr = np.array([G(complex(v, 0)).real for v in sr])
fig, ax = plt.subplots(figsize=(7, 4)); ax.plot(sr, Gr); ax.axhline(0, color='k', lw=0.5); ax.plot([-1], [0], 'o', color='tab:red', label='simple zero at s = -1')
ax.set_xlabel('s (real)'); ax.set_ylabel('G(s)'); ax.set_title('G on the real axis: positive on (-2,-1), negative for s > -1'); ax.legend()
fig.tight_layout(); fig.savefig('fig_G_real.png', dpi=200)
print("G(1) =", G(1+0j).real, " G(-1) =", G(-1+0j).real)
