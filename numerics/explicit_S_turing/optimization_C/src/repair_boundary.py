"""Convex minimum-displacement repair; subsequent Arb certification mandatory.
Preserves c_R1 exactly. Does not claim to optimize the arithmetic objective.
"""
import sys,json,math,time
from pathlib import Path
from fractions import Fraction as Q
from decimal import Decimal,localcontext
import numpy as np
import cvxpy as cp
from scipy.optimize import minimize_scalar

def repair(path,out,eta=5e-7):
    start=time.time();s=json.loads(Path(path).read_text());d=float(s['d']);m=s['m'];B=[tuple(x) for x in s['B']];lam=2*d-1;n=len(B)
    assert s['representation']=='laguerre';v=np.array(s['parameters'],float)
    def row(t,b=.5):
        t=np.atleast_1d(t);b=np.broadcast_to(b,t.shape);z=[d+b+1j*t,d-b+1j*t];a=[]
        for kind,j in B:
            off=1 if kind=='R' else 2;x=sum(zz**(-off)*(1-lam/zz)**(j-off) for zz in z)
            a.append(x.real if kind=='R' else -x.imag)
        f=np.sign(t)*np.pi-2*np.arctan(t/(d+b))-2*np.arctan(t/(d-b))+np.arctan(t/(2*d+b))+np.arctan(t/(2*d-b))
        safe=np.where(t==0,1.,t)
        direct=2*np.arctan((d+b)/safe)+2*np.arctan((d-b)/safe)-np.arctan((2*d+b)/safe)-np.arctan((2*d-b)/safe)
        f=np.where(np.abs(t)>=1,direct,f)
        f=np.where(t==0,np.pi,f)
        return np.array(a).T*(1+t[:,None]**2),f*(1+t**2)
    t=np.geomspace(1e-8,5000,30000);t=np.r_[-t[::-1],0.,t];G,F=row(t)
    zero_b=np.linspace(0,.5,501);zg,zf=row(np.zeros_like(zero_b),zero_b)
    tp=np.r_[-np.geomspace(1e-6,2000,1000)[::-1],0,np.geomspace(1e-6,2000,1000)]
    gg,ff=row(tp);gg=np.vstack([gg,zg]);ff=np.r_[ff,zf]
    first=np.r_[np.ones(m),np.zeros(m-1)];second=np.r_[-lam*np.arange(m),np.zeros(m-1)]
    for it in range(20):
        h=G@v-F;idx=np.where((h<1e-3)&(h<=np.roll(h,1))&(h<=np.roll(h,-1)))[0];new=[];worst=float(h.min())
        for i in idx:
            if i==0 or i==len(t)-1:continue
            r=minimize_scalar(lambda x:float((lambda a,b:a@v-b)(*row(x))[0]),bounds=(t[i-1],t[i+1]),method='bounded',options={'xatol':1e-14})
            worst=min(worst,r.fun)
            if r.fun<eta*.95:new.append(r.x)
        print('repair',it,'min H*(1+t^2)',worst,'cuts',len(new),flush=True)
        if not new:break
        ng,nf=row(np.array(new));gg=np.vstack([gg,ng]);ff=np.r_[ff,nf]
        delta=cp.Variable(n);prob=cp.Problem(cp.Minimize(cp.sum_squares(delta)),[gg@delta>=ff+eta-gg@v,first@delta==0.,(2*d*first-2*second)@(v+delta)>=eta])
        prob.solve(solver='CLARABEL',tol_gap_abs=1e-15,tol_gap_rel=1e-12,tol_feas=1e-12,max_iter=300)
        assert delta.value is not None
        # Exact preservation of the rational sum, including serialization.
        raw=[Q(repr(float(x))) for x in v+delta.value];oldsum=sum(Q(x) for x in s['parameters'][:m]);raw[0]+=oldsum-sum(raw[:m])
        with localcontext() as dc:
            dc.prec=10*(m+2);pars=[str(Decimal(x.numerator)/Decimal(x.denominator)) for x in raw]
        v=np.array(pars,float)
    else:raise RuntimeError('repair did not converge')
    if 'pars' not in locals():pars=s['parameters']
    old=[Q(0) for _ in B];lq=2*Q(s['d'])-1
    for col,(kind,j) in enumerate(B):
        off=1 if kind=='R' else 2
        for k in range(j-off+1):old[B.index((kind,k+off))]+=Q(pars[col])*math.comb(j-off,k)*(-lq)**k
    with localcontext() as dc:
        dc.prec=10*(m+2);coef=[str(Decimal(x.numerator)/Decimal(x.denominator)) for x in old]
    s.update(c=coef,parameters=pars,discs=[],kappa=[],certified=False,repair_eta=eta,repair_source=path,repair_seconds=time.time()-start)
    Path(out).write_text(json.dumps(s,indent=2))
if __name__=='__main__':repair(sys.argv[1],sys.argv[2])
