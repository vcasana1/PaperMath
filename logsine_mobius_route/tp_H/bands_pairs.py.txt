# Pair (rho, conj rho) coefficient of the corner band by band:
#   J_k(rho) = (1/gamma) int_{2^k}^{2^{k+1}} E_G(Y) Y^{-beta-2} sin(gamma log Y) dY ,  sum_k J_k -> -Im Ehat_G(1+rho)/gamma,
#   Ehat_G(1+rho) = zeta(rho) Theta(1+rho) - a/(rho-1) = -a/(rho-1)  =>  total = -a/|rho-1|^2.
import numpy as np, math, mpmath as mp
from scipy.integrate import quad
exec(open('bilinear_W.py').read().split('print("c_G')[0])
a=cG
for n in [1,2,3]:
    rho=complex(mp.zetazero(n)); b,g=rho.real,rho.imag
    f=lambda Y: (Gs(Y)-a*Y*Y)*Y**(-b-2)*math.sin(g*math.log(Y))/g
    Js=[]; tot=0.0
    for k in range(0,12):
        lo,hi=2.0**k,2.0**(k+1)
        J=sum(quad(f,m,min(m+1,hi),limit=200)[0] for m in np.arange(lo,hi,1.0))
        Js.append(J); tot+=J
    print(f"rho_{n}: bands k=0..11: "+" ".join(f"{J:+.2e}" for J in Js))
    print(f"   partial sum (Y<4096) = {tot:+.6e}   predicted total -a/|rho-1|^2 = {-a/abs(rho-1)**2:+.6e}   tail bound ~ {4096**-0.75:.1e}")
