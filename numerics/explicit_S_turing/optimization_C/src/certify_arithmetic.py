"""Arb certificate for C_zeta, independent of numerical optimization.

For p<=P0, certify the entire truncated trigonometric polynomial by
interval derivative exclusion and second-order Taylor branch-and-bound.
All omitted prime powers (including those of p<=P0) enter the tail.

Tail: exact integration by parts against Delta(x)=psi(x)-x,
  tail <= int_N^inf g dx + (N-psi(N))*g(N)
            + int_logN^inf epsilon(e^L) exp((1-sigma)L) |h'-sigma*h| dL.
Use unconditional Johnston-Ramare-Trudgian, Lemmas 6--8:
epsilon <= .94/sqrt(x) for 11<x<=1e19; epsilon<=1.994e-8 for x>=exp(40);
epsilon <= .64673/log(x)^2 for x>=1e5. No global RH assumption.
Source: https://ramare-olivier.github.io/Maths/JRT_Submitted.pdf
"""
import sys,json,time,argparse,heapq,math
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
from flint import arb,acb,arb_poly,acb_poly,ctx
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'hybrid_asymptotic'))
from certutil import A,box,up_str,down_str,provenance,sha256

def certify(path,N=10**8,P0=1000,tol='1e-13',step='0.02'):
    start=time.time();sol=json.loads(Path(path).read_text());d=Q(sol['d']).limit_denominator(10**6)
    B=[tuple(b) for b in sol['B']];ctx.prec=max(256,8*max(j for _,j in B));c=[A(Q(x)) for x in sol['c']]
    assert N>=10**5 and P0<=N and d>Q(1,2)
    assert len(B)==len(c) and len(set(B))==len(B) and B[0]==('R',1)
    assert all((k=='R' and j>=1) or (k=='I' and j>=2) for k,j in B)
    pi=arb.pi();da=A(d);sig=A(d+Q(1,2));alpha=sig-1;deg=max(j for _,j in B)-1
    pa=[arb(0)]*(deg+1);pb=pa.copy()
    for (k,j),cc in zip(B,c):(pa if k=='R' else pb).__setitem__(j-1,-cc/math.factorial(j-1)/pi)
    ap=arb_poly(pa);bp=arb_poly(pb);ad=ap.derivative();bd=bp.derivative()
    az=acb_poly(pa);bz=acb_poly(pb)
    def ab(L):return ap(L),bp(L)+((-da*L).exp()-2)/(pi*L)
    def h(L):
        a,b=ab(L);return (a*a+b*b).sqrt()
    def maxprime(coef):
        # x=2*pi*q, q in [0,1]. Complete coverage; samples only provide lower bounds.
        def vals(q,order):
            x=2*pi*q;tot=arb(0)
            for k,a,b in coef:
                co=(k*x).cos();si=(k*x).sin()
                if order==0:tot+=a*co+b*si
                elif order==1:tot+=k*(-a*si+b*co)
            return tot
        H2=sum((k*k*(a*a+b*b).sqrt() for k,a,b in coef),arb(0))
        best=max([vals(A(Q(i,64)),0).lower() for i in range(64)])
        stack=[(Q(i,32),Q(i+1,32)) for i in range(32)];n=0;upper=best;eps=arb(tol)
        while stack:
            lo,hi=stack.pop();n+=1;m=(lo+hi)/2;r=pi*A(hi-lo);v=vals(A(m),0);dv=vals(A(m),1)
            best=max(best,v.lower());u=(v+abs(dv)*r+H2*r*r/2).upper()
            if u<=best+eps:upper=max(upper,u);continue
            derivative=dv+box(-Q(1),Q(1))*H2*r
            if derivative>0 or derivative<0:
                endpoint=hi if derivative>0 else lo;ev=vals(A(endpoint),0)
                best=max(best,ev.lower());upper=max(upper,ev.upper());continue
            stack.extend([(lo,m),(m,hi)])
            if n>200000:raise RuntimeError('phase isolation did not terminate')
        return upper,best,n
    print(provenance(path,__file__,ROOT/'hybrid_asymptotic/certutil.py'),flush=True)
    sieve=np.ones(N+1,dtype=bool);sieve[:2]=False
    for i in range(2,math.isqrt(N)+1):
        if sieve[i]:sieve[i*i::i]=False
    primes=np.flatnonzero(sieve);del sieve
    total=arb(0);psi=arb(0);gain=arb(0);pnodes=0;phase_lower=arb(0)
    for count,p0 in enumerate(primes):
        p=int(p0);lp=arb(p).log();n=p;k=1;coef=[];hyp=arb(0)
        while n<=N:
            L=k*lp;w=lp*(-sig*L).exp();a,b=ab(L);aa=w*a;bb=w*b
            hh=(aa*aa+bb*bb).sqrt();hyp+=hh;psi+=lp
            if p<=P0:coef.append((k,aa,bb))
            n*=p;k+=1
        if p<=P0:
            up,low,nodes=maxprime(coef);up=min(up,hyp.upper())
            total+=up;phase_lower+=low;gain+=hyp-up;pnodes+=nodes
        else:total+=hyp
        if count and count%1000000==0:print('summed primes',count,'seconds',time.time()-start,flush=True)
    print('partial',total,'psi',psi,'phase_gain',gain,'phase_boxes',pnodes,'seconds',time.time()-start,flush=True)
    L0=arb(N).log();Lfar=max(200,int((deg+30)/float(alpha)))
    def inc(k,X,beta):
        return (-beta*X).exp()*sum((arb(math.factorial(k))/math.factorial(i)*X**i/beta**(k-i+1) for i in range(k+1)),arb(0))
    qq=[abs(a)+abs(b) for a,b in zip(pa,pb)]
    while True:
        far=sum((q*inc(i,arb(Lfar),alpha) for i,q in enumerate(qq)),arb(0))+2*inc(0,arb(Lfar),alpha)
        if far<arb('1e-25'):break
        Lfar+=50
        assert Lfar<10000
    # Analytic integration uses Arb's rigorous adaptive Gauss quadrature.
    integ=acb(0);edges=[L0]+[arb(x) for x in range(math.ceil(float(L0)),Lfar+1,5)]
    if edges[-1]!=Lfar:edges.append(arb(Lfar))
    for l,r in zip(edges,edges[1:]):
        mid=(l+r)/2;shift=arb_poly([mid,1]);as_=acb_poly(ap(shift));bs_=acb_poly(bp(shift))
        def integrand(z,analytic):
            a=as_(z-mid);b=bs_(z-mid)+((-acb(da)*z).exp()-2)/(pi*z)
            return (a*a+b*b).sqrt(analytic=analytic)*(-acb(alpha)*z).exp()
        q=acb.integral(integrand,acb(l),acb(r),abs_tol=arb('1e-25'),rel_tol=arb('1e-20'),eval_limit=20000)
        assert q.is_finite() and q.imag.contains(0);integ+=q
    # h <= sum (|pa_i|+|pb_i|) L^i + 2/L, with 2/L<=2 for L>=1.
    I=integ.real+far
    # Certified interval quadrature for the absolute derivative error. Midpoint
    # polynomial forms reduce dependency; all endpoints are exact rationals.
    def polyball(p,dp,L):
        m=arb(L.mid());return p(arb_poly([m,1]))(L-m)
    def normupper(a,b):
        au=a.abs_upper();bu=b.abs_upper();return (au*au+bu*bu).sqrt().upper()
    def normball(a,b):
        al=a.abs_lower();bl=b.abs_lower();return (al*al+bl*bl).sqrt().lower().union(normupper(a,b))
    err=arb(0);l=Q(float(L0.lower())) # start to the left is safe, integrand nonnegative
    dl=Q(step);boxes=0
    while l<Lfar:
        r=min(l+dl,Q(Lfar));Lb=box(l,r);aa=polyball(ap,ad,Lb);be=(-da*Lb).exp()
        bb=polyball(bp,bd,Lb)+(be-2)/(pi*Lb);hh=normball(aa,bb)
        aa1=polyball(ad,ad.derivative(),Lb);bb1=polyball(bd,bd.derivative(),Lb)-da*be/(pi*Lb)-(be-2)/(pi*Lb*Lb)
        if hh>0:der=(aa*aa1+bb*bb1)/hh-sig*hh
        else:der=normupper(aa1,bb1)+sig*normupper(aa,bb)
        eps=arb('0.64673')/(Lb*Lb)
        if r<=40:eps=eps.min(arb('0.94')*(-Lb/2).exp())
        if l>=40:eps=eps.min(arb('1.994e-8'))
        bound=eps*(-alpha*Lb).exp()*abs(der)
        err+=bound.upper()*A(r-l);l=r;boxes+=1
    # For L>=Lfar>=40, use constant eps and polynomial absolute derivative bound.
    assert Lfar>=40
    farerr=arb(0)
    for i,q in enumerate(qq):
        farerr+=q*sig*inc(i,arb(Lfar),alpha)
        if i:farerr+=q*i*inc(i-1,arb(Lfar),alpha)
    # derivative of (exp(-dL)-2)/L bounded by d*exp(-dL)/L+2/L^2.
    farerr+=(2*sig+2)*inc(0,arb(Lfar),alpha)+da*inc(0,arb(Lfar),alpha+da)
    err+=arb('1.994e-8')*farerr
    correction=(N-psi)*h(L0)*(-sig*L0).exp();tail=I+correction+err
    Cz=total+tail
    result=dict(certified=True,N0=N,P0=P0,Czeta_upper=up_str(Cz,24),partial_upper=up_str(total,24),
                tail_upper=up_str(tail,24),integral_upper=up_str(I,24),far_upper=up_str(far,24),error_upper=up_str(err,24),
                boundary_correction_upper=up_str(correction,24),phase_gain_lower=down_str(gain,24),
                phase_boxes=pnodes,error_boxes=boxes,seconds=time.time()-start,
                input_sha256=sha256(path),code_sha256=sha256(__file__),Lfar=Lfar,
                theorem_source='JRT Lemmas 6,7,8; unconditional, ranges checked in code')
    body=json.dumps(result,indent=2)
    Path(path).with_name(Path(path).stem+f'_arithmetic_N{N}.json').write_text(body)
    Path(path).with_name(Path(path).stem+f'_arithmetic_N{N}_P{P0}_{result["code_sha256"][:10]}_step{step}.json').write_text(body)
    print(json.dumps(result,indent=2),flush=True);return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('path');ap.add_argument('--N',type=int,default=10**8);ap.add_argument('--P0',type=int,default=1000)
    ap.add_argument('--step',default='0.02');a=ap.parse_args();certify(a.path,a.N,a.P0,step=a.step)
