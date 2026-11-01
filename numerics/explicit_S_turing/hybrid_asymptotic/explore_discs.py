# Search program (not a certificate): the hybrid of the kernel majorant with Jensen discs.
# Linear programme in (c_iota, kappa_k):
#   minimise  c_R1/(2 pi) + (1/pi) sum_k kappa_k J_k
#   subject to  f(b,t) + eta/(1+t^2) <= U(b,t) + sum_k kappa_k W_k(b,t)  on a grid of (b,t), refined by cutting planes,
#               2 d c_R1 - 2 c_R2 >= eta  (limit of t^2 U at |t| -> oo),  kappa_k >= 0,
# with J_k = (1/pi) int_0^pi e(c_k + R_k cos th) dth for the profile e (PROF=P: e_P of profile_published.py; PROF=B: the
# Bourgain profile of lpcommon.bourgain_nodes).  Candidate discs: the family 'vwide' described in the article.
# Usage:  PROF=P python3 explore_discs.py <m> <d> [eta]      -> expl_m<m>_d<d>_<PROF>_eta<eta>.json (input of certify_hybrid.py)
import numpy as np, sys, os, json, time, math
from scipy.optimize import linprog
from scipy import sparse
from lpcommon import f, F, basis, tgrid, bourgain_nodes, J_float

PROF = os.environ.get('PROF', 'P')
if PROF == 'P':
    from profile_published import nodes_published; nodes = nodes_published()
elif PROF == 'B': nodes = bourgain_nodes()
else: raise SystemExit('PROF must be P or B')

def Wmat(discs, bb, tt):
    # sparse matrix of W_k(b,t) = log^+(R_k / sqrt((c_k - 1/2 - b)^2 + (t + v_k)^2))
    rows = []; cols = []; vals = []
    for k, (c, R, v) in enumerate(discs):
        dist = np.sqrt((c-0.5-bb)**2+(tt+v)**2)
        w = np.log(R/np.maximum(dist, 1e-300)); i = np.nonzero(w > 0)[0]
        rows.append(i); cols.append(np.full(len(i), k)); vals.append(w[i])
    r = np.concatenate(rows) if rows else np.zeros(0, int)
    return sparse.csr_matrix((np.concatenate(vals) if vals else [], (r, np.concatenate(cols) if cols else [])), shape=(len(bb), len(discs)))
def Gmat(d, B, bb, tt): return np.array([F(d+bb, tt, k, j)+F(d-bb, tt, k, j) for (k, j) in B]).T

def solve(d, m, discs, eta=0.0, maxit=30, nb=26):
    B = basis(m); nB = len(B)
    sc = np.array([(d-0.5)**j for (_, j) in B])                 # scaling of the coefficients, for conditioning
    J = np.array([J_float(nodes, c, R) for c, R, v in discs])
    obj = np.concatenate([[sc[0]/(2*np.pi)], np.zeros(nB-1), J/np.pi])
    bb, tt = [a.ravel() for a in np.meshgrid(np.linspace(0, 0.5, nb), tgrid(300., 500, 300), indexing='ij')]
    def block(bb, tt): return sparse.hstack([sparse.csr_matrix(Gmat(d, B, bb, tt)*sc), Wmat(discs, bb, tt)]).tocsr(), f(bb, tt, d)+eta/(1+tt**2)
    A, Fv = block(bb, tt)
    arow = np.zeros(nB+len(discs)); arow[0] = 2*d*sc[0]; arow[1] = -2*sc[1]
    bf = np.linspace(0, 0.5, 101); tp = np.geomspace(1e-7, 3000., 6000); tf = np.concatenate([-tp[::-1], tp])
    for it in range(maxit):
        r = linprog(obj, A_ub=-sparse.vstack([A, sparse.csr_matrix(arow)]), b_ub=-np.concatenate([Fv, [eta]]),
                    bounds=[(None, None)]*nB+[(0, None)]*len(discs), method='highs')
        assert r.status == 0, 'LP solver: '+r.message
        x = r.x; used = np.nonzero(x[nB:] > 1e-12)[0]; du = [discs[k] for k in used]
        nbl = []; ntl = []; worst = -1
        for b in bf:   # violations on a finer grid -> new cutting planes (local maxima of the violation)
            v = f(b, tf, d)+eta/(1+tf**2)-Gmat(d, B, np.full_like(tf, b), tf)@(x[:nB]*sc)
            if len(used): v = v-Wmat(du, np.full_like(tf, b), tf)@x[nB+used]
            worst = max(worst, v.max()); idx = np.nonzero((v > 0) & (v >= np.roll(v, 1)) & (v >= np.roll(v, -1)))[0]
            nbl += [b]*len(idx); ntl += list(tf[idx])
        if not nbl: break
        A2, F2 = block(np.array(nbl), np.array(ntl)); A = sparse.vstack([A, A2]).tocsr(); Fv = np.concatenate([Fv, F2])
    xs = x.copy(); xs[:nB] *= sc
    return r.fun, xs, B, J, worst, it

def family_vwide():
    # centres c, radii R = c - 1 + x with R <= c - 1/2, vertical offsets v
    C = [1.03, 1.06, 1.1, math.log(3), 1.15, 1.2, 1.25, 1.3, 1.4, 1.5, math.log(5), 2.0, math.e, 3.0]
    out = []
    for c in C:
        for R in [c-1+x for x in [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]]:
            if R <= 0 or R > c-0.5+1e-12: continue
            for v in [-2, -1.6, -1.3, -1.0, -0.8, -0.65, -0.5, -0.35, -0.2, 0, 0.2, 0.35, 0.5, 0.65, 0.8, 1.0, 1.3, 1.6, 2]:
                if abs(v) <= R+2.5: out.append((c, R, float(v)))
    return out

if __name__ == '__main__':
    m = int(sys.argv[1]); d = float(sys.argv[2]); eta = float(sys.argv[3]) if len(sys.argv) > 3 else 0.0
    discs = family_vwide(); t0 = time.time()
    val, x, B, J, w, it = solve(d, m, discs, eta)
    nB = len(B); keep = [k for k in range(len(discs)) if x[nB+k] > 1e-10]
    used_c = sorted(set(round(discs[k][0], 4) for k in keep))
    print('m=%d d=%.3f prof=%s eta=%g ndiscs=%d C(grid)=%.6f kernel=%.6f worst violation=%.2e it=%d used=%d centres=%s  %.0fs'
          % (m, d, PROF, eta, len(discs), val, x[0]/(2*np.pi), w, it, len(keep), used_c, time.time()-t0), flush=True)
    json.dump({'m': m, 'd': d, 'prof': PROF, 'eta': eta, 'B': B, 'c': list(x[:nB]), 'discs': [discs[k] for k in keep], 'kappa': [x[nB+k] for k in keep],
               'J_grid': [J[k] for k in keep], 'C_grid_objective': val}, open('expl_m%d_d%.2f_%s_eta%g.json' % (m, d, PROF, eta), 'w'))
