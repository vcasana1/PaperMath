# route_constants.py: every numerical constant quoted in logsine_mobius_route_v1.tex
# (mpmath, 30 digits; sympy for the algebraic identities). Output: route_constants_output.txt
import mpmath as mp, sympy as sp
mp.mp.dps = 30

# C from the series formula C = pi^2/2 - log(2 pi) - 1 - 2 sum (zeta(2k)-1)/(2k-1)
C = mp.pi**2/2 - mp.log(2*mp.pi) - 1 - 2*mp.nsum(lambda k: (mp.zeta(2*k)-1)/(2*k-1), [1, mp.inf])
a = mp.pi*(C - mp.log(2))
print("C =", C)
print("a = pi(C-log2) =", a, "  Fhat(1) = log2 - C =", mp.log(2)-C)
print("log(pi) - zeta(3)/2 =", mp.log(mp.pi) - mp.zeta(3)/2)
print("2 pi^2/3 - 6 =", 2*mp.pi**2/3 - 6)
print("Cl2(pi/3) = max Cl2 =", mp.clsin(2, mp.pi/3))
print("(6/pi^2) a =", 6/mp.pi**2*a)

def A(s):
    # A(s) = (1/s)[log pi - gamma - psi(1-s/2) + 1/s + 2 sum (zeta(2k)-1)/(2k-s)]
    S = mp.nsum(lambda k: (mp.zeta(2*k)-1)/(2*k-s), [1, mp.inf])
    return (mp.log(mp.pi) - mp.euler - mp.digamma(1-s/2) + 1/s + 2*S)/s
def A_series(s):
    return mp.log(2*mp.pi)/s + 1/s**2 + mp.nsum(lambda k: mp.zeta(2*k)/(k*(2*k-s)), [1, mp.inf])

def Fhat_direct(s, N=600):
    # Fhat(s) = int_1^inf log|2 sin pi u| u^{-s-1} du = -((s+1)/(2 pi)) int_1^inf Cl2(2 pi u) u^{-s-2} du
    f = lambda u: mp.clsin(2, 2*mp.pi*u)*u**(-s-2)
    I = mp.fsum(mp.quad(f, [n, n+mp.mpf(1)/2, n+1]) for n in range(1, N))
    return -(s+1)/(2*mp.pi)*I    # tail beyond N is < 1.02 N^{-Re s-1}/(Re s+1) in absolute value
def Fhat_formula(s):
    return mp.pi/s*mp.cot(mp.pi*s/2)*mp.zeta(s) + A(s)

mp.mp.dps = 20
for s in [mp.mpc(0.5, 3), mp.mpc(1.5, 2), mp.mpf(1)]:
    if s == 1:
        print("Fhat(1): direct =", Fhat_direct(mp.mpf(1)), " log2 - C =", mp.log(2)-C)
    else:
        print("s =", s, " direct =", mp.nstr(Fhat_direct(s), 10), " formula =", mp.nstr(Fhat_formula(s), 10),
              " |A - A_series| =", mp.nstr(abs(A(s)-A_series(s)), 3))

# zeros: residues r_k = -(2 pi/(1+rho)) A(rho)/zeta'(rho) of What at s = 1+rho
print("k  gamma_k  |A(rho)|  |zeta'(rho)|  |r_k|")
for k in range(1, 6):
    rho = mp.zetazero(k)
    Ar, zp = A(rho), mp.zeta(rho, derivative=1)
    r = -(2*mp.pi/(1+rho))*Ar/zp
    print(k, mp.nstr(rho.imag, 12), mp.nstr(abs(Ar), 6), mp.nstr(abs(zp), 6), mp.nstr(abs(r), 6), " A(rho)=", mp.nstr(Ar, 8))

# minimum of |s A(s)| on a grid of 0<sigma<1, |t|<=40 (sanity check of A != 0; not a proof)
m = min(abs(A(mp.mpc(x, y))*mp.mpc(x, y)) for x in [0.01, 0.25, 0.5, 0.75, 0.99] for y in [0.0, 0.5, 1, 1.41, 2, 5, 14.13, 40])
print("min |B(s)| on grid =", mp.nstr(m, 6))

# sympy: the two identities of the proof of A != 0
s_, t_, k_ = sp.symbols('sigma t k', positive=True)
lhs = sp.re(sp.expand_complex((s_+sp.I*t_)/(2*k_-s_-sp.I*t_))) + t_**2/(4*k_**2+t_**2)
rhs = 2*k_*s_*(2*k_*(2*k_-s_)-t_**2)/(((2*k_-s_)**2+t_**2)*(4*k_**2+t_**2))
print("Case I identity residual:", sp.simplify(lhs-rhs))
im1 = sp.im(sp.expand_complex(1/(s_+sp.I*t_)))/t_ + 1/(s_**2+t_**2)
im2 = sp.im(sp.expand_complex(2/(2*k_-s_-sp.I*t_)))/t_ - 2/((2*k_-s_)**2+t_**2)
print("Im identities residuals:", sp.simplify(im1), sp.simplify(im2))
q = (sp.pi**2/3)*(s_**2+t_**2) - ((2-s_)**2+t_**2)
print("2zeta(2)(sigma^2+t^2) - (2-sigma)^2 - t^2 =", sp.expand(q))
