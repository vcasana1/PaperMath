# Exploration (not a certificate): enlarged kernel basis. Each basis function is
#   G_{X,j,d',tau}(b,t) = F_X(d'+b, t+tau) + F_X(d'-b, t+tau),   d' > 1/2,
# whose sum over the zeros is 2 sum_rho F_X(s'-rho) with s' = 1/2+d'+i(T+tau); it equals log T + O(1) for (R,1) and O(1)
# otherwise (Lemma "Sums of the kernel" at the point s'). Objective: (sum of all (R,1) coefficients)/(2pi) + sum kappa J/pi.
# For the lower bound the same data are used with t -> -t (tau -> -tau), which does not change the objective.
import numpy as np, sys, json, time
from scipy.optimize import linprog
from scipy import sparse
from lpm import f, F
from explore_discs import Wmat, Jf, family, tgrid, PROF
def Gcol(bb, tt, X, j, dp, tau): return F(dp+bb, tt+tau, X, j)+F(dp-bb, tt+tau, X, j)
def basis(d, m, extra):
    B = [('R', j, d, 0.0) for j in range(1, m+1)]+[('I', j, d, 0.0) for j in range(2, m+1)]
    if extra == 'none': return B
    taus = [-2, -1.5, -1, -0.6, -0.3, 0.3, 0.6, 1, 1.5, 2]; dps = [0.6, 0.75, d, 1.2, 1.6]
    for dp in dps:
        for tau in ([0.0] if dp != d else [])+taus:
            for (X, j) in [('R', 1), ('R', 2), ('I', 2), ('R', 3), ('I', 3)]:
                B.append((X, j, dp, float(tau)))
    return B
def solve(d, m, extra, fam, eta=0.0, maxit=30, nb=26):
    B = basis(d, m, extra); nB = len(B); discs = family(fam) if fam != 'nodisc' else []
    sc = np.array([(dp-0.5)**j for (_, j, dp, _) in B]); J = np.array([Jf(c, R) for c, R, v in discs])
    isR1 = np.array([1.0 if (X == 'R' and j == 1) else 0.0 for (X, j, _, _) in B])
    obj = np.concatenate([isR1*sc/(2*np.pi), J/np.pi])
    def G(bb, tt): return np.array([Gcol(bb, tt, X, j, dp, tau) for (X, j, dp, tau) in B]).T*sc
    bb, tt = [a.ravel() for a in np.meshgrid(np.linspace(0, 0.5, nb), tgrid(300.), indexing='ij')]
    def block(bb, tt):
        M = sparse.csr_matrix(G(bb, tt))
        if discs: M = sparse.hstack([M, Wmat(discs, bb, tt)])
        return M.tocsr(), f(bb, tt, d)+eta/(1+tt**2)
    A, Fv = block(bb, tt)
    # |t| -> oo: t^2 (U - f) -> sum over R1 of 2 c d' - sum over R2 of 2 c - 4 d^3*0 ... ; impose lim t^2 U >= eta (f = O(t^-3))
    arow = np.zeros(nB+len(discs))
    for i, (X, j, dp, tau) in enumerate(B):
        if X == 'R' and j == 1: arow[i] = 2*dp*sc[i]
        if X == 'R' and j == 2: arow[i] = -2*sc[i]
        if X == 'I' and j == 2: arow[i] = 0.0   # -Im (x+it)^-2 = 2xt/(x^2+t^2)^2 ~ 2x/t^3
    bf = np.linspace(0, 0.5, 101); tp = np.geomspace(1e-7, 3000., 6000); tf = np.concatenate([-tp[::-1], tp])
    for it in range(maxit):
        r = linprog(obj, A_ub=-sparse.vstack([A, sparse.csr_matrix(arow)]), b_ub=-np.concatenate([Fv, [eta]]),
                    bounds=[(None, None)]*nB+[(0, None)]*len(discs), method='highs')
        if r.status != 0: print('status', r.status, r.message); return None
        x = r.x; used = np.nonzero(x[nB:] > 1e-12)[0]; du = [discs[k] for k in used]
        nbl = []; ntl = []; worst = -1
        for b in bf:
            bv = np.full_like(tf, b); v = f(b, tf, d)+eta/(1+tf**2)-G(bv, tf)@x[:nB]
            if len(used): v = v-Wmat(du, bv, tf)@x[nB+used]
            worst = max(worst, v.max()); idx = np.nonzero((v > 0) & (v >= np.roll(v, 1)) & (v >= np.roll(v, -1)))[0]
            nbl += [b]*len(idx); ntl += list(tf[idx])
        if not nbl: break
        A2, F2 = block(np.array(nbl), np.array(ntl)); A = sparse.vstack([A, A2]).tocsr(); Fv = np.concatenate([Fv, F2])
    xs = x.copy(); xs[:nB] *= sc
    kern = float(np.sum(isR1*xs[:nB])/(2*np.pi))
    return r.fun, xs, B, discs, J, worst, it, kern
if __name__ == '__main__':
    m = int(sys.argv[1]); d = float(sys.argv[2]); extra = sys.argv[3]; fam = sys.argv[4]; eta = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
    t0 = time.time(); val, x, B, discs, J, w, it, kern = solve(d, m, extra, fam, eta)
    nB = len(B); keep = [k for k in range(len(discs)) if x[nB+k] > 1e-10]
    nzb = [B[i] for i in range(nB) if abs(x[i]) > 1e-9 and B[i][3] != 0.0 or (abs(x[i]) > 1e-9 and B[i][2] != d)]
    print('m=%d d=%.3f extra=%s fam=%s eta=%g nB=%d ndiscs=%d C=%.6f kernel=%.6f viol=%.2e it=%d used=%d extra_used=%d  %.0fs' % (m, d, extra, fam, eta, nB, len(discs), val, kern, w, it, len(keep), len(nzb), time.time()-t0), flush=True)
    json.dump({'m': m, 'd': d, 'prof': PROF, 'eta': eta, 'B': B, 'c': list(x[:nB]), 'discs': [discs[k] for k in keep], 'kappa': [x[nB+k] for k in keep], 'J': [J[k] for k in keep], 'C': val},
              open('basis_m%d_d%.2f_%s_%s_%s_eta%g.json' % (m, d, extra, fam, PROF, eta), 'w'))
