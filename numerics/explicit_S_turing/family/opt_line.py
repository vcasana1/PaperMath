# Optimize one explicit line |N(T)-main(T)| <= A1 log T + A3 for a target height L* = log T*.
# Kernel U = sum c_i G_i (basis R1..R_mR, I2..I_mI), d fixed. Convex program (SOCP, Clarabel):
#   minimize  (c_R1/2pi) L* + C_zeta(c) + z
#   s.t.      f(b,t) + eta/(1+t^2) <= U(b,t)      on a (b,t) grid, refined by cutting planes
#             2d c_R1 - 2 c_R2 >= eta              (behaviour at |t| -> oo)
#             z >= F_u(T;c), z >= F_l(T;c)         on a T grid in [1,1e6], and z >= limits at T = oo
# C_zeta(c) = sum_n Lambda(n) n^{-sigma1} || (A0(log n), B0(log n)) ||_2  (n <= n0) + quadrature of the tail.
# Output: JSON with exact binary coefficients, used by the certifiers.
import sys, json, math, time, numpy as np, cvxpy as cp, mpmath as mp
sys.path.insert(0, '../hybrid_asymptotic')
from lpm import f, F, tgrid

def basis(mR, mI): return [('R', j) for j in range(1, mR+1)] + [('I', j) for j in range(2, mI+1)]

def kernel_rows(d, B, bb, tt):
    G = np.array([F(d+bb, tt, k, j) + F(d-bb, tt, k, j) for (k, j) in B]).T
    return G, f(bb, tt, d)

def primes(N):
    s = np.ones(N+1, bool); s[:2] = False
    for i in range(2, int(N**0.5)+1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0]

def czeta_data(d, B, n0):
    s1 = 0.5+d; rows_a = []; rows_b = []; beta0 = []; w = []
    for p in primes(n0):
        lp = math.log(p); n = p; k = 1
        while n <= n0:
            L = k*lp
            rows_a.append([-(L**(j-1)/math.factorial(j-1))/math.pi if kk == 'R' else 0 for (kk, j) in B])
            rows_b.append([-(L**(j-1)/math.factorial(j-1))/math.pi if kk == 'I' else 0 for (kk, j) in B])
            beta0.append((math.exp(-d*L)-2)/(L*math.pi)); w.append(lp*math.exp(-s1*L)); n *= p; k += 1
    # tail n > n0: psi(x) ~ x, sum Lambda(n) g(n) ~ int g(x) dx = int g e^L dL ; Gauss-Legendre in L on [log n0, 700]
    xg, wg = np.polynomial.legendre.leggauss(400); a, b = math.log(n0), 700.0
    for x, ww in zip(xg, wg):
        L = (b-a)/2*x+(a+b)/2; wt = (b-a)/2*ww*math.exp((1-s1)*L)
        rows_a.append([-(L**(j-1)/math.factorial(j-1))/math.pi if kk == 'R' else 0 for (kk, j) in B])
        rows_b.append([-(L**(j-1)/math.factorial(j-1))/math.pi if kk == 'I' else 0 for (kk, j) in B])
        beta0.append((math.exp(-d*L)-2)/(L*math.pi)); w.append(wt)
    return np.array(rows_a), np.array(rows_b), np.array(beta0), np.array(w)

def elem_data(d, B, Tgrid):
    mp.mp.dps = 25
    s1r = mp.mpf(1)/2+d; s2r = mp.mpf(1)/2+2*d
    base = []; Phi = []
    for T in Tgrid:
        T = mp.mpf(T); s1 = s1r+1j*T; s2 = s2r+1j*T
        Ael = lambda s: mp.im(mp.log(s)+mp.log(s-1))-T/2*mp.log(mp.pi)+mp.im(mp.loggamma(s/2))
        base.append(float((2*Ael(s1)-Ael(s2))/mp.pi-T/(2*mp.pi)*mp.log(T/(2*mp.pi*mp.e))))
        row = []
        for (k, j) in B:
            if j == 1: D = 1/s1+1/(s1-1)-mp.log(mp.pi)/2+mp.psi(0, s1/2)/2
            else: D = s1**(-j)+(s1-1)**(-j)+(-1)**(j-1)/mp.factorial(j-1)/2**j*mp.psi(j-1, s1/2)
            row.append(float(mp.re(D)) if k == 'R' else float(-mp.im(D)))
        Phi.append(row)
    return np.array(base), np.array(Phi)

def optimize(d, mR, mI, Lstar, eta=2e-4, n0=20000, maxit=25, verbose=True):
    B = basis(mR, mI); nB = len(B); i1 = B.index(('R', 1)); i2 = B.index(('R', 2))
    isR = np.array([k == 'R' for k, _ in B])
    bb, tt = [a.ravel() for a in np.meshgrid(np.linspace(0, 0.5, 26), tgrid(300.), indexing='ij')]
    G, Fv = kernel_rows(d, B, bb, tt); Fv = Fv+eta/(1+tt**2)
    RA, RB, b0, w = czeta_data(d, B, n0)
    Tg = np.unique(np.concatenate([np.geomspace(1, 1e6, 260), [1.0]]))
    base, Phi = elem_data(d, B, Tg); logT = np.log(Tg)
    sc = np.array([(d-0.5)**j for (_, j) in B])        # scaling for conditioning
    bfine = np.linspace(0, 0.5, 201); tp = np.geomspace(1e-8, 3000., 12000); tfine = np.concatenate([-tp[::-1], tp])
    for it in range(maxit):
        y = cp.Variable(nB); z = cp.Variable(); c = cp.multiply(sc, y)
        cons = [G@c >= Fv, 2*d*c[i1]-2*c[i2] >= eta]
        sign = np.where(isR, 1.0, -1.0)
        Fu = base+(Phi@c)/math.pi-c[i1]/(2*math.pi)*logT
        Fl = -base+(Phi@cp.multiply(sign, c))/math.pi-c[i1]/(2*math.pi)*logT
        cons += [z >= Fu, z >= Fl, z >= 7/8-c[i1]/(2*math.pi)*math.log(2*math.pi)]
        Cz = cp.sum(cp.multiply(w, cp.norm(cp.vstack([RA@c, RB@c+b0]), 2, axis=0)))
        obj = c[i1]/(2*math.pi)*Lstar+Cz+z
        prob = cp.Problem(cp.Minimize(obj), cons); prob.solve(solver=cp.CLARABEL)
        cv = sc*y.value
        nb = []; nt = []; worst = -1
        for b in bfine:
            Gr, Fr = kernel_rows(d, B, np.full_like(tfine, b), tfine); v = Fr+eta/(1+tfine**2)-Gr@cv; worst = max(worst, v.max())
            idx = np.where((v > 0) & (v >= np.roll(v, 1)) & (v >= np.roll(v, -1)))[0]; nb += [b]*len(idx); nt += list(tfine[idx])
        if verbose: print('  it %d obj=%.5f C1=%.5f Cz~%.4f z=%.4f worst=%.2e' % (it, prob.value, cv[i1]/(2*math.pi), Cz.value, z.value, worst), flush=True)
        if not nb: break
        G2, F2 = kernel_rows(d, B, np.array(nb), np.array(nt)); G = np.vstack([G, G2]); Fv = np.concatenate([Fv, F2+eta/(1+np.array(nt)**2)])
    return dict(d=d, B=B, c=list(map(float, cv)), C1=float(cv[i1]/(2*math.pi)), Cz_est=float(Cz.value), z_est=float(z.value),
                A3_est=float(Cz.value+z.value), Lstar=Lstar, eta=eta, prof='B', discs=[], kappa=[], J=[], m=max(j for _, j in B))

if __name__ == '__main__':
    d = float(sys.argv[1]); mR = int(sys.argv[2]); mI = int(sys.argv[3]); Ls = float(sys.argv[4]); out = sys.argv[5]
    t0 = time.time(); r = optimize(d, mR, mI, Ls)
    print('RESULT d=%.3f mR=%d mI=%d L*=%g  A1=%.5f A3~%.4f  value@L*~%.4f  (%.0fs)' % (d, mR, mI, Ls, r['C1'], r['A3_est'], r['C1']*Ls+r['A3_est'], time.time()-t0), flush=True)
    json.dump(r, open(out, 'w'))
