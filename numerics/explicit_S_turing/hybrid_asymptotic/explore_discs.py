# Exploration (not a certificate): kernel + Jensen discs, wide families of centres c > 1 (incl. log 3, log 5, 2, e, 3, ...),
# sparse LP with cutting planes. Weight per zero: W(1/2+|b|) (+ W(1/2-|b|) if the disc crosses Re s = 1/2), cost 2J log T,
# i.e. objective c_R1/(2pi) + sum kappa_k J_k/pi as in certify_hybrid.py. Profile: Bourgain nodes, reflected for sigma<1/2.
import numpy as np, sys, json, time
from scipy.optimize import linprog
from scipy import sparse
from lpm import f, F, bourgain_nodes
import os
PROF = os.environ.get('PROF', 'B')
if PROF == 'T':
    from profile_tty import nodes_tty; nodes = nodes_tty()
else: nodes = bourgain_nodes()
XS = np.array([float(a) for a, _ in nodes]); ES = np.array([float(e) for _, e in nodes])
def prof(s):
    s = np.asarray(s, float); out = np.zeros_like(s)
    m = (s >= 0.5) & (s < 1); out[m] = np.interp(s[m], XS, ES)
    l = s < 0.5; out[l] = 0.5 - s[l] + np.interp(1 - s[l], XS, ES)
    return out
def Jf(c, R, n=40001):
    th = np.linspace(0, np.pi, n); return np.trapezoid(prof(c + R*np.cos(th)), th)/np.pi
def Wmat(discs, bb, tt):
    rows = []; cols = []; vals = []
    for k, (c, R, v) in enumerate(discs):
        for sgn in (1, -1):
            if sgn == -1 and c - R >= 0.5: continue
            dist = np.sqrt((c - 0.5 - sgn*bb)**2 + (tt + v)**2)
            w = np.log(R/np.maximum(dist, 1e-300)); i = np.nonzero(w > 0)[0]
            rows.append(i); cols.append(np.full(len(i), k)); vals.append(w[i])
    r = np.concatenate(rows) if rows else np.zeros(0, int)
    return sparse.csr_matrix((np.concatenate(vals) if vals else [], (r, np.concatenate(cols) if cols else [])), shape=(len(bb), len(discs)))
def Gmat(d, B, bb, tt): return np.array([F(d+bb, tt, k, j)+F(d-bb, tt, k, j) for (k, j) in B]).T
def tgrid(tmax):
    p = np.unique(np.concatenate([[1e-9], np.geomspace(1e-4, tmax, 500), np.linspace(0, 4, 300)[1:]])); return np.concatenate([-p[::-1], p])
def solve(d, m, discs, eta=0.0, maxit=30, nb=26):
    B = [('R', j) for j in range(1, m+1)]+[('I', j) for j in range(2, m+1)]; nB = len(B)
    sc = np.array([(d-0.5)**j for (_, j) in B]); J = np.array([Jf(c, R) for c, R, v in discs])
    obj = np.concatenate([[sc[0]/(2*np.pi)], np.zeros(nB-1), J/np.pi])
    bb, tt = [a.ravel() for a in np.meshgrid(np.linspace(0, 0.5, nb), tgrid(300.), indexing='ij')]
    def block(bb, tt): return sparse.hstack([sparse.csr_matrix(Gmat(d, B, bb, tt)*sc), Wmat(discs, bb, tt)]).tocsr(), f(bb, tt, d)+eta/(1+tt**2)
    A, Fv = block(bb, tt)
    arow = np.zeros(nB+len(discs)); arow[0] = 2*d*sc[0]; arow[1] = -2*sc[1]
    bf = np.linspace(0, 0.5, 101); tp = np.geomspace(1e-7, 3000., 6000); tf = np.concatenate([-tp[::-1], tp])
    for it in range(maxit):
        r = linprog(obj, A_ub=-sparse.vstack([A, sparse.csr_matrix(arow)]), b_ub=-np.concatenate([Fv, [eta]]),
                    bounds=[(None, None)]*nB+[(0, None)]*len(discs), method='highs')
        if r.status != 0: return None
        x = r.x; used = np.nonzero(x[nB:] > 1e-12)[0]; du = [discs[k] for k in used]
        nbl = []; ntl = []; worst = -1
        for b in bf:
            v = f(b, tf, d)+eta/(1+tf**2)-Gmat(d, B, np.full_like(tf, b), tf)@(x[:nB]*sc)
            if len(used): v = v-Wmat(du, np.full_like(tf, b), tf)@x[nB+used]
            worst = max(worst, v.max()); idx = np.nonzero((v > 0) & (v >= np.roll(v, 1)) & (v >= np.roll(v, -1)))[0]
            nbl += [b]*len(idx); ntl += list(tf[idx])
        if not nbl: break
        A2, F2 = block(np.array(nbl), np.array(ntl)); A = sparse.vstack([A, A2]).tocsr(); Fv = np.concatenate([Fv, F2])
    xs = x.copy(); xs[:nB] *= sc
    return r.fun, xs, B, J, worst, it
def family(name):
    import math
    if name == 'old':   # the m=10 certified family
        return [(c, R, v) for c in [1.03, 1.06, 1.1, 1.15, 1.2, 1.25, 1.3, 1.4] for R in [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5, 0.6] if c-R >= 0.5 and c-R < 1 for v in [-0.5, -0.3, -0.15, 0, 0.15, 0.3, 0.5]]
    if name == 'vwide':   # centres incl. log 3, log 5, 2, e, 3; vertical offsets up to |v| = 2
        C = [1.03, 1.06, 1.1, math.log(3), 1.15, 1.2, 1.25, 1.3, 1.4, 1.5, math.log(5), 2.0, math.e, 3.0]
        out = []
        for c in C:
            for R in [c-1+x for x in [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]]:
                if R <= 0 or R > c-0.5+1e-12: continue
                for v in [-2, -1.6, -1.3, -1.0, -0.8, -0.65, -0.5, -0.35, -0.2, 0, 0.2, 0.35, 0.5, 0.65, 0.8, 1.0, 1.3, 1.6, 2]:
                    if abs(v) <= R+2.5: out.append((c, R, float(v)))
        return out
    C = [1.01, 1.02, 1.04, 1.06, 1.08, 1.1, 1.13, 1.16, 1.2, 1.25, 1.3, 1.35, 1.4, 1.5, math.log(3), math.log(5), 1.75, 2.0, math.e/1.25, 2.5, math.e, 3.0, math.pi, 4.0, 5.0]
    out = []
    for c in sorted(set(C)):
        rmax = c-0.5 if name != 'cross' else c-0.35
        Rs = sorted(set([c-1+x for x in [0.02, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]] + ([c-0.4, c-0.45] if name == 'cross' else [])))
        for R in Rs:
            if R <= 0 or R > rmax+1e-12: continue
            h = R if R < 1 else min(R, 2.0)
            for v in np.linspace(-0.8*h, 0.8*h, 9 if R < 0.5 else 7): out.append((c, R, float(v)))
    return out
if __name__ == '__main__':
    m = int(sys.argv[1]); d = float(sys.argv[2]); fam = sys.argv[3]; eta = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
    discs = family(fam); t0 = time.time()
    res = solve(d, m, discs, eta)
    val, x, B, J, w, it = res; nB = len(B); keep = [k for k in range(len(discs)) if x[nB+k] > 1e-10]
    used_c = sorted(set(round(discs[k][0], 4) for k in keep))
    print('m=%d d=%.3f fam=%s eta=%g ndiscs=%d C=%.6f kernel=%.6f viol=%.2e it=%d used=%d centres=%s  %.0fs' % (m, d, fam, eta, len(discs), val, x[0]/(2*np.pi), w, it, len(keep), used_c, time.time()-t0), flush=True)
    json.dump({'m': m, 'd': d, 'prof': PROF, 'eta': eta, 'B': B, 'c': list(x[:nB]), 'discs': [discs[k] for k in keep], 'kappa': [x[nB+k] for k in keep], 'J': [J[k] for k in keep], 'C': val},
              open('expl_m%d_d%.2f_%s_%s_eta%g.json' % (m, d, fam, PROF, eta), 'w'))
