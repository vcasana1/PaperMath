# Exploration (grid LP, NOT certified): Turing-Backlund split.
# pi S(T) = arg zeta(b2+iT) - I1 - I2 - sum_rho g_delta,  segments start at beta* = 1/2 + delta.
# Asymptotic coefficient of log T:  A + B with
#   A = min c_R1/(2 pi) s.t. f_delta(b,t) <= sum_j c_j [F_j(dk+b,t)+F_j(dk-b,t)]  (kernel evaluated at abscissa 1/2+dk > 1)
#   B = 2 * min_{c0,R} J(e*; c0, R)/log(R/(c0-beta*))   (Backlund: zeros of Re zeta on [beta*, c0]; c0 >= 1.75 so Re zeta(c0+iT) > 0)
import sys, json, math, numpy as np
sys.path.insert(0, '../../../numerics/explicit_S_turing/hybrid_asymptotic')
from scipy.optimize import linprog
def fdel(b,t,dl): return 2*np.arctan((b+dl)/t)+2*np.arctan((dl-b)/t)-np.arctan((b+2*dl)/t)-np.arctan((2*dl-b)/t)
def F(x,t,k,j):
    z=(x+1j*t)**(-j); return z.real if k=='R' else -z.imag
def tgrid():
    p=np.unique(np.concatenate([[1e-9],np.geomspace(1e-4,300,600),np.linspace(0,4,300)[1:]])); return np.concatenate([-p[::-1],p])
def A_kernel(dl,dk,m):
    B=[('R',j) for j in range(1,m+1)]+[('I',j) for j in range(2,m+1)]
    bb,tt=[a.ravel() for a in np.meshgrid(np.linspace(0,0.5,41),tgrid(),indexing='ij')]
    sc=np.array([(dk-0.5)**j for _,j in B])
    G=np.array([F(dk+bb,tt,k,j)+F(dk-bb,tt,k,j) for (k,j) in B]).T*sc
    Fv=fdel(bb,tt,dl)
    obj=np.zeros(len(B)); obj[0]=sc[0]/(2*math.pi)
    arow=np.zeros(len(B)); arow[0]=2*dk*sc[0]; arow[1]=-2*sc[1]
    r=linprog(obj,A_ub=-np.vstack([G,arow]),b_ub=-np.concatenate([Fv,[1e-6]]),bounds=[(None,None)]*len(B),method='highs')
    return r.fun if r.status==0 else None
# reflected Bourgain profile
k,l=13/84,55/84; nodes=[]
for _ in range(8): nodes.append((l-k,k)); k,l=k/(2*k+2),0.5+l/(2*k+2)
nodes.append((1.0,0.0)); xs=np.array([a for a,_ in nodes]); es=np.array([e for _,e in nodes])
def e(s):
    if s>=1: return 0.0
    if s>=0.5: return float(np.interp(s,xs,es))
    if s>=0: return 0.5-s+e(1-s)
    return 0.5-s
def J(c0,R,n=4001):
    th=np.linspace(0,np.pi,n); return np.trapezoid([e(c0+R*math.cos(x)) for x in th],th)/np.pi
def B_backlund(bstar):
    best=9
    for c0 in [1.75,1.85,2.0,2.25,2.5,3.0]:
        r=c0-bstar
        for q in [1.2,1.4,1.6,1.8,2.0,2.3,2.6,3.0,3.5]:
            R=q*r; best=min(best,2*J(c0,R)/math.log(q))
    return best
out=sys.argv[1]
for dl in [0.05,0.1,0.15,0.2,0.25,0.3,0.4,0.5]:
    Bv=B_backlund(0.5+dl)
    for dk in [0.55,0.7,0.9]:
        for m in [4,8,12]:
            Av=A_kernel(dl,dk,m)
            rec=dict(delta=dl,dk=dk,m=m,A=Av,B=Bv,total=(Av+Bv) if Av is not None else None)
            open(out,'a').write(json.dumps(rec)+'\n'); print(rec,flush=True)
