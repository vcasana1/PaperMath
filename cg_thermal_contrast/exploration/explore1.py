import numpy as np, mpmath as mp
from scipy import integrate
Cg = mp.mpf('0.743794861839400544203641994634580661025264331972917222960354')
def c(m):
    a = 2*mp.pi*m
    return 1 + a*(mp.si(a) - mp.pi/2)
S = mp.nsum(lambda m: c(m)/m, [1, mp.inf])
print('sum c_m/m =', S, ' Cg - log2 =', Cg - mp.log(2))
print('c_1 =', c(1), ' 1-c_1 =', 1-c(1))
def logVinf(nb):
    q = mp.mpf(nb)/(nb+1)
    return -mp.log(nb+1) + mp.nsum(lambda m: c(m)*q**m/m, [1, mp.inf])
delta = mp.pi**2/12 - mp.mpf(3)/4
print('delta', delta)
for nb in [0.01, 0.1, 1, 5, 20, 100, 1000]:
    ex = logVinf(nb)
    lead = Cg - mp.log(2*mp.sqrt(mp.mpf(nb)*(nb+1)))
    corr = lead - delta*mp.log(1+1/mp.mpf(nb))
    eps = mp.log(1+1/mp.mpf(nb))/(2*mp.pi)
    bound = eps**2*(2*mp.log(1+1/eps)+mp.mpf(9)/4)
    print(nb, 'exact', mp.nstr(ex,12), 'lead', mp.nstr(lead,12), 'lead+corr', mp.nstr(corr,12), 'R', mp.nstr(ex-corr,6), 'bound', mp.nstr(bound,6), 'V', mp.nstr(mp.e**ex,8))
def logV(u, nb):
    A = 4*nb*(nb+1)
    return -0.5*np.log1p(A*np.sin(np.pi*u)**2)
def window(nb, U):
    tot = 0.0
    for N in range(1, U):
        v, e = integrate.quad(lambda u: logV(u, nb)/u**2, N, N+1, points=[N+0.5], limit=400, epsabs=1e-13, epsrel=1e-13)
        tot += v
    return tot
I20 = window(20, 20)
print('nbar=20 window[1,20]: integral', I20, ' normalised V_20 =', np.exp(I20/(1-1/20)), ' unnormalised =', np.exp(I20))
print('V_inf exact nbar=20:', mp.e**logVinf(20), ' asympt:', mp.e**Cg/(2*mp.sqrt(420)))
