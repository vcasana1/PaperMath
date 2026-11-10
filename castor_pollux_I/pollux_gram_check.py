# Check of the weighted Gram formula (Theorem "weighted Gram") of Pollux I:
#   I_{jk}(sigma) = int_M^inf h(x/j) h(x/k) x^{-2 sigma - 1} dx,  h(u) = log|2 sin(pi u)|,  M = max(j,k),
#   I_{jk}(sigma) = M^{-2 sigma}/(2 sigma) * [ T(0) + sum_{r>=1} A(r) kappa(2 pi M r/(jk)) ],
#   A(r) = T(r) + T(-r) + U(r),  kappa(y) = 2 sigma Re E_{2 sigma+1}(-i y).
import mpmath as mp
from math import gcd
mp.mp.dps = 18
def h(u): return mp.log(abs(2*mp.sin(mp.pi*u)))
def T(j,k,r):
    g = gcd(j,k); jp, kp = j//g, k//g
    if r % g: return mp.mpf(0)
    rp = r//g
    if rp == 0: return mp.pi**2/(12*jp*kp)
    m = 1                                   # least m >= 1 with m*kp - rp = n*jp, n >= 1
    while (m*kp - rp) % jp or (m*kp - rp)//jp < 1: m += 1
    n = (m*kp - rp)//jp
    return (mp.digamma(mp.mpf(m)/jp) - mp.digamma(mp.mpf(n)/kp))/(2*rp)
def U(j,k,r):
    s = mp.mpf(0)
    for m in range(1, r//k + 1):
        if (r - m*k) % j == 0 and (r - m*k)//j >= 1: s += mp.mpf(1)/(2*m*((r - m*k)//j))
    return s
def kappa(sig, y): return 2*sig*mp.re(mp.expint(2*sig+1, -1j*y)) if y else mp.mpf(1)
def series(j,k,sig,R):
    M = max(j,k); tot = T(j,k,0)
    for r in range(1, R+1):
        a = T(j,k,r) + T(j,k,-r) + U(j,k,r)
        if a: tot += a*kappa(sig, 2*mp.pi*M*r/(j*k))
    return M**(-2*sig)/(2*sig)*tot
def direct(j,k,sig,periods):
    M = max(j,k); L = j*k//gcd(j,k); X = M + periods*L
    f = lambda x: h(x/j)*h(x/k)*x**(-2*sig-1)
    val = mp.fsum(mp.quad(f, [a, a+mp.mpf(1)/2, a+1]) for a in range(M, X))
    return val + T(j,k,0)*mp.mpf(X)**(-2*sig)/(2*sig)   # tail: |error| <= (pi^2/6) L X^{-2 sigma - 1}
for (j,k,sig) in [(2,3,mp.mpf('0.75')), (4,6,mp.mpf('0.75')), (3,3,mp.mpf('0.5')), (2,5,mp.mpf('0.3'))]:
    d = direct(j,k,sig,150)
    print(f"j={j} k={k} sigma={sig}: direct = {mp.nstr(d,10)}")
    for R in (2000, 20000):
        s = series(j,k,sig,R); print(f"      series R={R}: {mp.nstr(s,10)}   diff = {mp.nstr(d-s,3)}")
    print(f"      gcd term alone: {mp.nstr(max(j,k)**(-2*sig)/(2*sig)*T(j,k,0),10)}")
