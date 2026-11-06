"""Numerical search only. Boundary reduction: manuscript v11, section 7.1.
Fixed d,m: convex SOCP; d and m are outer, nonconvex choices.
No numerical result from this file is a certificate.
"""
import os, sys, json, time, argparse
from pathlib import Path
import numpy as np
import cvxpy as cp
from scipy.optimize import minimize_scalar
from scipy.special import eval_laguerre,eval_genlaguerre
from fractions import Fraction as Q
import math
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'family'))
from opt_line import basis, kernel_rows, czeta_data, czeta_pp_data

def search(d,m,eta=2e-5,n0=20000,ppmax=1000,Lstart=100.,maxit=30,representation='monomial',empirical_N=0,phase_samples=64,solver_tol=1e-8):
    B=basis(m,m); nb=len(B); cap=.08382
    original_rows=kernel_rows
    lam=2*(d-.5)
    conversion=np.eye(nb)
    if representation=='laguerre':
        conversion=np.zeros((nb,nb))
        for col,(kind,j) in enumerate(B):
            off=1 if kind=='R' else 2
            for k in range(j-off+1):conversion[B.index((kind,k+off)),col]=math.comb(j-off,k)*(-lam)**k
        def rows(dd,BB,bb,tt):
            zz=[dd+bb+1j*tt,dd-bb+1j*tt];gg=[]
            for kind,j in BB:
                off=1 if kind=='R' else 2
                zval=sum(z**(-off)*(1-lam/z)**(j-off) for z in zz)
                gg.append(zval.real if kind=='R' else -zval.imag)
            # Equivalent arctangent identity avoids cancellation at large |t|.
            safe=np.where(tt==0,1.,tt)
            ff=original_rows(dd,[('R',1)],bb,tt)[1]
            direct=2*np.arctan((dd+bb)/safe)+2*np.arctan((dd-bb)/safe)-np.arctan((2*dd+bb)/safe)-np.arctan((2*dd-bb)/safe)
            return np.array(gg).T,np.where(np.abs(tt)>=1,direct,ff)
        rowsfun=rows
    else:rowsfun=original_rows
    # Multiply boundary inequalities by 1+t^2, avoiding tiny tail rows.
    tp=np.unique(np.r_[0.,np.linspace(0,5,400),np.geomspace(1e-5,5000,600)])
    tt=np.r_[-tp[:0:-1],tp]; bb=np.full_like(tt,.5)
    G,F=rowsfun(d,B,bb,np.where(tt==0,1e-30,tt)); F[tt==0]=np.pi
    G*=1+tt[:,None]**2; F=F*(1+tt**2)+eta
    bzero=np.linspace(0,.5,201)
    G0,_=rowsfun(d,B,bzero,np.zeros_like(bzero)+1e-30)
    G=np.vstack([G,G0]); F=np.r_[F,np.full(len(bzero),np.pi+eta)]
    RA,RB,b0,w,primeof=czeta_data(d,B,n0)
    # Resolve the oscillatory high-order tail in short panels. A single
    # 400-node rule over [log(n0),700] under-resolves some candidate norms.
    xn,wn=np.polynomial.legendre.leggauss(160)
    edges=sorted(set([np.log(n0)]+[x for x in [20.,40.,80.,160.,320.,700.] if x>np.log(n0)]))
    LL=[];WW=[]
    for l,r in zip(edges,edges[1:]):
        nodes=(l+r)/2+(r-l)*xn/2
        LL.extend(nodes);WW.extend((r-l)*wn/2*np.exp((.5-d)*nodes))
    LL=np.array(LL);newa=np.zeros((len(LL),nb));newb=newa.copy()
    for col,(kind,j) in enumerate(B):
        (newa if kind=='R' else newb)[:,col]=-LL**(j-1)/math.factorial(j-1)/np.pi
    keep=primeof!=0
    RA=np.vstack([RA[keep],newa]);RB=np.vstack([RB[keep],newb]);b0=np.r_[b0[keep],(np.exp(-d*LL)-2)/(LL*np.pi)]
    w=np.r_[w[keep],WW];primeof=np.r_[primeof[keep],np.zeros(len(LL),int)]
    if empirical_N:
        from empirical_quadrature import nodes
        LL,w=nodes(d,empirical_N,ppmax)
        RA=np.zeros((len(LL),nb));RB=RA.copy()
        for col,(kind,j) in enumerate(B):(RA if kind=='R' else RB)[:,col]=-LL**(j-1)/math.factorial(j-1)/np.pi
        b0=(np.exp(-d*LL)-2)/(LL*np.pi);primeof=np.zeros(len(LL),int)
    groups=czeta_pp_data(d,B,ppmax,empirical_N or n0)
    if representation=='laguerre':
        def rmaps(L):
            a=np.zeros((len(L),nb));b=a.copy()
            for col,(kind,j) in enumerate(B):
                if kind=='R':a[:,col]=-eval_laguerre(j-1,lam*L)/np.pi
                else:b[:,col]=-L*eval_genlaguerre(j-2,1,lam*L)/((j-1)*np.pi)
            return a,b
        # Recover L from R2/R1 in the original data (R1=-1/pi,R2=-L/pi).
        L=RA[:,1]/RA[:,0];RA,RB=rmaps(L)
        newgroups=[]
        for p,ks,ra,rb,bz in groups:
            L=ks*np.log(p);wpp=np.log(p)*np.exp(-(d+.5)*L);a,b=rmaps(L)
            newgroups.append((p,ks,a*wpp[:,None],b*wpp[:,None],bz))
        groups=newgroups
    mask=(primeof==0)|(primeof>ppmax)
    # Whitening all linear maps, including the objective, improves conditioning.
    maps=[G,RA[mask]*w[mask,None],RB[mask]*w[mask,None]]
    for p,ks,ra,rb,bz in groups: maps.extend([ra,rb])
    M=np.vstack(maps); norms=np.linalg.norm(M,axis=0); norms=np.maximum(norms,1e-100)
    _,s,V=np.linalg.svd(M/norms,full_matrices=False)
    transform=(V.T/s)/norms[:,None]
    print('conditioning',s[0]/s[-1],flush=True)
    xph=np.linspace(0,2*np.pi,phase_samples,endpoint=False)
    phasegrids=[list(xph) for _ in groups]
    fine=np.r_[-np.geomspace(1e-8,1e5,16000)[::-1],0.,np.geomspace(1e-8,1e5,16000)]
    def kval(t,cv):
        gg,ff=rowsfun(d,B,np.full(np.size(t),.5),np.atleast_1d(t)+1e-100)
        return (gg@cv-ff)*(1+np.atleast_1d(t)**2)-eta
    for it in range(maxit):
        y=cp.Variable(nb); c=transform@y
        cR1=conversion[0]@c;cR2=conversion[1]@c
        cons=[(G@transform)@y>=F,cR1<=2*np.pi*cap-1e-10,
              2*d*cR1-2*cR2>=eta]
        ts=cp.Variable(len(groups))
        for gi,(p,ks,ra,rb,bz) in enumerate(groups):
            xx=np.array(phasegrids[gi]); co=np.cos(np.outer(xx,ks)); si=np.sin(np.outer(xx,ks))
            cons.append(ts[gi]>=((co@ra+si@rb)@transform)@y+si@bz)
        Cz=cp.sum(ts)+cp.sum(cp.norm(cp.vstack([((RA[mask]*w[mask,None])@transform)@y,((RB[mask]*w[mask,None])@transform)@y+b0[mask]*w[mask]]),axis=0))
        obj=Cz-cR1/(2*np.pi)*np.log(2*np.pi)+(cR1/(2*np.pi)-cap)*Lstart
        prob=cp.Problem(cp.Minimize(obj),cons)
        try: prob.solve(solver='CLARABEL',tol_gap_abs=solver_tol,tol_feas=solver_tol,tol_gap_rel=solver_tol,max_iter=300,verbose=bool(os.environ.get('SOLVER_VERBOSE')))
        except Exception as e:
            print('SOLVER ERROR',repr(e),flush=True);return None
        if y.value is None:print('STATUS',prob.status,flush=True);return None
        cv=transform@y.value
        vals=kval(fine,cv); idx=np.where((vals< 1e-3)&(vals<=np.roll(vals,1))&(vals<=np.roll(vals,-1)))[0]
        newt=[]
        continuous_worst=float(vals.min())
        for k in idx:
            if k==0 or k==len(fine)-1:continue
            res=minimize_scalar(lambda t:float(kval(t,cv)[0]),bounds=(fine[k-1],fine[k+1]),method='bounded',options={'xatol':1e-13})
            continuous_worst=min(continuous_worst,float(res.fun))
            if res.fun< -1e-9:newt.append(res.x)
        # Search continuous phase maxima of every truncated prime polynomial.
        pgap=0.
        for gi,(p,ks,ra,rb,bz) in enumerate(groups):
            aa=ra@cv; bs=rb@cv+bz
            def pv(x):return np.cos(np.outer(np.atleast_1d(x),ks))@aa+np.sin(np.outer(np.atleast_1d(x),ks))@bs
            xx=np.linspace(0,2*np.pi,600,endpoint=False); vv=pv(xx)
            for j in np.where((vv>=np.roll(vv,1))&(vv>=np.roll(vv,-1)))[0]:
                res=minimize_scalar(lambda x:-float(pv(x)[0]),bounds=(xx[j]-2*np.pi/600,xx[j]+2*np.pi/600),method='bounded')
                gap=-res.fun-ts.value[gi];pgap=max(pgap,gap)
                if gap>2e-9:phasegrids[gi].append(res.x)
        # t=0 is a one-dimensional rational boundary too.
        bzfine=np.linspace(0,.5,2001); gz,_=rowsfun(d,B,bzfine,np.full_like(bzfine,1e-100));vz=gz@cv-np.pi-eta
        zi=np.where((vz< -1e-8)&(vz<=np.roll(vz,1))&(vz<=np.roll(vz,-1)))[0]
        if len(zi):G=np.vstack([G,gz[zi]]);F=np.r_[F,np.full(len(zi),np.pi+eta)]
        worst=continuous_worst
        print(json.dumps(dict(it=it,d=d,m=m,objective=float(prob.value),C1=float(conversion[0]@cv/(2*np.pi)),Cz=float(Cz.value),worst=worst,phasegap=float(pgap),newcuts=len(newt),status=prob.status)),flush=True)
        if not newt and not len(zi) and pgap<2e-9:break
        if newt:
            nt=np.array(newt); ng,nf=rowsfun(d,B,np.full_like(nt,.5),nt)
            G=np.vstack([G,ng*(1+nt[:,None]**2)]);F=np.r_[F,nf*(1+nt**2)+eta]
    params=[repr(float(v)) for v in cv]
    if representation=='laguerre':
        # Exact rational conversion from stored decimals. Keep all digits.
        old=[Q(0) for _ in B];lq=2*(Q(str(d))-Q(1,2))
        for col,(kind,j) in enumerate(B):
            off=1 if kind=='R' else 2
            for k in range(j-off+1):old[B.index((kind,k+off))]+=Q(params[col])*math.comb(j-off,k)*(-lq)**k
        from decimal import Decimal,localcontext
        with localcontext() as dc:
            dc.prec=max(160,10*(m+2))
            coeff=[str(Decimal(v.numerator)/Decimal(v.denominator)) for v in old]
    else:coeff=params
    return dict(d=str(d),m=m,B=B,c=coeff,representation=representation,parameters=params,discs=[],kappa=[],eta=eta,quadrature='positive empirical prime-power Gauss + continuous tail' if empirical_N else '160 Gauss nodes per log panel',empirical_N=empirical_N,
                C1=float(conversion[0]@cv/(2*np.pi)),Cz_est=float(Cz.value),C_est=float(prob.value),Lstart=Lstart,
                Lpeak_est=float(Lstart+2*np.pi*cons[1].dual_value),
                numerical_worst=worst,phasegap=float(pgap),status=prob.status,iterations=it+1,
                n0=n0,ppmax=ppmax,certified=False)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--d',type=float,required=True);ap.add_argument('--m',type=int,default=10)
    ap.add_argument('--eta',type=float,default=2e-5);ap.add_argument('--n0',type=int,default=20000)
    ap.add_argument('--Lstart',type=float,default=100.);ap.add_argument('--out',required=True)
    ap.add_argument('--basis',default='monomial',choices=['monomial','laguerre'])
    ap.add_argument('--empirical-N',type=int,default=0)
    ap.add_argument('--ppmax',type=int,default=1000);ap.add_argument('--phase-samples',type=int,default=64);ap.add_argument('--solver-tol',type=float,default=1e-8)
    args=ap.parse_args();start=time.time();r=search(args.d,args.m,args.eta,args.n0,ppmax=args.ppmax,Lstart=args.Lstart,representation=args.basis,empirical_N=args.empirical_N,phase_samples=args.phase_samples,solver_tol=args.solver_tol)
    if r:r['seconds']=time.time()-start;Path(args.out).write_text(json.dumps(r,indent=2))
    else:sys.exit(1)
