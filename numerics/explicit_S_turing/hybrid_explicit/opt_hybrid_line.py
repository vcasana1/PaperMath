# Explicit hybrid line (exploration/optimisation; certification is separate).
# Bound, for T >= T1:  |N(T) - main(T)| <= A1 L + B loglog T + A3,  L = log T, with
#   A1 = c_R1/(2pi) + (1/pi) sum kappa_k J_k,   B = (1/pi) sum kappa_k g_k,
#   A3 = C_zeta(c) + sup F + (1/pi) sum kappa_k a_k  (+ small explicit corrections, see README),
# where, on the Jensen circle of disc k, log|zeta(sigma+it)| <= e(sigma) log t + g(sigma) loglog t + a(sigma):
#   1/2 <= sigma <= 1: Trudgian's Phragmen-Lindelof Lemma 3 (JNT 2014, arXiv:1208.5846) applied to (s-1)zeta(s)
#     between the lines sigma=1/2 (Hiary-Patel-Yang 2024: 0.618 t^{1/6} log t), sigma_k = 1-k/(2^k-2), k=4..9
#     (Yang 2023, arXiv:2301.03165: 1.546 t^{1/(2^k-2)} log t) and sigma=1 (Trudgian 2014: (3/4) log t), t >= 3;
#     e, a are linear between nodes and g = 1;
#   sigma > 1: log|zeta| <= log zeta(sigma);
#   lower bound at the centre: log|zeta(s0)| >= log(zeta(2c)/zeta(c)).
# Objective at target L*: A1 L* + B log L* + A3.
import sys, json, math, time, numpy as np, cvxpy as cp, mpmath as mp
sys.path.insert(0, '../family'); sys.path.insert(0, '../hybrid_asymptotic')
from opt_line import basis, kernel_rows, czeta_data, elem_data
from lpm import f, F, tgrid
from explore_discs import Wmat
XN = [0.5]+[1-k/(2**k-2) for k in range(4, 10)]+[1.0]
XE = [1/6]+[1/(2**k-2) for k in range(4, 10)]+[0.0]
XA = [math.log(0.618)]+[math.log(1.546)]*6+[math.log(0.75)]
def disc_coeffs(c, R, n=20001):
    th = np.linspace(0, np.pi, n); s = c+R*np.cos(th); ins = s <= 1
    e = np.where(ins, np.interp(s, XN, XE), 0.0); a = np.where(ins, np.interp(s, XN, XA), 0.0)
    lz = np.zeros_like(s); m = ~ins; lz[m] = [float(mp.log(mp.zeta(x))) for x in s[m]] if m.any() else []
    J = np.trapezoid(e, th)/np.pi; G = np.trapezoid(ins.astype(float), th)/np.pi
    Aa = np.trapezoid(a+lz, th)/np.pi+float(mp.log(mp.zeta(c)/mp.zeta(2*c)))
    return J, G, Aa
def optimize(d, mR, mI, Lstar, discs, eta=2e-4, n0=20000, maxit=25):
    B = basis(mR, mI); nB = len(B); i1 = B.index(('R', 1)); i2 = B.index(('R', 2)); isR = np.array([k == 'R' for k, _ in B])
    DC = np.array([disc_coeffs(c, R) for c, R, v in discs]); K = len(discs)
    bb, tt = [a.ravel() for a in np.meshgrid(np.linspace(0, 0.5, 26), tgrid(300.), indexing='ij')]
    G, Fv = kernel_rows(d, B, bb, tt); Fv = Fv+eta/(1+tt**2); W = Wmat(discs, bb, tt).toarray()
    RA, RB, b0, w = czeta_data(d, B, n0)
    Tg = np.unique(np.concatenate([np.geomspace(1, 1e6, 260), [1.0]])); base, Phi = elem_data(d, B, Tg); logT = np.log(Tg)
    sc = np.array([(d-0.5)**j for (_, j) in B])
    bf = np.linspace(0, 0.5, 201); tp = np.geomspace(1e-8, 3000., 12000); tf = np.concatenate([-tp[::-1], tp])
    for it in range(maxit):
        y = cp.Variable(nB); z = cp.Variable(); kap = cp.Variable(K, nonneg=True); c = cp.multiply(sc, y)
        cons = [G@c+W@kap >= Fv, 2*d*c[i1]-2*c[i2] >= eta]
        sign = np.where(isR, 1.0, -1.0)
        Fu = base+(Phi@c)/math.pi-c[i1]/(2*math.pi)*logT; Fl = -base+(Phi@cp.multiply(sign, c))/math.pi-c[i1]/(2*math.pi)*logT
        cons += [z >= Fu, z >= Fl, z >= 7/8-c[i1]/(2*math.pi)*math.log(2*math.pi)]
        Cz = cp.sum(cp.multiply(w, cp.norm(cp.vstack([RA@c, RB@c+b0]), 2, axis=0)))
        discterm = (DC[:, 0]*Lstar+DC[:, 1]*math.log(Lstar)+DC[:, 2])@kap/math.pi
        obj = c[i1]/(2*math.pi)*Lstar+Cz+z+discterm
        prob = cp.Problem(cp.Minimize(obj), cons); prob.solve(solver=cp.CLARABEL)
        cv = sc*y.value; kv = np.maximum(kap.value, 0)
        nb = []; nt = []; worst = -1
        for b in bf:
            Gr, Fr = kernel_rows(d, B, np.full_like(tf, b), tf); v = Fr+eta/(1+tf**2)-Gr@cv-Wmat(discs, np.full_like(tf, b), tf)@kv
            worst = max(worst, v.max()); idx = np.where((v > 0) & (v >= np.roll(v, 1)) & (v >= np.roll(v, -1)))[0]; nb += [b]*len(idx); nt += list(tf[idx])
        print('  it %d obj=%.4f C1=%.5f A1=%.5f B=%.4f worst=%.2e' % (it, prob.value, cv[i1]/(2*math.pi), cv[i1]/(2*math.pi)+DC[:, 0]@kv/math.pi, DC[:, 1]@kv/math.pi, worst), flush=True)
        if not nb: break
        G2, F2 = kernel_rows(d, B, np.array(nb), np.array(nt)); G = np.vstack([G, G2]); Fv = np.concatenate([Fv, F2+eta/(1+np.array(nt)**2)])
        W = np.vstack([W, Wmat(discs, np.array(nb), np.array(nt)).toarray()])
    keep = [k for k in range(K) if kv[k] > 1e-10]
    A1 = cv[i1]/(2*math.pi)+DC[:, 0]@kv/math.pi; Bc = DC[:, 1]@kv/math.pi; A3 = Cz.value+z.value+DC[:, 2]@kv/math.pi
    return dict(d=d, B=B, c=list(map(float, cv)), C1=float(cv[i1]/(2*math.pi)), A1=float(A1), Bll=float(Bc), A3_est=float(A3),
                Cz_est=float(Cz.value), z_est=float(z.value), Lstar=Lstar, eta=eta, prof='X',
                discs=[discs[k] for k in keep], kappa=[float(kv[k]) for k in keep], DC=[list(map(float, DC[k])) for k in keep],
                val=float(A1*Lstar+Bc*math.log(Lstar)+A3))
if __name__ == '__main__':
    d = float(sys.argv[1]); mR = int(sys.argv[2]); mI = int(sys.argv[3]); Ls = float(sys.argv[4]); dfile = sys.argv[5]; out = sys.argv[6]
    discs = [tuple(x) for x in json.load(open(dfile))]
    t0 = time.time(); r = optimize(d, mR, mI, Ls, discs)
    print('RESULT d=%.3f m=(%d,%d) L*=%g ndiscs=%d used=%d: |N-main| <= %.5f L + %.4f loglog T + %.4f   val@L*=%.3f  (kernel C1=%.5f)  %.0fs' % (
        d, mR, mI, Ls, len(discs), len(r['discs']), r['A1'], r['Bll'], r['A3_est'], r['val'], r['C1'], time.time()-t0), flush=True)
    json.dump(r, open(out, 'w'))
