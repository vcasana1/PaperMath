"""Convex outer approximation of the arithmetic SOCP, solved by HiGHS.
Each norm-block tangent and prime phase gives a globally valid cutting
plane for the finite numerical objective. All final proofs are independent.
Laguerre representation permits higher orders without coefficient scaling.
"""
import sys,json,time,math,argparse
from pathlib import Path
from fractions import Fraction as Q
from decimal import Decimal,localcontext
import numpy as np
from scipy.special import eval_laguerre,eval_genlaguerre
from scipy.optimize import linprog,minimize_scalar
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'family'))
from opt_line import basis,primes

def search(d,m,out,eta=1e-7,n0=20000,PP=300,maxit=150):
    start=time.time();B=basis(m,m);n=len(B);lam=2*d-1;cap=.08382;Lstart=100.
    def maps(L):
        a=np.zeros((len(L),n));b=a.copy()
        for col,(k,j) in enumerate(B):
            if k=='R':a[:,col]=-eval_laguerre(j-1,lam*L)/np.pi
            else:b[:,col]=-L*eval_genlaguerre(j-2,1,lam*L)/((j-1)*np.pi)
        return a,b
    def krows(bb,tt):
        zz=[d+bb+1j*tt,d-bb+1j*tt];row=[]
        for k,j in B:
            off=1 if k=='R' else 2;v=sum(z**(-off)*(1-lam/z)**(j-off) for z in zz)
            row.append(v.real if k=='R' else -v.imag)
        ff=np.sign(tt)*np.pi-2*np.arctan(tt/(d+bb))-2*np.arctan(tt/(d-bb))+np.arctan(tt/(2*d+bb))+np.arctan(tt/(2*d-bb))
        safe=np.where(tt==0,1.,tt)
        direct=2*np.arctan((d+bb)/safe)+2*np.arctan((d-bb)/safe)-np.arctan((2*d+bb)/safe)-np.arctan((2*d-bb)/safe)
        ff=np.where(np.abs(tt)>=1,direct,ff)
        ff=np.where(tt==0,np.pi,ff)
        return np.array(row).T*(1+tt[:,None]**2),ff*(1+tt**2)+eta
    ts=np.unique(np.r_[0.,np.linspace(0,5,400),np.geomspace(1e-6,3000,600)])
    ts=np.r_[-ts[:0:-1],ts];K,ff=krows(np.full_like(ts,.5),ts)
    kz,fz=krows(np.linspace(0,.5,101),np.zeros(101));K=np.vstack([K,kz]);ff=np.r_[ff,fz]
    cR1=np.r_[np.ones(m),np.zeros(m-1)];cR2=np.r_[-lam*np.arange(m),np.zeros(m-1)]
    LR=[];WR=[];PR=[];KR=[]
    for p in primes(n0):
        lp=np.log(p);k=1;nn=int(p)
        while nn<=n0:
            L=k*lp;LR.append(L);WR.append(lp*np.exp(-(d+.5)*L));PR.append(p);KR.append(k);nn*=int(p);k+=1
    xn,wn=np.polynomial.legendre.leggauss(180)
    edges=[np.log(n0),20.,40.,80.,160.,320.,700.]
    for l,r in zip(edges,edges[1:]):
        L=(l+r)/2+(r-l)*xn/2;LR.extend(L);WR.extend((r-l)*wn/2*np.exp((.5-d)*L));PR.extend(np.zeros(len(L),int));KR.extend(np.zeros(len(L),int))
    L=np.array(LR);w=np.array(WR);pof=np.array(PR);ks=np.array(KR);a,b=maps(L)
    a*=w[:,None];b*=w[:,None];b0=w*(np.exp(-d*L)-2)/(L*np.pi)
    pgroups=[]
    for p in primes(PP):
        mask=pof==p;pgroups.append((ks[mask],a[mask],b[mask],b0[mask]))
    mask=(pof==0)|(pof>PP);aa=a[mask];bb=b[mask];beta=b0[mask]
    groups=[x for x in np.array_split(np.arange(len(aa)),24) if len(x)]
    ng=len(groups);np_=len(pgroups);nv=n+ng+np_
    rows=[];rhs=[]
    def add(cr,offset,index=None):
        rr=np.zeros(nv);rr[:n]=cr
        if index is not None:rr[index]=1.
        rows.append(rr);rhs.append(offset)
    for r,f in zip(K,ff):add(r,f)
    add(-cR1,-2*np.pi*cap+1e-10);add(2*d*cR1-2*cR2,eta)
    # Epigraphs start at zero; all arithmetic components are nonnegative.
    for i in range(ng+np_):add(np.zeros(n),0,n+i)
    for gi,(kk,ra,rb,bz) in enumerate(pgroups):
        xx=np.linspace(0,2*np.pi,32,endpoint=False)
        for x in xx:add(-(np.cos(kk*x)@ra+np.sin(kk*x)@rb),np.sin(kk*x)@bz,n+ng+gi)
    # Start from a feasible, lower-order kernel when available at the same d.
    params=np.zeros(n);best=None
    src=Path(out).parent/f'd{int(round(d*100)):03d}_m40_lag.json'
    if src.exists():
        sr=json.loads(src.read_text());sv=np.array(sr['parameters'],float);params[:40]=sv[:40];params[m:m+39]=sv[40:]
    else:params[0]=.6
    obj=np.r_[cR1*(Lstart-np.log(2*np.pi))/(2*np.pi),np.ones(ng+np_)]
    finep=np.geomspace(1e-8,1e5,10000);fine=np.r_[-finep[::-1],0.,finep]
    fineK,fineF=krows(np.full_like(fine,.5),fine)
    for it in range(maxit):
        ax=aa@params;bx=bb@params+beta;hh=np.hypot(ax,bx);hval=0.
        for gi,idx in enumerate(groups):
            ux=np.divide(ax[idx],hh[idx],out=np.zeros(len(idx)),where=hh[idx]>0)
            uy=np.divide(bx[idx],hh[idx],out=np.zeros(len(idx)),where=hh[idx]>0)
            gradient=ux@aa[idx]+uy@bb[idx];off=uy@beta[idx]
            add(-gradient,off,n+gi);hval+=hh[idx].sum()
        ppvalue=0.
        for gi,(kk,ra,rb,bz) in enumerate(pgroups):
            ar=ra@params;bi=rb@params+bz;xx=np.linspace(0,2*np.pi,128,endpoint=False)
            vv=np.cos(np.outer(xx,kk))@ar+np.sin(np.outer(xx,kk))@bi;j=int(np.argmax(vv))
            res=minimize_scalar(lambda x:-float(np.cos(kk*x)@ar+np.sin(kk*x)@bi),bounds=(xx[j]-2*np.pi/128,xx[j]+2*np.pi/128),method='bounded')
            x=res.x;cr=np.cos(kk*x)@ra+np.sin(kk*x)@rb;offset=np.sin(kk*x)@bz
            add(-cr,offset,n+ng+gi);ppvalue-=res.fun
        full=hval+ppvalue+obj[:n]@params-cap*Lstart
        violation=fineF-fineK@params;worst=float(violation.max())
        idx=np.where((violation>1e-9)&(violation>=np.roll(violation,1))&(violation>=np.roll(violation,-1)))[0]
        for i in idx:add(fineK[i],fineF[i])
        if worst<1e-8 and (best is None or full<best[0]):best=(full,params.copy())
        rr=np.array(rows);rs=np.array(rhs)
        res=linprog(obj,A_ub=-rr,b_ub=-rs,bounds=[(-10.,10.)]*n+[(None,None)]*(ng+np_),method='highs',options={'dual_feasibility_tolerance':1e-8,'primal_feasibility_tolerance':1e-8})
        if not res.success:print('LP failed',res.message,flush=True);break
        low=res.fun-cap*Lstart;gap=(best[0]-low) if best else float('inf')
        print(json.dumps(dict(it=it,d=d,m=m,full=full,best=best[0] if best else None,lower=low,gap=gap,worst=worst,rows=len(rows),seconds=time.time()-start)),flush=True)
        Path(out).with_suffix('.checkpoint.json').write_text(json.dumps(dict(d=str(d),m=m,B=B,parameters=[repr(float(x)) for x in params],representation='laguerre',C_est=full,certified=False,iteration=it,numerical_worst=worst)))
        params=res.x[:n]
        if gap<1e-7 and worst<1e-8:break
    if best is None:raise RuntimeError('no numerically feasible candidate')
    val,params=best;old=[Q(0) for _ in B];lq=2*Q(str(d))-1;pars=[repr(float(x)) for x in params]
    for col,(kind,j) in enumerate(B):
        off=1 if kind=='R' else 2
        for k in range(j-off+1):old[B.index((kind,k+off))]+=Q(pars[col])*math.comb(j-off,k)*(-lq)**k
    with localcontext() as dc:
        dc.prec=400;coeff=[str(Decimal(x.numerator)/Decimal(x.denominator)) for x in old]
    result=dict(d=str(d),m=m,B=B,c=coeff,parameters=pars,representation='laguerre',C1=float(cR1@params/(2*np.pi)),
                C_est=val,Cz_est=float(val-(obj[:n]@params-cap*Lstart)),discs=[],kappa=[],eta=eta,
                certified=False,solver='HiGHS convex outer approximation',numerical_gap=gap,numerical_lower=low,
                seconds=time.time()-start,iterations=it+1,quadrature='180 Gauss nodes per panel',ppmax=PP)
    Path(out).write_text(json.dumps(result,indent=2));return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--d',type=float,default=1.);ap.add_argument('--m',type=int,required=True);ap.add_argument('--out',required=True);ap.add_argument('--maxit',type=int,default=150);a=ap.parse_args();search(a.d,a.m,a.out,maxit=a.maxit)
