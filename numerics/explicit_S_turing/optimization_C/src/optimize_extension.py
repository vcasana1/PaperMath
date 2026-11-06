"""Local high-order experiments using all primes in primoss.bin.
Numerical search ONLY. Sparse extension is explicitly distinguished from a
full optimization of every coefficient. Positive quadrature preserves convexity.
Weighted Laguerre recurrence avoids forming L^1000 or factorials in floats.
"""
import sys,json,time,math,argparse
from pathlib import Path
from fractions import Fraction as Q
from decimal import Decimal,localcontext
import numpy as np
import cvxpy as cp
from scipy.optimize import minimize_scalar
BASE=Path(__file__).resolve().parents[1]

def weighted_laguerre(x,orders,alpha=0):
    x=np.array(x);want=set(orders);out={};prev=np.ones_like(x);cur=1+alpha-x;scale=np.zeros_like(x)
    def value(p):
        with np.errstate(divide='ignore',under='ignore'):
            return np.sign(p)*np.exp(np.log(np.abs(p))+scale-x/2)
    if 0 in want:out[0]=value(prev)
    if 1 in want:out[1]=value(cur)
    for k in range(1,max(orders)):
        nxt=((2*k+1+alpha-x)*cur-(k+alpha)*prev)/(k+1);prev,cur=cur,nxt
        large=np.maximum(np.abs(cur),np.abs(prev))>1e100
        if np.any(large):cur[large]*=1e-100;prev[large]*=1e-100;scale[large]+=100*np.log(10)
        if k+1 in want:out[k+1]=value(cur)
    return out

def empirical_file(path,PP=1000,width=.02):
    cache=BASE/'inputs/empirical_primoss_PP1000_width002.npz'
    if cache.exists():
        r=np.load(cache);return r['L'],r['W']
    p=np.memmap(path,dtype='<u8',mode='r');N=int(p[-1]);nb=int(math.log(10**10)/width)+2
    mu=np.zeros((6,nb));counts=np.zeros(nb,np.int64)
    def add(ps,k=1):
        L=k*np.log(ps.astype(float));w=np.log(ps.astype(float))*np.exp(-1.5*L)
        ids=np.floor(L/width).astype(np.int64);u=(L-(ids+.5)*width)/(width/2)
        counts[:]+=np.bincount(ids,minlength=nb)
        for r in range(6):mu[r,:]+=np.bincount(ids,weights=w*u**r,minlength=nb)
    start=time.time()
    for offset in range(0,len(p),1000000):
        ps=p[offset:offset+1000000];add(ps[ps>PP])
        if offset%100000000==0:print('prime moments',offset,'seconds',time.time()-start,flush=True)
    for k in range(2,int(math.log(10**10)/math.log(PP))+1):
        limit=int((10**10)**(1/k))+2;ps=p[np.searchsorted(p,PP+1):np.searchsorted(p,limit+1)]
        ps=np.array([v for v in ps if int(v)**k<=10**10],dtype=np.uint64)
        if len(ps):add(ps,k)
    Ls=[];Ws=[]
    for i in np.flatnonzero(counts):
        mom=mu[:,i]/mu[0,i];H=np.array([[mom[r+s] for s in range(3)] for r in range(3)]);H1=np.array([[mom[r+s+1] for s in range(3)] for r in range(3)])
        # Small groups occur only at the low end. A positive one-node rule
        # is allowed in SEARCH and is not a certification of the norm.
        try:
            ch=np.linalg.cholesky(H);ci=np.linalg.inv(ch);xx,V=np.linalg.eigh(ci@H1@ci.T)
            if np.max(np.abs(xx))>1.0001:raise ValueError('node')
            ww=mu[0,i]*V[0]**2
        except (ValueError,np.linalg.LinAlgError):xx=np.array([mom[1]]);ww=np.array([mu[0,i]])
        Ls.extend((i+.5)*width+xx*width/2);Ws.extend(ww)
    Ls=np.array(Ls);Ws=np.array(Ws);np.savez(cache,L=Ls,W=Ws)
    print('all file prime moments aggregated',len(p),'nodes',len(Ls),flush=True);return Ls,Ws

def search(a):
    start=time.time();m=a.m;d=1.;lam=1.;seed=json.loads(Path(a.seed).read_text())
    if a.sparse:
        js=sorted(set(range(1,101))|set(np.rint(np.geomspace(101,m,a.sparse)).astype(int)))
    else:js=list(range(1,m+1))
    B=[('R',j) for j in js]+[('I',j) for j in js if j>=2];n=len(B)
    print('local order',m,'free parameters',n,'full family',2*m-1,'sparse',bool(a.sparse),flush=True)
    def maps(L):
        R=weighted_laguerre(L,[j-1 for k,j in B if k=='R']);I=weighted_laguerre(L,[j-2 for k,j in B if k=='I'],1)
        return np.array([-(R[j-1] if k=='R' else np.zeros(len(L)))/np.pi for k,j in B]).T,np.array([-(L*I[j-2]/(j-1) if k=='I' else np.zeros(len(L)))/np.pi for k,j in B]).T
    L,W=empirical_file(a.primes);xg,wg=np.polynomial.legendre.leggauss(64)
    # Dense positive tail quadrature; SEARCH ONLY, extending with the order.
    # High-order Laguerre phases oscillate approximately in sqrt(L). The
    # denser independent recheck uses this coordinate too, with 128 nodes.
    edges=np.linspace(np.sqrt(np.log(10**10)),np.sqrt(max(700.,6*m+100)),max(48,m//8)+1);Lt=[];Wt=[]
    for lo,hi in zip(edges,edges[1:]):
        yy=(lo+hi)/2+(hi-lo)*xg/2;Lt.extend(yy*yy);Wt.extend((hi-lo)*wg*yy)
    Lall=np.r_[L,Lt];weights=np.r_[W*np.exp(L/2),Wt];RA,RB=maps(Lall);RA*=weights[:,None];RB*=weights[:,None]
    b0=weights*np.exp(-Lall/2)*(np.exp(-Lall)-2)/(np.pi*Lall)
    if Path(a.primes).exists():
        pf=np.memmap(a.primes,dtype='<u8',mode='r');small=pf[:np.searchsorted(pf,1001)];prime_count=len(pf)
    else:
        # The delivered positive quadrature contains all large-prime data.
        # Only this small deterministic list is needed separately afterwards.
        s=np.ones(1001,bool);s[:2]=False
        for p in range(2,32):
            if s[p]:s[p*p::p]=False
        small=np.flatnonzero(s);prime_count=json.loads((BASE/'inputs/primoss_source.json').read_text())['count']
        print('using delivered all-prime quadrature; binary unavailable',flush=True)
    groups=[]
    for p0 in small:
        p=int(p0);ks=np.arange(1,int(math.log(10**10)/math.log(p))+1);LL=ks*np.log(p);aa,bb=maps(LL);w=np.log(p)*np.exp(-LL)
        groups.append((ks,aa*w[:,None],bb*w[:,None],w*np.exp(-LL/2)*(np.exp(-LL)-2)/(np.pi*LL)))
    def rows(theta,beta=.5):
        theta=np.atleast_1d(theta);t=.5*np.tan(theta/2);beta=np.broadcast_to(beta,t.shape);z=[d+beta+1j*t,d-beta+1j*t]
        gg=np.zeros((len(t),n))
        for zz in z:
            w=1-lam/zz
            for col,(kind,j) in enumerate(B):
                off=1 if kind=='R' else 2;v=zz**(-off)*w**(j-off);gg[:,col]+=v.real if kind=='R' else -v.imag
        safe=np.where(t==0,1.,t)
        f1=np.sign(t)*np.pi-2*np.arctan(t/(d+beta))-2*np.arctan(t/(d-beta))+np.arctan(t/(2*d+beta))+np.arctan(t/(2*d-beta))
        f2=2*np.arctan((d+beta)/safe)+2*np.arctan((d-beta)/safe)-np.arctan((2*d+beta)/safe)-np.arctan((2*d-beta)/safe)
        f=np.where(np.abs(t)>=1,f2,f1);f=np.where(t==0,np.pi,f)
        return gg*(1+t[:,None]**2),f*(1+t*t)
    th=np.linspace(-np.pi+1e-4,np.pi-1e-4,max(5000,8*m));G,F=rows(th)
    gz,fz=rows(np.zeros(201),np.linspace(0,.5,201));G=np.vstack([G,gz]);F=np.r_[F,fz]
    first=np.array([1. if k=='R' else 0. for k,j in B]);second=np.array([-(j-1) if k=='R' else 0. for k,j in B])
    norms=np.maximum(np.linalg.norm(G,axis=0),1e-10);scale=1/norms
    phase=[list(np.linspace(0,2*np.pi,32,endpoint=False)) for _ in groups];eta=2e-7
    fine=np.linspace(-np.pi+1e-5,np.pi-1e-5,max(24000,40*m));GF,FF=rows(fine)
    for it in range(a.maxit):
        y=cp.Variable(n);v=cp.multiply(scale,y);ep=cp.Variable(len(groups));constraints=[G@v>=F+eta,first@v<=2*np.pi*.08382-1e-10,(2*first-2*second)@v>=eta]
        for i,(ks,aa,bb,beta) in enumerate(groups):
            xx=np.array(phase[i]);co=np.cos(np.outer(xx,ks));si=np.sin(np.outer(xx,ks));constraints.append(ep[i]>=(co@aa+si@bb)@v+si@beta)
        Cz=cp.sum(ep)+cp.sum(cp.norm(cp.vstack([RA@v,RB@v+b0]),axis=0));obj=Cz-(first@v)/(2*np.pi)*np.log(2*np.pi)+((first@v)/(2*np.pi)-.08382)*135
        prob=cp.Problem(cp.Minimize(obj),constraints);prob.solve(solver='CLARABEL',tol_gap_abs=1e-8,tol_feas=1e-9,tol_gap_rel=1e-9,max_iter=200)
        if v.value is None:raise RuntimeError(prob.status)
        vv=v.value;h=GF@vv-FF-eta;idx=np.where((h<1e-3)&(h<=np.roll(h,1))&(h<=np.roll(h,-1)))[0];new=[];worst=float(h.min())
        for j in idx:
            if j==0 or j==len(fine)-1:continue
            r=minimize_scalar(lambda x:float((lambda g,f:g@vv-f-eta)(*rows(x))[0]),bounds=(fine[j-1],fine[j+1]),method='bounded')
            worst=min(worst,r.fun)
            if r.fun<-1e-8:new.append(r.x)
        gap=0.
        for i,(ks,aa,bb,beta) in enumerate(groups):
            ar=aa@vv;bi=bb@vv+beta;xx=np.linspace(0,2*np.pi,256,endpoint=False);values=np.cos(np.outer(xx,ks))@ar+np.sin(np.outer(xx,ks))@bi
            for j in np.where((values>=np.roll(values,1))&(values>=np.roll(values,-1)))[0]:
                r=minimize_scalar(lambda x:-float(np.cos(ks*x)@ar+np.sin(ks*x)@bi),bounds=(xx[j]-2*np.pi/256,xx[j]+2*np.pi/256),method='bounded')
                gap=max(gap,-r.fun-ep.value[i])
                if -r.fun-ep.value[i]>2e-8:phase[i].append(r.x)
        print(json.dumps(dict(iteration=it,m=m,n=n,C_est=float(prob.value),worst=worst,newcuts=len(new),phasegap=gap,seconds=time.time()-start)),flush=True)
        if not new and gap<2e-8:break
        if new:gg,ff=rows(new);G=np.vstack([G,gg]);F=np.r_[F,ff]
    full=[('R',j) for j in range(1,m+1)]+[('I',j) for j in range(2,m+1)];pars=[Q(0)]*len(full)
    for bj,val in zip(B,vv):pars[full.index(bj)]=Q(repr(float(val)))
    old=[Q(0)]*len(full)
    for (kind,j),v0 in zip(full,pars):
        if not v0:continue
        off=1 if kind=='R' else 2
        for k in range(j-off+1):old[full.index((kind,k+off))]+=v0*math.comb(j-off,k)*(-1)**k
    with localcontext() as dc:
        dc.prec=10*(m+2);ps=[str(Decimal(x.numerator)/Decimal(x.denominator)) for x in pars];cs=[str(Decimal(x.numerator)/Decimal(x.denominator)) for x in old]
    out=dict(d='1.0',m=m,B=full,c=cs,parameters=ps,representation='laguerre',discs=[],kappa=[],certified=False,C_est=float(prob.value),
             numerical_worst=worst,phasegap=gap,free_parameters=n,sparse_extension=bool(a.sparse),prime_file=a.primes,prime_count=prime_count,tail_Lmax=max(700.,6*m+100),seconds=time.time()-start)
    Path(a.out).write_text(json.dumps(out,indent=2));print('saved numerical candidate',a.out,flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--m',type=int,required=True);ap.add_argument('--sparse',type=int,default=0);ap.add_argument('--maxit',type=int,default=8)
    ap.add_argument('--primes',required=True);ap.add_argument('--seed',default='candidates/d100_m100_lowmargin.json');ap.add_argument('--out',required=True);search(ap.parse_args())
