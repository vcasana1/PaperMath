"""Executed local convex-Newton refinement of arithmetic cost and K margins.
Not an optimality certificate. All outputs must pass independent verifiers.
The original slope is preserved EXACTLY by rational serialization.
"""
import sys,json,math,time
from pathlib import Path
from fractions import Fraction as Q
from decimal import Decimal,localcontext
import numpy as np
import cvxpy as cp
from scipy.special import eval_laguerre,eval_genlaguerre
from scipy.optimize import minimize_scalar
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'family'))
from opt_line import primes
from empirical_quadrature import nodes

def refine(path,out,eta=1e-10):
    start=time.time();s=json.loads(Path(path).read_text());d=float(s['d']);m=s['m'];B=[tuple(b) for b in s['B']];n=len(B);lam=2*d-1
    assert s['representation']=='laguerre';v=np.array(s['parameters'],float);initial=v.copy()
    first=np.r_[np.ones(m),np.zeros(m-1)];second=np.r_[-lam*np.arange(m),np.zeros(m-1)]
    def maps(L):
        a=np.zeros((len(L),n));b=a.copy()
        for col,(kind,j) in enumerate(B):
            if kind=='R':a[:,col]=-eval_laguerre(j-1,lam*L)/np.pi
            else:b[:,col]=-L*eval_genlaguerre(j-2,1,lam*L)/((j-1)*np.pi)
        return a,b
    L,w=nodes(d,10**8,1000);a,b=maps(L);a*=w[:,None];b*=w[:,None];b0=w*(np.exp(-d*L)-2)/(L*np.pi)
    pg=[]
    for p in primes(1000):
        ks=np.arange(1,int(np.log(10**12)/np.log(p))+1);ll=ks*np.log(p);ww=np.log(p)*np.exp(-(d+.5)*ll);aa,bb=maps(ll)
        pg.append((ks,aa*ww[:,None],bb*ww[:,None],ww*(np.exp(-d*ll)-2)/(ll*np.pi)))
    def model(v):
        ax=a@v;bx=b@v+b0;h=np.hypot(ax,bx);valid=h>1e-150
        ua=ax[valid]/h[valid];ub=bx[valid]/h[valid]
        grad=ua@a[valid]+ub@b[valid];orth=(-ub[:,None]*a[valid]+ua[:,None]*b[valid])/np.sqrt(h[valid,None]);H=orth.T@orth;value=h.sum()
        for ks,aa,bb,beta in pg:
            ar=aa@v;bi=bb@v+beta;xx=np.linspace(0,2*np.pi,256,endpoint=False)
            vv=np.cos(np.outer(xx,ks))@ar+np.sin(np.outer(xx,ks))@bi;j=int(np.argmax(vv))
            r=minimize_scalar(lambda x:-float(np.cos(ks*x)@ar+np.sin(ks*x)@bi),bounds=(xx[j]-2*np.pi/256,xx[j]+2*np.pi/256),method='bounded')
            x=r.x;co=np.cos(ks*x);si=np.sin(ks*x);g=co@aa+si@bb;cross=(-ks*si)@aa+(ks*co)@bb;curvature=-(ks*ks*co)@ar-(ks*ks*si)@bi
            value-=r.fun;grad+=g
            if curvature< -1e-20:H+=np.outer(cross,cross)/(-curvature)
        H=(H+H.T)/2;H+=np.eye(n)*max(1e-10,float(np.trace(H))*1e-12/n)
        return value,grad,H
    def krows(t,beta=.5):
        t=np.atleast_1d(t);beta=np.broadcast_to(beta,t.shape);zz=[d+beta+1j*t,d-beta+1j*t];cols=[]
        for kind,j in B:
            off=1 if kind=='R' else 2;z=sum(x**(-off)*(1-lam/x)**(j-off) for x in zz);cols.append(z.real if kind=='R' else -z.imag)
        safe=np.where(t==0,1.,t)
        f1=np.sign(t)*np.pi-2*np.arctan(t/(d+beta))-2*np.arctan(t/(d-beta))+np.arctan(t/(2*d+beta))+np.arctan(t/(2*d-beta))
        f2=2*np.arctan((d+beta)/safe)+2*np.arctan((d-beta)/safe)-np.arctan((2*d+beta)/safe)-np.arctan((2*d-beta)/safe)
        f=np.where(np.abs(t)>=1,f2,f1);f=np.where(t==0,np.pi,f)
        return np.array(cols).T*(1+t[:,None]**2),f*(1+t*t)
    tt=np.geomspace(1e-8,5000,18000);tt=np.r_[-tt[::-1],0.,tt];fineG,fineF=krows(tt)
    coarse=np.r_[-np.geomspace(1e-6,3000,800)[::-1],0.,np.geomspace(1e-6,3000,800)]
    G,F=krows(coarse);gz,fz=krows(np.zeros(301),np.linspace(0,.5,301));G=np.vstack([G,gz]);F=np.r_[F,fz]
    for iteration in range(12):
        val,grad,H=model(v);h=fineG@v-fineF;idx=np.where((h<1e-3)&(h<=np.roll(h,1))&(h<=np.roll(h,-1)))[0]
        newt=[];worst=float(h.min())
        for j in idx:
            if j==0 or j==len(tt)-1:continue
            r=minimize_scalar(lambda t:float((lambda g,f:g@v-f)(*krows(t))[0]),bounds=(tt[j-1],tt[j+1]),method='bounded',options={'xatol':1e-13})
            newt.append(r.x);worst=min(worst,r.fun)
        gg,ff=krows(np.array(newt));G=np.vstack([G,gg]);F=np.r_[F,ff]
        delta=cp.Variable(n);objective=grad@delta+cp.quad_form(delta,cp.psd_wrap(H))/2
        cons=[G@delta>=F+eta-G@v,first@delta==0,(2*d*first-2*second)@(v+delta)>=eta,cp.norm_inf(delta)<=.001]
        problem=cp.Problem(cp.Minimize(objective),cons);problem.solve(solver='CLARABEL',tol_gap_abs=1e-13,tol_feas=1e-13,tol_gap_rel=1e-12,max_iter=300)
        assert delta.value is not None
        change=delta.value;print(json.dumps(dict(iteration=iteration,arithmetic_model=val,worst=worst,predicted_change=float(problem.value),step=float(np.max(np.abs(change))),seconds=time.time()-start)),flush=True)
        raw=[Q(repr(float(x))) for x in v+change];target=sum(Q(x) for x in s['parameters'][:m]);raw[0]+=target-sum(raw[:m])
        with localcontext() as dc:
            dc.prec=10*(m+2);pars=[str(Decimal(x.numerator)/Decimal(x.denominator)) for x in raw]
        v=np.array(pars,float)
        if iteration>=2 and np.max(np.abs(change))<1e-8 and worst>eta*.5:break
    old=[Q(0)]*n;lq=2*Q(s['d'])-1
    for col,(kind,j) in enumerate(B):
        off=1 if kind=='R' else 2
        for k in range(j-off+1):old[B.index((kind,k+off))]+=Q(pars[col])*math.comb(j-off,k)*(-lq)**k
    with localcontext() as dc:
        dc.prec=10*(m+2);coeff=[str(Decimal(x.numerator)/Decimal(x.denominator)) for x in old]
    s.update(c=coeff,parameters=pars,certified=False,margin_refinement=True,eta=eta,refinement_source=path,seconds_refinement=time.time()-start)
    Path(out).write_text(json.dumps(s,indent=2))
if __name__=='__main__':refine(sys.argv[1],sys.argv[2],float(sys.argv[3]) if len(sys.argv)>3 else 1e-10)
