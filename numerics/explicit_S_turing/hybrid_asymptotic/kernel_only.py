# Search program (not a certificate): the smallest leading constant c_R1/(2 pi) of a kernel majorant without discs,
#   minimise c_R1/(2 pi)  subject to  f(b,t) <= U(b,t) on a grid of (b,t), refined by cutting planes, and 2 d c_R1 - 2 c_R2 >= 0,
# for the basis of order m and the given d; with the option 'rh' the constraint is imposed only at b = 0 (beta = 1/2), which is
# what would be needed if all zeros were on the critical line.  Used for Remark "On the infimum of the leading constant".
# Usage:  python3 kernel_only.py <m> <d1,d2,...> [rh]
import numpy as np, sys, time
from scipy.optimize import linprog
from lpcommon import f, F, basis, tgrid

def Gmat(d, B, bb, tt): return np.array([F(d+bb, tt, k, j)+F(d-bb, tt, k, j) for (k, j) in B]).T

def solve(d, m, rh=False, maxit=60, nb=26, tol=1e-9):
    B = basis(m); nB = len(B)
    sc = np.array([(d-0.5)**j for (_, j) in B])                 # scaling of the coefficients, for conditioning
    obj = np.zeros(nB); obj[0] = sc[0]/(2*np.pi)
    bgrid = np.array([0.0]) if rh else np.linspace(0, 0.5, nb)
    bb, tt = [a.ravel() for a in np.meshgrid(bgrid, tgrid(300.), indexing='ij')]
    A = Gmat(d, B, bb, tt)*sc; Fv = f(bb, tt, d)
    arow = np.zeros(nB); arow[0] = 2*d*sc[0]; arow[1] = -2*sc[1]
    bf = np.array([0.0]) if rh else np.linspace(0, 0.5, 201); tp = np.geomspace(1e-8, 3000., 12000); tf = np.concatenate([-tp[::-1], tp])
    for it in range(maxit):
        r = linprog(obj, A_ub=-np.vstack([A, arow]), b_ub=-np.concatenate([Fv, [0.0]]), bounds=[(None, None)]*nB, method='highs')
        assert r.status == 0, 'LP solver: '+r.message
        x = r.x; nbl = []; ntl = []; worst = -1
        for b in bf:   # violations on a finer grid -> new cutting planes (local maxima of the violation)
            v = f(b, tf, d)-Gmat(d, B, np.full_like(tf, b), tf)@(x*sc)
            worst = max(worst, v.max()); idx = np.nonzero((v > tol) & (v >= np.roll(v, 1)) & (v >= np.roll(v, -1)))[0]
            nbl += [b]*len(idx); ntl += list(tf[idx])
        if not nbl: break
        A = np.vstack([A, Gmat(d, B, np.array(nbl), np.array(ntl))*sc]); Fv = np.concatenate([Fv, f(np.array(nbl), np.array(ntl), d)])
    return r.fun, worst, it

if __name__ == '__main__':
    m = int(sys.argv[1]); ds = [float(x) for x in sys.argv[2].split(',')]; rh = len(sys.argv) > 3 and sys.argv[3] == 'rh'
    for d in ds:
        t0 = time.time(); val, w, it = solve(d, m, rh)
        print('m=%d d=%.2f %s C1(grid)=%.5f worst violation=%.1e it=%d  %.0fs' % (m, d, 'constraint at beta=1/2 only' if rh else 'all beta', val, w, it, time.time()-t0), flush=True)
