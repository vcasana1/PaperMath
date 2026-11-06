"""Numerical convex feasibility repair on all geometric interfaces.
The piecewise harmonic minimum principle justifies searching these interfaces;
the actual proof is a separate Arb program. No numerical feasibility is a proof.
"""
import sys,json,time,math
from pathlib import Path
from fractions import Fraction as Q
from decimal import Decimal,localcontext
import numpy as np
import cvxpy as cp
from scipy.optimize import minimize_scalar
from geometry_jensen import weight
from geometry_curves import curves,points
def repair(path,out,eta=2e-6):
    start=time.time();s=json.loads(Path(path).read_text());m=s['m'];B=[tuple(v) for v in s['B']];n=len(B);assert float(s['d'])==1.
    keep=[i for i,k in enumerate(s['geometry_weights']) if float(k)>1e-6];gs=[s['geometries'][i] for i in keep];kv=np.array([float(s['geometry_weights'][i]) for i in keep]);v=np.r_[np.array(s['parameters'],float),kv]
    T=math.ceil(max(g['R']+abs(g['v']) if g['kind']=='circle' else g['H']+abs(g['v']) for g in gs))+1;cc=curves(gs,T)
    def row(b,t):
        b,t=np.broadcast_arrays(np.atleast_1d(b),np.atleast_1d(t));G=np.zeros((len(t),n+len(gs)))
        for z in [1+b+1j*t,1-b+1j*t]:
            w=1-1/z
            for j,(kind,k) in enumerate(B):
                off=1 if kind=='R' else 2;f=z**(-off)*w**(k-off);G[:,j]+=f.real if kind=='R' else -f.imag
        for j,g in enumerate(gs):G[:,n+j]=weight(g,b,t)
        safe=np.where(t==0,1.,t);f=np.sign(t)*np.pi-2*np.arctan(t/(1+b))-2*np.arctan(t/(1-b))+np.arctan(t/(2+b))+np.arctan(t/(2-b))
        direct=2*np.arctan((1+b)/safe)+2*np.arctan((1-b)/safe)-np.arctan((2+b)/safe)-np.arctan((2-b)/safe)
        f=np.where(np.abs(t)>=1,direct,f);f=np.where(t==0,np.pi,f)
        return G*(1+t[:,None]**2),f*(1+t*t)
    rows=[];rhs=[]
    for c in cc:
        b,t=points(c,np.linspace(-1,1,801));gg,ff=row(b,t);rows.append(gg);rhs.extend(ff)
    for b0 in [0,.5]:
        t=np.r_[-np.geomspace(T,1e5,800)[::-1],np.geomspace(T,1e5,800)];gg,ff=row(np.full(len(t),b0),t);rows.append(gg);rhs.extend(ff)
    G=np.vstack(rows);F=np.array(rhs);first=np.r_[np.ones(m),np.zeros(m-1+len(gs))];tail=np.r_[2+2*np.arange(m),np.zeros(m-1+len(gs))]
    target=sum(Q(p) for p in s['parameters'][:m]);u=np.linspace(-1,1,5001)
    for it in range(12):
        new=[];worst=1.
        for c in cc:
            b,t=points(c,u);gg,ff=row(b,t);h=gg@v-ff;worst=min(worst,float(h.min()));idx=np.where((h<1e-3)&(h<=np.roll(h,1))&(h<=np.roll(h,-1)))[0]
            for j in idx:
                if j==0 or j==len(u)-1:continue
                def fun(x):
                    b,t=points(c,x);gg,ff=row(b,t);return float((gg@v-ff)[0])
                r=minimize_scalar(fun,bounds=(u[j-1],u[j+1]),method='bounded',options={'xatol':1e-13});worst=min(worst,r.fun)
                if r.fun<eta*.95:new.append((c,r.x))
        print(json.dumps(dict(iteration=it,worst_scaled_slack=worst,cuts=len(new),geometries=len(gs),seconds=time.time()-start)),flush=True)
        if not new and worst>eta*.8:break
        for c,x in new:
            b,t=points(c,x);gg,ff=row(b,t);G=np.vstack([G,gg]);F=np.r_[F,ff]
        delta=cp.Variable(len(v));prob=cp.Problem(cp.Minimize(cp.sum_squares(delta)),[G@delta>=F+eta-G@v,first@delta==0,tail@(v+delta)>=eta,v[n:]+delta[n:]>=0,cp.norm_inf(delta)<=.01])
        prob.solve(solver='CLARABEL',tol_gap_abs=1e-14,tol_feas=1e-11,tol_gap_rel=1e-11,max_iter=250);assert delta.value is not None,prob.status
        raw=[Q(repr(float(x))) for x in v+delta.value];raw[0]+=target-sum(raw[:m])
        v=np.array([float(x) for x in raw]);pars=raw[:n];kap=raw[n:]
    else:raise RuntimeError('geometry repair did not converge')
    if 'pars' not in locals():pars=[Q(x) for x in s['parameters']];kap=[Q(s['geometry_weights'][i]) for i in keep]
    old=[Q(0)]*n
    for col,(kind,j) in enumerate(B):
        off=1 if kind=='R' else 2
        for k in range(j-off+1):old[B.index((kind,k+off))]+=pars[col]*math.comb(j-off,k)*(-1)**k
    with localcontext() as dc:
        dc.prec=10*(m+2);param=[str(Decimal(x.numerator)/Decimal(x.denominator)) for x in pars];coeff=[str(Decimal(x.numerator)/Decimal(x.denominator)) for x in old];kw=[str(Decimal(x.numerator)/Decimal(x.denominator)) for x in kap]
    for key in ['C_numerical','A_total_numerical','B_loglog_numerical','peak_logT_numerical']:
        if key in s:s['search_'+key]=s.pop(key)
    s.update(parameters=param,c=coeff,geometries=gs,geometry_weights=kw,certified=False,geometry_repair_source=path,geometry_repair_eta=eta,geometry_repair_seconds=time.time()-start,geometry_boundary_T=T)
    Path(out).write_text(json.dumps(s,indent=2));print('REPAIRED NUMERICALLY',out,flush=True)
if __name__=='__main__':repair(sys.argv[1],sys.argv[2],float(sys.argv[3]) if len(sys.argv)>3 else 2e-6)
