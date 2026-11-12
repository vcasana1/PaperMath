import numpy as np
from scipy import optimize, integrate
# Ramsey Fisher information relative to QFI = 1/(nb(nb+1))
def eta_ramsey(nb, ngrid=4001):
    q = nb/(nb+1.0)
    best = (0,0,0)
    # phi in (0, 2pi); search on log grid near 0 and uniform
    phis = np.unique(np.concatenate([np.linspace(1e-6, np.pi, ngrid), np.logspace(-7, np.log10(np.pi), ngrid)]))
    thetas = np.linspace(0, np.pi, 721)
    C = (1-q)/(1-q*np.exp(-1j*phis))
    dC = (np.exp(-1j*phis)-1)*C**2        # dC/dnbar
    E = np.exp(1j*thetas)[:,None]
    num = (np.real(E*dC[None,:]))**2
    den = 1-(np.real(E*C[None,:]))**2
    F = num/np.maximum(den,1e-300)
    i = np.unravel_index(np.argmax(F), F.shape)
    return F[i]*nb*(nb+1), phis[i[1]], thetas[i[0]]
def eta_spec(nb, mmax=None):
    q = nb/(nb+1.0)
    mmax = mmax or int(60*nb+60)
    m = np.arange(0, mmax)
    p = (1-q)*q**m
    F = p*(m-nb)**2/(nb**2*(nb+1)**2*(1-p))
    i = np.argmax(F)
    return F[i]*nb*(nb+1), i
print('nbar   eta_Ramsey  phi*  phi*nbar theta*   eta_spec  m*   1/(nb+1)  ratio')
for nb in [0.001,0.01,0.05,0.1,0.2,0.3,0.5,0.75,1,1.5,2,3,5,10,20,50,100,1000]:
    er, ph, th = eta_ramsey(nb)
    es, ms = eta_spec(nb)
    print('%7.3f  %.5f  %.5f %.4f %.4f   %.5f  %d  %.5f  %.3f' % (nb, er, ph, ph*nb, th, es, ms, 1/(nb+1), er/es))
# universal large-n limit: f(x,psi) = x^2 sin^2(psi-a)/((1+x^2)(x^2+sin^2 psi)), a=arctan x
def f(v):
    x, psi = v
    a = np.arctan(x)
    return -(x**2*np.sin(psi-a)**2/((1+x**2)*(x**2+np.sin(psi)**2)))
best = min((optimize.minimize(f, [x0,p0], method='Nelder-Mead', options={'xatol':1e-12,'fatol':1e-15}) for x0 in [0.3,1,2] for p0 in [0.5,1.5,2.5]), key=lambda r: r.fun)
print('large-n limit: max f =', -best.fun, 'at x, psi =', best.x)
