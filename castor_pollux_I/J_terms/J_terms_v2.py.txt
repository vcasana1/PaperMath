# J_terms_v2.py  (v1 lost precision in T1 near u=0: Q-q0 was computed as a difference)
# Values of the three terms of the regularized integral
#   J(s) = int_0^inf Q(u) u^{-s-3} du  (regularized) = T1(s) + T2(s) + T3(s),
# for s = sigma + i t, sigma in [1/2, 1], at several heights t.
#
#   Q(u)  = (1/(2 pi^2)) sum_{m>=1} sin^2(pi m u)/m^3 = (S3 - Re Li3(e^{2 pi i u}))/(4 pi^2)
#   q0(u) = (u^2/2)(3/2 - log(2 pi u))                       (behaviour of Q at u -> 0)
#   T1(s) = int_0^1 (Q(u) - q0(u)) u^{-s-3} du
#   T2(s) = int_1^inf Q(u) u^{-s-3} du = int_0^1 Q(v) Hurwitz(s+3, 1+v) dv
#   T3(s) = (1/2)(1/s^2 - (3/2 - log 2 pi)/s)                 (= int_0^1 q0 u^{-s-3} du, continued)
# Check: J = -(G - A)/((s+1)(s+2)); with the identity G - A = (pi/s) cot(pi s/2) zeta(s)
# this is used only as an independent numerical check of T1+T2+T3.
import mpmath as mp
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

mp.mp.dps = 30
S3 = mp.zeta(3)
c0 = mp.mpf(3) / 2 - mp.log(2 * mp.pi)


def Q(u):
    return (S3 - mp.re(mp.polylog(3, mp.exp(2j * mp.pi * u)))) / (4 * mp.pi ** 2)


def q0(u):
    return u ** 2 / 2 * (mp.mpf(3) / 2 - mp.log(2 * mp.pi * u))


# Q(u) - q0(u) = sum_{j>=2} b_j u^{2j} for 0 <= u < 1, from
#   Re Li3(e^{ix}) = S3 - (x^2/2)(3/2 - log x) + sum_{j>=2} (-1)^j zeta(3-2j) x^{2j}/(2j)!   (|x| < 2 pi)
B = [None, None] + [-(1 / (4 * mp.pi ** 2)) * (-1) ** j * mp.zeta(3 - 2 * j) * (2 * mp.pi) ** (2 * j) / mp.factorial(2 * j)
                    for j in range(2, 120)]


def Qren(u):
    if u <= mp.mpf("0.5"):
        return mp.fsum(B[j] * u ** (2 * j) for j in range(2, 120))
    return Q(u) - q0(u)


def T1(s):
    f = lambda u: Qren(u) * u ** (-s - 3)
    return mp.quad(f, [0, mp.mpf("0.001"), mp.mpf("0.05"), mp.mpf("0.25"), mp.mpf("0.5"), mp.mpf("0.75"), 1])


def T2(s):
    f = lambda v: Q(v) * mp.zeta(s + 3, 1 + v)
    return mp.quad(f, [0, mp.mpf("0.25"), mp.mpf("0.5"), mp.mpf("0.75"), 1])


def T3(s):
    return (1 / s ** 2 - c0 / s) / 2


def J_check(s):
    return -(mp.pi / s) * mp.cot(mp.pi * s / 2) * mp.zeta(s) / ((s + 1) * (s + 2))


heights = [mp.mpf("14.134725141734693790"), mp.mpf(20), mp.mpf(50)]
sigmas = [mp.mpf(k) / 20 for k in range(10, 21)]  # 0.50, 0.55, ..., 1.00

rows = []
for t in heights:
    for sg in sigmas:
        s = mp.mpc(sg, t)
        a, b, c = T1(s), T2(s), T3(s)
        J = a + b + c
        Jc = J_check(s)
        rows.append((float(t), float(sg), a, b, c, J, Jc))
        print(f"t={float(t):9.4f} sigma={float(sg):.2f} |T1|={float(abs(a)):.6e} |T2|={float(abs(b)):.6e} "
              f"|T3|={float(abs(c)):.6e} |J|={float(abs(J)):.6e} |J-Jcheck|={float(abs(J-Jc)):.2e}", flush=True)

with open("J_terms_v2.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["t", "sigma", "Re_T1", "Im_T1", "Re_T2", "Im_T2", "Re_T3", "Im_T3",
                "Re_J", "Im_J", "abs_T1", "abs_T2", "abs_T3", "abs_J", "abs_J_minus_check"])
    for (t, sg, a, b, c, J, Jc) in rows:
        w.writerow([t, sg] + [mp.nstr(x, 12) for x in (mp.re(a), mp.im(a), mp.re(b), mp.im(b),
                                                         mp.re(c), mp.im(c), mp.re(J), mp.im(J),
                                                         abs(a), abs(b), abs(c), abs(J), abs(J - Jc))])

fig, axes = plt.subplots(1, len(heights), figsize=(15, 4.6), sharey=False)
for ax, t in zip(axes, heights):
    sel = [r for r in rows if abs(r[0] - float(t)) < 1e-9]
    x = [r[1] for r in sel]
    ax.semilogy(x, [float(abs(r[2])) for r in sel], "o-", label=r"$|T_1|$ ($0<u<1$, renormalized)")
    ax.semilogy(x, [float(abs(r[3])) for r in sel], "s-", label=r"$|T_2|$ ($u>1$)")
    ax.semilogy(x, [float(abs(r[4])) for r in sel], "^-", label=r"$|T_3|=|C(s)|$ (counterterm)")
    ax.semilogy(x, [float(abs(r[5])) for r in sel], "k*-", ms=9, label=r"$|J|=|T_1+T_2+T_3|$")
    ax.set_title(f"t = {float(t):.4f}")
    ax.set_xlabel(r"$\sigma$")
    ax.grid(True, which="both", alpha=0.3)
axes[0].set_ylabel("absolute value")
axes[0].legend(fontsize=8, loc="lower left")
fig.suptitle(r"The three terms of $J(s)=\int_0^\infty Q(u)\,u^{-s-3}\,du$ (regularized), $s=\sigma+it$")
fig.tight_layout()
fig.savefig("fig_J_terms_v2.png", dpi=160)
print("saved fig_J_terms_v2.png and J_terms_v2.csv")
