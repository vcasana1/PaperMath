"""Adaptation of screen_geometry_joint_general.py: explicit user-selected slope.
Numerical screening only. Original scripts and certificates are preserved.
The supplied geometry pool carries the certified explicit boundary costs.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"src"))
"""Execute convex finite-height screening of circles/rectangles. NOT A PROOF.
Objective covers a grid of ALL high-height residuals, refines the analytic
log-height peak, and constrains its derivative beyond the last height.
All arithmetic data are aggregated from the author's complete prime binary.
"""
import sys,json,time,math,argparse
from pathlib import Path
from fractions import Fraction as Q
from decimal import Decimal,localcontext
import numpy as np
import cvxpy as cp
from scipy.optimize import minimize_scalar,minimize
from scipy.special import zeta as real_zeta
from geometry_jensen import make_pool,matrix,weight
from geometry_curves import curves,points as curve_points
from optimize_extension import weighted_laguerre,empirical_file
BASE=Path(__file__).resolve().parents[2];sys.path.insert(0,str(BASE/"src"))

def run(args):
    start=time.time();TARGET=float(args.slope);d=float(args.d);lam=2*d-1;lamq=2*Q(args.d)-1;assert d>.5;m=args.m;B=[('R',j) for j in range(1,m+1)]+[('I',j) for j in range(2,m+1)];n=len(B);pool=json.loads(Path(args.pool).read_text()) if args.pool else make_pool(args.geometry)
    seed=json.loads(Path(args.seed).read_text()) if args.seed else None
    print('LOCAL GEOMETRY SCREEN m',m,'coefficients',n,'geometries',len(pool),'mode',args.geometry,flush=True)
    DC=np.array([g['cost'] for g in pool]);J,Gc,Ac=DC.T;Ac=Ac.copy()-np.array([np.log(real_zeta(g['c'],1)/real_zeta(2*g['c'],1)) for g in pool])
    print('geometry cost ranges',DC.min(axis=0),DC.max(axis=0),'setup seconds',time.time()-start,flush=True)
    def maps(L):
        R=weighted_laguerre(lam*L,list(range(m)));I=weighted_laguerre(lam*L,list(range(m-1)),1)
        a=np.column_stack([-R[j-1]/np.pi for j in range(1,m+1)]+[np.zeros(len(L)) for j in range(2,m+1)])
        b=np.column_stack([np.zeros(len(L)) for j in range(1,m+1)]+[-L*I[j-2]/((j-1)*np.pi) for j in range(2,m+1)])
        return a,b
    far=max(700.,25/min(g['c']-1 for g in pool));L,W=empirical_file(args.primes);x,w=np.polynomial.legendre.leggauss(32);edges=np.linspace(np.log(10**10),far,math.ceil(far/8)+1);Lt=[];Wt=[]
    for lo,hi in zip(edges,edges[1:]):
        y=(lo+hi)/2+(hi-lo)*x/2;Lt.extend(y);Wt.extend(w*(hi-lo)/2)
    Lall=np.r_[L,Lt];weights=np.r_[W*np.exp(L/2),Wt];RA,RB=maps(Lall);RA*=weights[:,None];RB*=weights[:,None];b0=weights*np.exp(-(d-.5)*Lall)*(np.exp(-d*Lall)-2)/(np.pi*Lall)
    CA=np.column_stack([-weights*np.exp(-(g['c']-1)*Lall)*np.cos(g['v']*Lall)/(np.pi*Lall) for g in pool]);CB=np.column_stack([weights*np.exp(-(g['c']-1)*Lall)*np.sin(g['v']*Lall)/(np.pi*Lall) for g in pool])
    sv=np.ones(1001,bool);sv[:2]=False
    for p in range(2,32):
        if sv[p]:sv[p*p::p]=False
    groups=[]
    for p in np.flatnonzero(sv):
        ks=np.arange(1,int(np.log(10**10)/np.log(p))+1);ll=ks*np.log(p);a,b=maps(ll);ww=np.log(p)*np.exp(-ll)
        ca=np.column_stack([-np.log(p)*np.exp(-g['c']*ll)*np.cos(g['v']*ll)/(np.pi*ll) for g in pool]);cb=np.column_stack([np.log(p)*np.exp(-g['c']*ll)*np.sin(g['v']*ll)/(np.pi*ll) for g in pool])
        groups.append((ks,a*ww[:,None],b*ww[:,None],ww*np.exp(-(d-.5)*ll)*(np.exp(-d*ll)-2)/(np.pi*ll),ca,cb))
    def rows(beta,t):
        beta,t=np.broadcast_arrays(beta,t);out=np.zeros((len(t),n))
        for z in [d+beta+1j*t,d-beta+1j*t]:
            w0=1-lam/z
            for col,(kind,j) in enumerate(B):
                off=1 if kind=='R' else 2;zz=z**(-off)*w0**(j-off);out[:,col]+=zz.real if kind=='R' else -zz.imag
        safe=np.where(t==0,1.,t);ff=np.sign(t)*np.pi-2*np.arctan(t/(d+beta))-2*np.arctan(t/(d-beta))+np.arctan(t/(2*d+beta))+np.arctan(t/(2*d-beta))
        direct=2*np.arctan((d+beta)/safe)+2*np.arctan((d-beta)/safe)-np.arctan((2*d+beta)/safe)-np.arctan((2*d-beta)/safe)
        ff=np.where(np.abs(t)>=1,direct,ff);ff=np.where(t==0,np.pi,ff);return out,ff
    th=np.linspace(-np.pi+1e-4,np.pi-1e-4,1001);t=.5*np.tan(th/2);t[500]=0
    bb,tt=[a.ravel() for a in np.meshgrid(np.linspace(0,.5,11),t,indexing='ij')];raw,F=rows(bb,tt);factor=1+tt*tt;K=raw*factor[:,None];F*=factor;WK=matrix(pool,bb,tt,factor)
    if seed:
        sg=seed['geometries'];T=math.ceil(max(abs(g['v'])+(g['H'] if g['kind']=='rectangle' else g['R']) for g in sg))+1
        for curve in curves(sg,T):
            b,t=curve_points(curve,np.linspace(-1,1,101));gg,ff=rows(b,t);fac=1+t*t;K=np.vstack([K,gg*fac[:,None]]);F=np.r_[F,ff*fac]
            from scipy import sparse
            WK=sparse.vstack([WK,matrix(pool,b,t,fac)]).tocsr()
    first=np.r_[np.ones(m),np.zeros(m-1)];second=np.r_[-np.arange(m),np.zeros(m-1)];scale=1/np.maximum(np.linalg.norm(K,axis=0),1e-8)
    Lmin=40.;heights=list(np.geomspace(Lmin,100000.,121));phase=[list(np.linspace(0,2*np.pi,32,endpoint=False)) for _ in groups];eta=2e-7
    if seed:
        assert seed['m']==m;vv=np.array(seed['parameters'],float)
        def key(g):return json.dumps({k:v for k,v in g.items() if k!='cost'},sort_keys=True)
        mapping={key(g):float(w) for g,w in zip(seed['geometries'],seed['geometry_weights'])};seed_k=np.array([mapping.get(key(g),0.) for g in pool])
        for i,(ks,a,b,beta,ca,cb) in enumerate(groups):
            ar=a@vv+ca@seed_k;bi=b@vv+cb@seed_k+beta;xx=np.linspace(0,2*np.pi,512,endpoint=False);pv=np.cos(np.outer(xx,ks))@ar+np.sin(np.outer(xx,ks))@bi
            j=int(np.argmax(pv));r=minimize_scalar(lambda x:-float(np.cos(ks*x)@ar+np.sin(ks*x)@bi),bounds=(xx[j]-2*np.pi/512,xx[j]+2*np.pi/512),method='bounded');phase[i].append(r.x)
    for it in range(args.maxit):
        y=cp.Variable(n);v=cp.multiply(scale,y);kap=cp.Variable(len(pool),nonneg=True);ep=cp.Variable(len(groups));zeta=cp.Variable();C=cp.Variable()
        Ak=first@v/(2*np.pi);At=Ak+J@kap/np.pi;Bc=Gc@kap/np.pi;R=zeta-Ak*np.log(2*np.pi)+Ac@kap/np.pi
        cons=[K@v+WK@kap>=F+eta,(2*d*first-2*lam*second)@v>=eta,At+Bc/max(heights)<=TARGET-1e-10]
        la=json.loads((BASE/'inputs/low_L60_arithmetic_N1000000.json').read_text());le=json.loads((BASE/'inputs/low_L60_elemS.json').read_text())
        cons.append(C>=float(la['Czeta_upper'])+float(le['Fsup_upper'])+(float(le['A1'])-TARGET)*Lmin)
        for i,(ks,a,b,beta,ca,cb) in enumerate(groups):
            xx=np.array(phase[i]);co=np.cos(np.outer(xx,ks));si=np.sin(np.outer(xx,ks));cons.append(ep[i]>=(co@a+si@b)@v+(co@ca+si@cb)@kap+si@beta)
        cons.append(zeta>=cp.sum(ep)+cp.sum(cp.norm(cp.vstack([RA@v+CA@kap,RB@v+CB@kap+b0]),axis=0)))
        for h in heights:cons.append((C-R)/h>=At-TARGET+Bc*(np.log(h)+np.pi*np.pi/(8*h*h))/h)
        prob=cp.Problem(cp.Minimize(C),cons);prob.solve(solver='CLARABEL',tol_gap_abs=1e-8,tol_gap_rel=1e-9,tol_feas=1e-9,max_iter=250)
        if v.value is None:raise RuntimeError(prob.status)
        vv=v.value;kv=np.maximum(kap.value,0);used=np.flatnonzero(kv>1e-7);active=[pool[i] for i in used];uv=kv[used]
        gap=0.
        for i,(ks,a,b,beta,ca,cb) in enumerate(groups):
            ar=a@vv+ca@kv;bi=b@vv+cb@kv+beta;xx=np.linspace(0,2*np.pi,256,endpoint=False);pv=np.cos(np.outer(xx,ks))@ar+np.sin(np.outer(xx,ks))@bi
            for j in np.where((pv>=np.roll(pv,1))&(pv>=np.roll(pv,-1)))[0]:
                res=minimize_scalar(lambda x:-float(np.cos(ks*x)@ar+np.sin(ks*x)@bi),bounds=(xx[j]-2*np.pi/256,xx[j]+2*np.pi/256),method='bounded')
                gap=max(gap,-res.fun-ep.value[i])
                if -res.fun-ep.value[i]>2e-8:phase[i].append(res.x)
        # Complete finite search is numerical; subsequent proof would need
        # whole-domain interval verification of the Green-weighted inequality.
        def residual(b,t):
            a,f=rows(np.atleast_1d(b),np.atleast_1d(t));h=a@vv-f
            for g,k in zip(active,uv):h+=k*weight(g,np.atleast_1d(b),np.atleast_1d(t))
            return h*(1+np.atleast_1d(t)**2)-eta
        fine=.5*np.tan(np.linspace(-np.pi+1e-5,np.pi-1e-5,6001)/2);fine[3000]=0.;points=[];worst=1.
        for b in np.linspace(0,.5,21):
            h=residual(np.full(len(fine),b),fine);worst=min(worst,float(h.min()));idx=np.where((h<-1e-8)&(h<=np.roll(h,1))&(h<=np.roll(h,-1)))[0]
            for j in idx:points.append((b,float(fine[j])))
        for b,t in sorted(points,key=lambda bt:float(residual(*bt)[0]))[:20]:
            sign=1 if t>=0 else -1
            def fun(q):return float(residual(np.clip(q[0],0,.5),sign*max(abs(q[1]),1e-12))[0])
            res=minimize(fun,[b,t],method='Nelder-Mead',options={'maxiter':150,'xatol':1e-8,'fatol':1e-11});worst=min(worst,float(res.fun));points.append((float(np.clip(res.x[0],0,.5)),sign*max(abs(float(res.x[1])),1e-12)))
        at=float(At.value);bc=float(Bc.value);peak=max(Lmin,bc/(TARGET-at)) if bc>0 and at<TARGET else Lmin
        actual_peak=float(R.value)+(at-TARGET)*peak+bc*(np.log(peak)+np.pi*np.pi/(8*peak*peak));height_gap=actual_peak-float(C.value)
        print(json.dumps(dict(iteration=it,C_numerical=float(C.value),A_total=at,B_loglog=bc,geometries_used=len(used),kappa_sum=float(kv.sum()),worst=worst,phasegap=gap,peak_logT=peak,height_gap=height_gap,seconds=time.time()-start)),flush=True)
        if points:
            pb=np.array([p[0] for p in points]);pt=np.array([p[1] for p in points]);gg,ff=rows(pb,pt);fac=1+pt*pt
            K=np.vstack([K,gg*fac[:,None]]);F=np.r_[F,ff*fac];from scipy import sparse
            WK=sparse.vstack([WK,matrix(pool,pb,pt,fac)]).tocsr()
        if height_gap>1e-7:heights.append(peak)
        if not points and gap<2e-8 and height_gap<1e-7:break
    pars=[Q(repr(float(x))) for x in vv];old=[Q(0)]*n
    for col,(kind,j) in enumerate(B):
        off=1 if kind=='R' else 2
        for k in range(j-off+1):old[B.index((kind,k+off))]+=pars[col]*math.comb(j-off,k)*(-lamq)**k
    with localcontext() as dc:
        dc.prec=10*(m+2);coeff=[str(Decimal(v.numerator)/Decimal(v.denominator)) for v in old]
    keep=np.flatnonzero(kv>1e-9)
    out=dict(d=args.d,m=m,B=B,c=coeff,parameters=[repr(float(x)) for x in vv],representation='laguerre',
       certified=False,target_slope=args.slope,centre_coupled=True,tail_Lmax=far,geometry_pool_size=len(pool),geometry_mode=args.geometry,geometries=[pool[i] for i in keep],geometry_weights=[repr(float(kv[i])) for i in keep],
       C_numerical=float(C.value),A_total_numerical=at,B_loglog_numerical=bc,peak_logT_numerical=peak,
       numerical_worst=worst,phasegap=gap,height_gap=height_gap,seconds=time.time()-start,
       limitations='Numerical geometry integrals and finite constraints; no global geometric inequality certificate. PL finite-height corrections still need interval assembly. Not a new uniform bound.')
    Path(args.out).write_text(json.dumps(out,indent=2));print('saved SCREEN ONLY',args.out,flush=True)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--slope',required=True);ap.add_argument('--m',type=int,default=40);ap.add_argument('--d',default='1.0');ap.add_argument('--maxit',type=int,default=4);ap.add_argument('--geometry',choices=['circle','rectangle','both'],default='both');ap.add_argument('--primes',required=True);ap.add_argument('--out',required=True);ap.add_argument('--pool');ap.add_argument('--seed');run(ap.parse_args())
