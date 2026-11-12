import numpy as np, mpmath as mp
from scipy import integrate, optimize
# I1 = int_1^inf |sin pi u| / u^2 du ; I2 = int_1^inf sin^2(pi u)/u^2 du
I1 = mp.nsum(lambda N: mp.quad(lambda u: mp.sin(mp.pi*(u-N))/u**2, [N, N+0.5, N+1]), [1, mp.inf])
print('I1 =', I1, ' 4 I1^2 =', 4*I1**2)
def c(m):
    a = 2*mp.pi*m
    return 1 + a*(mp.si(a) - mp.pi/2)
cm = [None]+[c(m) for m in range(1, 4001)]
print('sum c_m (4000 terms) =', mp.fsum(cm[1:]), ' pi^2/12-3/4 =', mp.pi**2/12-mp.mpf(3)/4)
def Sprime(q):
    return mp.nsum(lambda m: q**(m-1)*c(m), [1, mp.inf])
def eV(nb):
    q = mp.mpf(nb)/(nb+1)
    return (1-q)**2*(1-(1-q)*Sprime(q))**2/(4*I1**2)
def gR(nb):
    A = 4*nb*(nb+1.0); b = 1+1/A
    zs = -b+np.sqrt(b*b+b+1)
    z = min(zs, A)
    return z/(1+z)**2 + b*z/(1+z)**3, z
def thr(nb):
    q = nb/(nb+1.0)
    L = np.arange(1, int(40*nb+40))
    e = L**2*q**(L-1)*(1-q)**2/(1-q**L)
    i = np.argmax(e); return e[i], L[i]
print('nbar  eta_spec  eta_Ramsey(z)  eta_threshold(L)  e_V')
for nb in [0.01, 0.1, 0.3, 1, 1.52, 1.6, 3, 10, 20, 100]:
    g, z = gR(nb); t, L = thr(nb)
    print('%6.2f  %.4f  %.4f (z=%.4f)  %.4f (L=%d)  %.5f' % (nb, 1/(nb+1), g, z, t, L, eV(nb)))
# crossover Ramsey = spectroscopy
f = lambda nb: gR(nb)[0] - 1/(nb+1)
print('crossover nbar =', optimize.brentq(f, 1.0, 2.0))
# check closed formula eta(u) against brute force over theta
nb = 3.0; q = nb/(nb+1); A = 4*nb*(nb+1)
for u in [0.03, 0.1, 0.37, 0.5]:
    ph = 2*np.pi*u
    C = (1-q)/(1-q*np.exp(-1j*ph)); dC = (np.exp(-1j*ph)-1)*C**2
    th = np.linspace(0, np.pi, 200001)
    F = np.real(np.exp(1j*th)*dC)**2/(1-np.real(np.exp(1j*th)*C)**2)
    z = A*np.sin(np.pi*u)**2
    print(u, F.max()*nb*(nb+1), z/(1+z)**2+(1+1/A)*z/(1+z)**3)
# damped formula vs truncated rate equations for the coherence block
def Cdamped(t, chi, kap, nb):
    rho = kap/(2*chi)
    al = np.sqrt((1-1j*rho)**2 - 4j*rho*nb + 0j)
    M = (2*nb+1-1j*rho-al)/(2*nb+1-1j*rho+al)
    return np.exp((kap/2+1j*chi*(1-al))*t)*(1-M)/(1-M*np.exp(-2j*chi*al*t))
def Code(tmax, chi, kap, nb, nmax=400):
    q = nb/(nb+1); n = np.arange(nmax)
    p0 = (1-q)*q**n + 0j
    def rhs(t, p):
        d = -2j*chi*n*p
        d += kap*(nb+1)*(np.append((n[1:])*p[1:], 0) - n*p)
        d += kap*nb*(np.append(0, n[1:]*p[:-1]) - (n+1)*p)
        return d
    sol = integrate.solve_ivp(rhs, [0, tmax], p0, rtol=1e-10, atol=1e-13, dense_output=True)
    return lambda t: sol.sol(t).sum()
chi, kap, nb = 1.0, 0.05, 2.0
Cn = Code(8.0, chi, kap, nb)
for t in [0.3, 1.0, np.pi, 5.0, 2*np.pi, 8.0]:
    print('t=%.3f formula %s  ode %s' % (t, Cdamped(t, chi, kap, nb), Cn(t)))
al = np.sqrt((1-1j*kap/(2*chi))**2-4j*(kap/(2*chi))*nb)
print('long-time rate formula -kap/2 - chi*Im(al) =', -kap/2-chi*al.imag, ' Rigetti form:', 0.5*np.real(np.sqrt((kap+2j*chi)**2+8j*chi*kap*nb)-kap))
