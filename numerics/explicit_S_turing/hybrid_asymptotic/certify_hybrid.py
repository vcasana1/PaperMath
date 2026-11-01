# Certification (Arb ball arithmetic, python-flint, 256 bits) of the kernel inequality
#   f(b,t) <= U(b,t) + sum_k kappa_k W_k(b,t)     for 0 <= b <= 1/2, t != 0,
# with f(b,t) = 2 atan((d+b)/t) + 2 atan((d-b)/t) - atan((2d+b)/t) - atan((2d-b)/t),
#      U(b,t) = sum_iota c_iota [F_iota(d+b,t) + F_iota(d-b,t)],  F_Rj = Re (x+it)^(-j),  F_Ij = -Im (x+it)^(-j),
#      W_k(b,t) = log^+( R_k / sqrt((c_k-1/2-b)^2 + (t+v_k)^2) ),
# and of the constant C_H = c_R1/(2 pi) + (1/pi) sum_k kappa_k J_k,  J_k = (1/pi) int_0^pi e_P(c_k + R_k cos th) dth,
# where e_P is the piecewise linear profile of profile_published.py.  With an empty list of discs the program certifies
# the kernel inequality f <= U alone and prints C_1 = c_R1/(2 pi).
#
# Usage:  python3 certify_hybrid.py <solution.json> [T1]
#   solution.json: d, B (basis), c (coefficients, exact binary values), discs [(c_k,R_k,v_k)], kappa; T1 defaults to 40.
# Method (Proposition "Certification of the kernel inequality" and Section "The hybrid" of the article):
#   (a) on [0,1/2] x (0,T1] and [0,1/2] x [-T1,0): centred form H(centre) + grad H(box) . half-widths, bisection;
#   (b) for |t| >= T1, u = 1/t: t^2 U - 4 d^3 u - K5 |u|^3 > 0 on [0,1/2] x [0,1/T1] and [0,1/2] x [-1/T1,0], bisection;
#       this needs T1 >= 2d + 1/2 (convergence of the arctan series) and W_k = 0 for |t| >= T1.
import sys, json, time
from fractions import Fraction as Fr
from flint import arb, acb
from certutil import A, box, up_str, down_str, exact

sol = json.load(open(sys.argv[1])); T1 = Fr(sys.argv[2]) if len(sys.argv) > 2 else Fr(40)
d = Fr(sol['d']).limit_denominator(10**6); B = [tuple(x) for x in sol['B']]
c = [Fr(x) for x in sol['c']]                                           # exact binary values written by the optimiser
discs = [(Fr(cc).limit_denominator(10**4), Fr(R).limit_denominator(10**4), Fr(v).limit_denominator(10**4)) for cc, R, v in sol['discs']]
discs = [(cc, min(R, cc-Fr(1, 2)), v) for cc, R, v in discs]            # rational rounding must keep c_k - R_k >= 1/2 (a smaller R_k only lowers W_k)
kap = [Fr(x) for x in sol['kappa']]
# integrity of the data
assert len(c) == len(B) and len(discs) == len(kap)
assert B[0] == ('R', 1) and ('R', 2) in B and all(k in ('R', 'I') and j >= 1 for k, j in B) and ('I', 1) not in B
assert d > Fr(1, 2)
assert all(k >= 0 for k in kap) and all(R > 0 and cc-R >= Fr(1, 2) and cc > 1 for cc, R, v in discs)
assert T1 >= 2*d+Fr(1, 2)
assert all(abs(v)+R <= T1 for cc, R, v in discs)                         # then W_k = 0 for |t| >= T1
JMAX = max(j for _, j in B)
dA = A(d); half = A(Fr(1, 2)); PI = arb.pi()
cA = [A(x) for x in c]; kA = [A(x) for x in kap]; dsA = [(A(cc), A(R).log(), A(v)) for cc, R, v in discs]

def powers(x, t, n):
    # [(x+it)^0, (x+it)^-1, ..., (x+it)^-n]
    w = acb(1)/acb(x, t); pw = [acb(1)]
    for _ in range(n): pw.append(pw[-1]*w)
    return pw
def kernel(b, t):
    U = arb(0)
    for x in (dA+b, dA-b):
        pw = powers(x, t, JMAX)
        for i, (k, j) in enumerate(B):
            U += cA[i]*(pw[j].real if k == 'R' else -pw[j].imag)
    return U
def fbox(b, t, sgn):
    # f on the closure of t > 0 (sgn = +1) or of t < 0 (sgn = -1), in the form regular at t = 0
    return sgn*PI-2*(t/(dA+b)).atan()-2*(t/(dA-b)).atan()+(t/(2*dA+b)).atan()+(t/(2*dA-b)).atan()
def Wlow(b, t):
    # lower bound of sum_k kappa_k W_k on the box (W_k >= 0, so dropping a term is safe)
    s = arb(0)
    for (cc, lR, v), k in zip(dsA, kA):
        val = lR-((cc-half-b)**2+(t+v)**2).log()/2
        lo = val.lower()
        if lo > 0: s += k*lo
    return s
def grad(b, t):
    # partial derivatives of U - f with respect to b and t, on a box
    gb = arb(0); gt = arb(0)
    for x, sg in ((dA+b, 1), (dA-b, -1)):
        pw = powers(x, t, JMAX+1)
        for i, (k, j) in enumerate(B):
            dx = -j*pw[j+1]; dt = acb(0, -j)*pw[j+1]                      # d/dx (x+it)^-j,  d/dt (x+it)^-j
            if k == 'R': gb += cA[i]*sg*dx.real; gt += cA[i]*dt.real
            else: gb -= cA[i]*sg*dx.imag; gt -= cA[i]*dt.imag
    y1 = dA+b; y2 = dA-b; y3 = 2*dA+b; y4 = 2*dA-b; t2 = t*t
    ft = -2*y1/(y1*y1+t2)-2*y2/(y2*y2+t2)+y3/(y3*y3+t2)+y4/(y4*y4+t2)
    fb = 2*t/(y1*y1+t2)-2*t/(y2*y2+t2)-t/(y3*y3+t2)+t/(y4*y4+t2)
    return gb-fb, gt-ft
def Hcentered(b0, b1, t0, t1, sgn):
    bm = (b0+b1)/2; tm = (t0+t1)/2; b = box(b0, b1); t = box(t0, t1)
    H0 = kernel(A(bm), A(tm))-fbox(A(bm), A(tm), sgn)
    gb, gt = grad(b, t)
    H = H0+gb*box(-(b1-b0)/2, (b1-b0)/2)+gt*box(-(t1-t0)/2, (t1-t0)/2)
    return H+Wlow(b, t)
def cert_main(blo, bhi, tlo, thi, sgn, maxdepth=60):
    stack = [(blo, bhi, tlo, thi, 0)]; n = 0
    while stack:
        b0, b1, t0, t1, dep = stack.pop(); n += 1
        H = Hcentered(b0, b1, t0, t1, sgn)
        if H > 0: continue
        if dep >= maxdepth: raise RuntimeError('fail at b=[%s,%s] t=[%s,%s] H=%s' % (float(b0), float(b1), float(t0), float(t1), H))
        wb = (b1-b0)/Fr(1, 20); tm = max(abs(t0), abs(t1)); wt = (t1-t0)/max(Fr(1, 20), tm*Fr(3, 10))
        if wb >= wt: m_ = (b0+b1)/2; stack += [(b0, m_, t0, t1, dep+1), (m_, b1, t0, t1, dep+1)]
        else: m_ = (t0+t1)/2; stack += [(b0, b1, t0, m_, dep+1), (b0, b1, m_, t1, dep+1)]
    return n

# tail |t| >= T1, u = 1/t:  t^2 (U - f) >= t^2 U - 4 d^3 u - K5 |u|^3,  with t^2 U = sum_iota c_iota [Phi_iota(d+b,u) + Phi_iota(d-b,u)],
# Phi_R1 = x/(1+x^2 u^2),  Phi_iota = Re / -Im of u^(j-2) (xu+i)^(-j) for j >= 2;  K5 = (1/5) sum_i |alpha_i| y_i^5 (Lemma "The tail of the kernel").
def tailval(b, u):
    V = arb(0)
    for x in (dA+b, dA-b):
        for i, (k, j) in enumerate(B):
            if j == 1: V += cA[i]*x/(1+x*x*u*u)
            else:
                z = acb(u)**(j-2)*(acb(1)/acb(x*u, 1))**j
                V += cA[i]*(z.real if k == 'R' else -z.imag)
    return V
K5 = (2*(dA+half)**5+2*dA**5+(2*dA+half)**5+(2*dA)**5)/5
def cert_tail(u0, u1, maxdepth=40):
    assert max(abs(u0), abs(u1))*(2*d+Fr(1, 2)) <= 1                   # |y u| <= 1 for every y in {d+b, d-b, 2d+b, 2d-b}
    stack = [(Fr(0), Fr(1, 2), u0, u1, 0)]; n = 0
    while stack:
        b0, b1, a0, a1, dep = stack.pop(); n += 1
        b = box(b0, b1); u = box(a0, a1)
        H = tailval(b, u)-4*dA**3*u-K5*abs(u)**3
        if H > 0: continue
        if dep >= maxdepth: raise RuntimeError('tail fail b=[%s,%s] u=[%s,%s] H=%s' % (float(b0), float(b1), float(a0), float(a1), H))
        if (b1-b0)*8 >= (a1-a0)*T1: m_ = (b0+b1)/2; stack += [(b0, m_, a0, a1, dep+1), (m_, b1, a0, a1, dep+1)]
        else: m_ = (a0+a1)/2; stack += [(b0, b1, a0, m_, dep+1), (b0, b1, m_, a1, dep+1)]
    return n

def Jexact(nodes, cc, R):
    # (1/pi) int_0^pi e(cc + R cos th) dth for e piecewise linear through nodes, e = 0 for sigma >= 1; needs cc - R >= 1/2
    assert nodes[0][0] == Fr(1, 2) and nodes[-1] == (Fr(1), Fr(0)) and all(p[0] < q[0] for p, q in zip(nodes, nodes[1:]))
    tot = arb(0); ccA = A(cc); RA = A(R)
    lo, hi = cc-R, min(cc+R, Fr(1))
    for (p, ep), (q, eq) in zip(nodes, nodes[1:]):
        a, bq = max(p, lo), min(q, hi)
        if a >= bq: continue
        Bs = (eq-ep)/(q-p); As = ep-Bs*p                                 # e = As + Bs sigma on [p, q]
        tha = A((a-cc)/R).acos(); thb = A((bq-cc)/R).acos()               # tha >= thb
        tot += (A(As)+A(Bs)*ccA)*(tha-thb)+A(Bs)*RA*(tha.sin()-thb.sin())
    return tot/PI

if __name__ == '__main__':
    t_ = time.time()
    if discs:
        assert sol['prof'] == 'P', 'only the published-source profile e_P is supported'
        from profile_published import nodes_published
        nodes = nodes_published()
        J = [Jexact(nodes, cc, R) for cc, R, v in discs]
    else: J = []
    C = cA[0]/(2*PI)+sum((k*j for k, j in zip(kA, J)), arb(0))/PI
    print('d =', d, ' m =', JMAX, ' discs used:', len(discs), (' profile e_P (profile_published.py)' if discs else ''))
    print('C = c_R1/(2pi) + sum kappa_k J_k/pi =', C.str(25), ' (ball, midpoint and radius)')
    print('   radius of the ball:', C.rad().str(3), '  enclosure of C with directed rounding: [%s, %s]' % (down_str(C, 20), up_str(C, 20)))
    print('kernel part c_R1/(2pi) =', (cA[0]/(2*PI)).str(20))
    lim = 2*dA*cA[0]-2*cA[B.index(('R', 2))]; print('limit of t^2 U at |t| -> oo = 2 d c_R1 - 2 c_R2 =', lim.str(10), ' positive:', lim > 0)
    n1 = cert_main(Fr(0), Fr(1, 2), Fr(0), T1, +1); print('t in (0,T1]: certified, boxes', n1, flush=True)
    n2 = cert_main(Fr(0), Fr(1, 2), -T1, Fr(0), -1); print('t in [-T1,0): certified, boxes', n2, flush=True)
    n3 = cert_tail(Fr(0), 1/T1); n4 = cert_tail(-1/T1, Fr(0)); print('|t|>=T1: certified, boxes', n3+n4)
    Cup = up_str(C, 12); assert exact(C.upper()) <= Fr(Cup)
    print('all certified;  C <', Cup, '  time %.0fs' % (time.time()-t_))
