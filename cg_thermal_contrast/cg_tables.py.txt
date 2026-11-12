"""Numbers quoted in the note on the constant C_g and the Ramsey contrast of a thermal mode.

Python 3 with mpmath.  Run:  python3 cg_tables.py > cg_tables_output.txt
Notation: nbar mean occupation, q = nbar/(nbar+1), p0 = 1/(nbar+1), tau = log(1+1/nbar),
c_m(s) = int_1^inf cos(2 pi m u) u^(-s-1) du = Re E_{s+1}(-2 pi i m),
G(s) = -sum_m c_m(s)/m,  C_g = log 2 - G(1),  V_s = geometric visibility of order s.
"""
import mpmath as mp

mp.mp.dps = 30


def c(m, s=1):
    return mp.re(mp.expint(mp.mpf(s) + 1, -2j * mp.pi * m))


def G(s):
    return -mp.nsum(lambda m: c(m, s) / m, [1, mp.inf])


def minus_sGq(nbar, s=1):
    q = mp.mpf(nbar) / (nbar + 1)
    return s * mp.nsum(lambda m: q ** m * c(m, s) / m, [1, mp.inf])


if __name__ == '__main__':
    G1 = G(1)
    Cg = mp.log(2) - G1
    s1 = mp.pi ** 2 / 12 - mp.mpf(3) / 4
    print('G(1)            =', mp.nstr(G1, 20))
    print('C_g = log2-G(1) =', mp.nstr(Cg, 20))
    print('exp(C_g)/2      =', mp.nstr(mp.e ** Cg / 2, 20))
    print('C_g - log 2     =', mp.nstr(Cg - mp.log(2), 20))
    print('pi^2/12 - 3/4   =', mp.nstr(s1, 20))
    print()
    print('Sharp constants exp(-s G(s)) of Theorem 4.1')
    print('    s        G(s)          exp(-s G(s))')
    for s in ['0.5', '1', '2', '3']:
        g = G(mp.mpf(s))
        print('  %4s  %s  %s' % (s, mp.nstr(g, 12), mp.nstr(mp.e ** (-mp.mpf(s) * g), 12)))
    print()
    print('Geometric visibility of order 1, ratio to the vacuum probability, hot expansion')
    print('    nbar        p0            V_1          V_1/p0     hot formula    R(tau)      bound on R')
    for nb in ['0.01', '0.1', '1', '5', '20', '100', '1000']:
        n = mp.mpf(nb)
        p0 = 1 / (n + 1)
        q = n / (n + 1)
        tau = mp.log(1 + 1 / n)
        S = minus_sGq(n)
        V = p0 * mp.e ** S
        hot = mp.e ** Cg / 2 * p0 * q ** s1
        R = S - (Cg - mp.log(2)) + s1 * tau
        bound = tau ** 2 / mp.pi ** 2 * (mp.mpf(5) / 2 + mp.log(1 / tau) / 2) if tau <= 1 else None
        print('  %6s  %s  %s  %s  %s  %s  %s' % (nb, mp.nstr(p0, 10), mp.nstr(V, 10), mp.nstr(V / p0, 8),
              mp.nstr(hot, 10), mp.nstr(R, 6), mp.nstr(bound, 6) if bound is not None else '(tau > 1)'))
    print()
    print('Bracket of Corollary 4.2 for nbar = 20:')
    n = mp.mpf(20)
    V = mp.e ** minus_sGq(n) / (n + 1)
    print('  1/V_1 - 1 =', mp.nstr(1 / V - 1, 10), '   exp(C_g)/(2 V_1) - 1 =', mp.nstr(mp.e ** Cg / (2 * V) - 1, 10))
    print()
    print('Product of contrasts at the harmonic delays N/k (Proposition 5.2), nbar = 1')
    n = mp.mpf(1)
    A4 = 4 * n * (n + 1)
    target = mp.log(1 / (n + 1)) + minus_sGq(n)
    L = mp.log(2 * n + 1)
    print('  log V_1 =', mp.nstr(target, 12))
    print('       N    (1/N) log P(N)    difference     bound')
    for N in [10, 100, 1000, 10000]:
        tot = mp.fsum(-mp.log(1 + A4 * mp.sin(mp.pi * mp.mpf(N) / k) ** 2) / 2 for k in range(1, N))
        print('  %6d  %s  %s  %s' % (N, mp.nstr(tot / N, 12), mp.nstr(tot / N - target, 4),
              mp.nstr(L * (2 * mp.sqrt(2) / mp.sqrt(N) + mp.mpf(1) / N), 4)))
