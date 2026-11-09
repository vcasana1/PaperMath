# Top block of the corner, Y = X/(dj) in [1,2):  B(X) = X * sum_{d,j<=U, dj>X/2} mu(d)mu(j) k(X/(dj)),
#   k(Y) = Cl2(2 pi Y)/Y - a Y  (Y in [1,2)),  kappa(s) = int_1^2 k(Y) Y^{-s-1} dY  (entire).
# Pair (rho, conj rho) coefficient: I(rho) = int int_{[1/2,1]^2} x^{rho-1} y^{conj(rho)-1} k(1/(xy)) dx dy = -Im kappa(rho)/gamma.
# Split kappa = kappa_Cl + kappa_a, kappa_a(s) = -a (2^{1-s}-1)/(1-s).
import mpmath as mp
mp.mp.dps=20
a=mp.mpf('0.15911438342889386541')
kCl=lambda s: mp.quad(lambda Y: mp.clsin(2,2*mp.pi*Y)*Y**(-s-2),[1,mp.mpf(7)/6,1.5,2])
ka=lambda s: -a*(2**(1-s)-1)/(1-s)
# check the 1D reduction against the 2D integral for one rho
rho=mp.zetazero(1); g=rho.imag
k=lambda Y: (mp.clsin(2,2*mp.pi*Y)/Y - a*Y) if Y<2 else 0
I2=mp.quad(lambda x: mp.quad(lambda y: (x**(rho-1)*y**(mp.conj(rho)-1)*k(1/(x*y))) if x*y>0.5 else 0,[0.5,1/(2*x),1]) if x>0.5 else 0,[0.5,1])
print("check rho1: 2D =",mp.nstr(I2,10)," -Im kappa/gamma =",mp.nstr(-mp.im(kCl(rho)+ka(rho))/g,10))
print("s=0: kappa_Cl(0)=",mp.nstr(kCl(0),8)," kappa_a(0)=",mp.nstr(ka(0),8))
print(" k   gamma      -Im kCl/g     -Im ka/g      total I      |kCl/ka|   I/|zeta'|^2")
for n in range(1,11):
    rho=mp.zetazero(n); g=rho.imag; c=kCl(rho); d=ka(rho)
    I=-mp.im(c+d)/g
    print(f"{n:2d} {float(g):9.4f} {float(-mp.im(c)/g):+.6e} {float(-mp.im(d)/g):+.6e} {float(I):+.6e} {float(abs(c/d)):.3f} {float(I/abs(mp.zeta(rho,derivative=1))**2):+.3e}")
print(" beta  (off-line test, gamma=gamma_1):  -Im kCl/g  -Im ka/g  total")
for b in [0.5,0.6,0.7,0.8,0.9]:
    s=mp.mpf(b)+1j*mp.zetazero(1).imag; g=s.imag
    print(f" {b}: {float(-mp.im(kCl(s))/g):+.6e} {float(-mp.im(ka(s))/g):+.6e} {float(-mp.im(kCl(s)+ka(s))/g):+.6e}")
