# Exploration: Turing-Amberger-Bellotti-Wong kernel LP, optionally hybridised with Jensen discs + subconvexity profile.
import numpy as np
from scipy.optimize import linprog

def f(b,t,d):
    return (2*np.arctan((b+d)/t)+2*np.arctan((d-b)/t)-np.arctan((b+2*d)/t)-np.arctan((2*d-b)/t))

def basis(x,t,kind,j):
    z=(x+1j*t)**(-j)
    return z.real if kind=='R' else -z.imag

def tgrid(tmax=300.):
    p=np.concatenate([[1e-9],np.geomspace(1e-4,tmax,700),np.linspace(0,4,400)[1:]])
    p=np.unique(p); return np.concatenate([-p[::-1],p])

def build(d,B,bgrid,tg):
    bb,tt=np.meshgrid(bgrid,tg,indexing='ij'); bb=bb.ravel(); tt=tt.ravel()
    G=np.array([basis(d+bb,tt,k,j)+basis(d-bb,tt,k,j) for (k,j) in B]).T
    return bb,tt,G,f(bb,tt,d)

def solve(d,B,bmax=0.5,discs=(),prof=None,nb=41,tg=None,verbose=False):
    """minimise c_R1/(2pi) + sum kappa_k J_k/pi  s.t. f <= sum c_j G_j + sum kappa_k w_k on grid.
    discs: list of (c,R,v): Jensen disc centred at c + i(T+v), weight log+(R/dist) of the right member."""
    tg=tgrid() if tg is None else tg
    bgrid=np.linspace(0,bmax,nb) if not discs else np.linspace(0,0.5,nb)
    bb,tt,G,F=build(d,B,bgrid,tg)
    W=[]; J=[]
    for (c,R,v) in discs:
        dist=np.sqrt((c-0.5-bb)**2+(tt+v)**2)
        W.append(np.maximum(0,np.log(R/dist))); J.append(jensen(prof,c,R))
    W=np.array(W).T if discs else np.zeros((len(bb),0))
    A=-np.hstack([G,W]); rhs=-F
    obj=np.zeros(len(B)+len(discs)); i1=B.index(('R',1)); obj[i1]=1/(2*np.pi)
    for k in range(len(discs)): obj[len(B)+k]=J[k]/np.pi
    bounds=[(None,None)]*len(B)+[(0,None)]*len(discs)
    r=linprog(obj,A_ub=A,b_ub=rhs,bounds=bounds,method='highs')
    if r.status!=0: return None
    return r.fun, r.x

def jensen(prof,c,R,n=20000):
    th=np.linspace(0,np.pi,n+1); s=c+R*np.cos(th)
    v=np.array([prof(x) for x in s]); return np.trapezoid(v,th)/np.pi   # (1/2pi) int_0^{2pi}

# Bourgain profile, reflected
def bourgain():
    k,l=13/84,55/84; nodes=[]
    for _ in range(8):
        nodes.append((l-k,k)); k,l=k/(2*k+2),0.5+l/(2*k+2)
    nodes.append((1.0,0.0)); xs=np.array([a for a,_ in nodes]); es=np.array([e for _,e in nodes])
    def e(s):
        if s>=1: return 0.0
        if s>=0.5:
            if s<=xs[0]: return float(es[0])   # constant 13/84 below first node (convexity bound from 1/2)
            return float(np.interp(s,xs,es))
        if s>=0: return 0.5-s+e(1-s)
        return 0.5-s
    return e

def solve_scaled(d,m,discs=(),prof=None,nb=41,tg=None):
    B=[('R',j) for j in range(1,m+1)]+[('I',j) for j in range(2,m+1)]
    tg=tgrid() if tg is None else tg
    bgrid=np.linspace(0,0.5,nb)
    bb,tt,G,F=build(d,B,bgrid,tg)
    sc=np.array([(d-0.5)**j for (_,j) in B]); G=G*sc
    W=[];J=[]
    for (c,R,v) in discs:
        dist=np.sqrt((c-0.5-bb)**2+(tt+v)**2); W.append(np.maximum(0,np.log(R/dist))); J.append(jensen(prof,c,R))
    W=np.array(W).T if discs else np.zeros((len(bb),0))
    A=-np.hstack([G,W]); obj=np.zeros(len(B)+len(discs)); obj[0]=sc[0]/(2*np.pi)
    for k in range(len(discs)): obj[len(B)+k]=J[k]/np.pi
    r=linprog(obj,A_ub=A,b_ub=-F,bounds=[(None,None)]*len(B)+[(0,None)]*len(discs),method='highs')
    if r.status!=0: return None
    x=r.x.copy(); x[:len(B)]*=sc
    return r.fun,x,B

def explicit_profile():
    nodes=[(0.5,27/164)]+[(1-m/(2**m-2),1/(2**m-2)) for m in range(4,10)]+[(1.0,0.0)]
    xs=np.array([a for a,_ in nodes]); es=np.array([b for _,b in nodes])
    def e(s):
        if s>=1: return 0.0
        if s>=0.5: return float(np.interp(s,xs,es))
        if s>=0: return 0.5-s+e(1-s)
        return 0.5-s
    return e

def check(d,x,B,discs=(),nb=201,nt=40001,tmax=2000.):
    """max violation of f <= U + sum kappa w on a fine grid (b>=0 symmetric)."""
    bg=np.linspace(0,0.5,nb); tp=np.concatenate([np.geomspace(1e-7,tmax,nt//2)]); tg=np.concatenate([-tp[::-1],tp])
    worst=-1e9; arg=None
    for b in bg:
        U=sum(x[i]*(basis(d+b,tg,k,j)+basis(d-b,tg,k,j)) for i,(k,j) in enumerate(B))
        Wt=sum(x[len(B)+q]*np.maximum(0,np.log(R/np.sqrt((c-0.5-b)**2+(tg+v)**2))) for q,(c,R,v) in enumerate(discs))
        viol=f(b,tg,d)-U-Wt; i=np.argmax(viol)
        if viol[i]>worst: worst=viol[i]; arg=(b,tg[i])
    return worst,arg
