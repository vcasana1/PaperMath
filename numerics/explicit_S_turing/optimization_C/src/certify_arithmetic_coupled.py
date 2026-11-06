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
CODE_HASH=sha256(__file__)

def certify(path,N=10**8,P0=1000,tol='1e-16',step='0.02',binwidth='0.0001',extra=10**30,chunk_size=5000000):
    start=time.time();sol=json.loads(Path(path).read_text());d=Q(sol['d']).limit_denominator(10**6)
    B=[tuple(b) for b in sol['B']];ctx.prec=max(256,8*max(j for _,j in B));c=[A(Q(x)) for x in sol['c']]
    assert N>=10**5 and P0<=N and d>Q(1,2)
    assert len(B)==len(c) and len(set(B))==len(B) and B[0]==('R',1)
    assert all((k=='R' and j>=1) or (k=='I' and j>=2) for k,j in B)
    pi=arb.pi();da=A(d);sigbase=A(d+Q(1,2));deg=max(j for _,j in B)-1
    assert len(sol['geometries'])==len(sol['geometry_weights'])
    centre_q=[(Q(str(g['c'])),Q(str(g['v'])),Q(k)) for g,k in zip(sol['geometries'],sol['geometry_weights'])]
    assert all(cc>1 and kk>=0 for cc,vv,kk in centre_q)
    sigq=min([d+Q(1,2)]+[cc for cc,vv,kk in centre_q]);sig=A(sigq);alpha=sig-1;alpha_base=sigbase-1;beta_base=sigbase-sig
    centres=[(A(cc),A(vv),A(kk)) for cc,vv,kk in centre_q]
    pa=[arb(0)]*(deg+1);pb=pa.copy()
    for (k,j),cc in zip(B,c):(pa if k=='R' else pb).__setitem__(j-1,-cc/math.factorial(j-1)/pi)
    ap=arb_poly(pa);bp=arb_poly(pb);ad=ap.derivative();bd=bp.derivative()
    az=acb_poly(pa);bz=acb_poly(pb)
    def ab(L):
        factor=(-beta_base*L).exp();aa=factor*ap(L);bb=factor*(bp(L)+((-da*L).exp()-2)/(pi*L))
        for cc,vv,kk in centres:
            z=-kk/(pi*L)*acb(-(cc-sig)*L,-vv*L).exp();aa+=z.real;bb+=z.imag
        return aa,bb
    def h(L):
        a,b=ab(L);return (a*a+b*b).sqrt()
    def maxprime(coef):
        if len(coef)==1:
            _,a,b=coef[0];v=(a*a+b*b).sqrt()
            return v.upper(),v.lower(),1
        # Independent global phase bound. Write x=phi_1+delta, |delta|<=pi.
        # 1-cos(delta)>=2*delta^2/pi^2, and the higher harmonics have
        # Lipschitz constant L. Maximizing -2*R*delta^2/pi^2+L*|delta|
        # gives R+g(phi_1)+pi^2*L^2/(8*R). This requires no phase mesh.
        _,a1,b1=coef[0];R=(a1*a1+b1*b1).sqrt();analytic=None;phi_lower=None
        if R>0:
            unit=acb(a1/R,b1/R);value=R;lip=arb(0)
            for k,a,b in coef[1:]:
                power=unit**k;value+=a*power.real+b*power.imag;lip+=k*(a*a+b*b).sqrt()
            analytic=(value+pi*pi*lip*lip/(8*R)).upper();phi_lower=value.lower()
            if analytic<=phi_lower+arb(tol):return analytic,phi_lower,1
        # x=2*pi*q, q in [0,1]. Complete coverage; samples only provide lower bounds.
        def vals(q,order):
            x=2*pi*q;tot=arb(0)
            for k,a,b in coef:
                co=(k*x).cos();si=(k*x).sin()
                if order==0:tot+=a*co+b*si
                elif order==1:tot+=k*(-a*si+b*co)
            return tot
        H2=sum((k*k*(a*a+b*b).sqrt() for k,a,b in coef),arb(0))
        best=max([vals(A(Q(i,64)),0).lower() for i in range(64)]+([phi_lower] if phi_lower is not None else []))
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
        return min(upper,analytic) if analytic is not None else upper,best,n
    print(provenance(path,__file__,ROOT/'hybrid_asymptotic/certutil.py'),flush=True)
    direct_limit=max(P0,math.isqrt(N),100000)
    direct_limit=min(N,direct_limit)
    sieve=np.ones(direct_limit+1,dtype=bool);sieve[:2]=False
    for i in range(2,math.isqrt(direct_limit)+1):
        if sieve[i]:sieve[i*i::i]=False
    primes=np.flatnonzero(sieve);del sieve
    total=arb(0);psi=arb(0);gain=arb(0);pnodes=0;phase_lower=arb(0);removed=arb(0)
    for count,p0 in enumerate(primes):
        p=int(p0);lp=arb(p).log();n=p;k=1;coef=[];hyp=arb(0)
        limit=max(N,extra) if p<=P0 else N
        while n<=limit:
            L=k*lp;w=lp*(-sig*L).exp();a,b=ab(L);aa=w*a;bb=w*b
            hh=(aa*aa+bb*bb).sqrt();hyp+=hh
            if n<=N:psi+=lp
            else:removed+=hh.lower()
            if p<=P0:coef.append((k,aa,bb))
            n*=p;k+=1
        if p<=P0:
            up,low,nodes=maxprime(coef);up=min(up,hyp.upper())
            total+=up;phase_lower+=low;gain+=hyp-up;pnodes+=nodes
        else:total+=hyp
        if count and count%1000000==0:print('summed primes',count,'seconds',time.time()-start,flush=True)
    # Remaining primes exceed sqrt(N), hence have no higher power <=N.
    # Grouping is an exact partition by integer endpoints and exact counts.
    # Floating-point logs choose the groups only; all enclosures use Arb logs
    # of the actual smallest and largest prime in each group.
    assert direct_limit>=math.isqrt(N)
    base_sieve=np.ones(math.isqrt(N)+1,dtype=bool);base_sieve[:2]=False
    for q in range(2,math.isqrt(math.isqrt(N))+1):
        if base_sieve[q]:base_sieve[q*q::q]=False
    base_primes=np.flatnonzero(base_sieve).tolist();del base_sieve
    cache={};bins=0;primecount=len(primes);bin_excess=arb(0)
    def nupper(a,b):
        aa=a.abs_upper();bb=b.abs_upper();return (aa*aa+bb*bb).sqrt().upper()
    def nball(a,b):
        aa=a.abs_lower();bb=b.abs_lower();return (aa*aa+bb*bb).sqrt().lower().union(nupper(a,b))
    def fulljet(Lb):
        key=round(float(Lb.mid())*10)/10
        if key not in cache:
            center=arb(key);shift=arb_poly([center,1]);ap0=ap(shift);bp0=bp(shift)
            cache[key]=(center,ap0,ap0.derivative(),ap0.derivative().derivative(),bp0,bp0.derivative(),bp0.derivative().derivative())
        center,a0,a1,a2,b0p,b1p,b2p=cache[key];v=Lb-center;e=(-da*Lb).exp()
        aa=a0(v);aa1=a1(v);aa2=a2(v);bb=b0p(v)+(e-2)/(pi*Lb)
        bb1=b1p(v)-da*e/(pi*Lb)-(e-2)/(pi*Lb*Lb)
        bb2=b2p(v)+da*da*e/(pi*Lb)+2*da*e/(pi*Lb*Lb)+2*(e-2)/(pi*Lb*Lb*Lb)
        factor=(-beta_base*Lb).exp()
        aa,aa1,aa2=factor*aa,factor*(aa1-beta_base*aa),factor*(aa2-2*beta_base*aa1+beta_base*beta_base*aa)
        bb,bb1,bb2=factor*bb,factor*(bb1-beta_base*bb),factor*(bb2-2*beta_base*bb1+beta_base*beta_base*bb)
        for cc,vv,kk in centres:
            mu=acb(cc-sig,vv);z=-kk/(pi*Lb)*(-mu*Lb).exp();z1=z*(-mu-1/Lb);z2=z*(mu*mu+2*mu/Lb+2/(Lb*Lb))
            aa+=z.real;bb+=z.imag;aa1+=z1.real;bb1+=z1.imag;aa2+=z2.real;bb2+=z2.imag
        return aa,bb,aa1,bb1,aa2,bb2
    def abder(Lb):
        aa,bb,aa1,bb1,aa2,bb2=fulljet(Lb)
        hh=nball(aa,bb)
        if not hh>0:return aa,bb,hh,None,None
        dot=aa*aa1+bb*bb1;hp=dot/hh
        hpp=(aa1*aa1+aa*aa2+bb1*bb1+bb*bb2)/hh-dot*dot/(hh*hh*hh)
        return aa,bb,hh,hp,hpp
    def bin_bound(lo,hi,count,sdelta,sdelta2):
        midpoint=(lo+hi)//2;mid=arb(midpoint);Lm=mid.log();Lb=arb(lo).log().union(arb(hi).log())
        aa,bb,hh,hp,hpp=abder(Lb)
        natural=(count*Lb*(-sig*Lb).exp()*nupper(aa,bb)).upper()
        am,bm,hm,hpm,hppm=abder(Lm)
        if hp is not None and hpm is not None:
            phi=Lm*(-sig*Lm).exp()*hm
            phip=(-(sig+1)*Lm).exp()*(Lm*hpm+(1-sig*Lm)*hm)
            phipp=(-(sig+2)*Lb).exp()*(Lb*hpp+(2-(2*sig+1)*Lb)*hp+(sig*(sig+1)*Lb-(2*sig+1))*hh)
            val=count*phi+phip*sdelta+phipp*arb(sdelta2)/2
            upper=min(natural,val.upper());lower=max(arb(0),val.lower())
        else:upper=natural;lower=arb(0)
        Xb=arb(lo).union(arb(hi))
        logsum=count*Lm+arb(sdelta)/mid-arb(sdelta2)/(2*Xb*Xb)
        return upper,logsum,upper-lower
    for lower in range(direct_limit+1,N+1,chunk_size):
        upper=min(N,lower+chunk_size-1);seg=np.ones(upper-lower+1,dtype=bool)
        for p in base_primes:
            if p*p>upper:break
            first=max(p*p,((lower+p-1)//p)*p)
            seg[first-lower::p]=False
        ps=np.flatnonzero(seg).astype(np.int64)+lower;del seg
        if not len(ps):continue
        ids=np.floor(np.log(ps)/float(binwidth)).astype(np.int64)
        assert np.all(ids[1:]>=ids[:-1]), 'bin partition is not contiguous'
        _,idx,cnt=np.unique(ids,return_index=True,return_counts=True)
        last=idx+cnt-1;midpoint=(ps[idx]+ps[last])//2
        dx=ps-np.repeat(midpoint,cnt)
        assert int(np.max(np.abs(dx)))<=3037000499, 'integer square would overflow'
        sq=dx*dx
        assert int(np.max(sq))*int(np.max(cnt))<2**63, 'integer moments would overflow'
        sd=np.add.reduceat(dx,idx);sd2=np.add.reduceat(sq,idx)
        for i,ni,mm,si,si2 in zip(idx,cnt,midpoint,sd,sd2):
            lo=int(ps[i]);hi=int(ps[i+ni-1]);ni=int(ni)
            assert (lo+hi)//2==int(mm)
            u,psib,excess=bin_bound(lo,hi,ni,int(si),int(si2))
            total+=u;psi+=psib;bin_excess+=excess;bins+=1
        primecount+=len(ps)
        if (upper//chunk_size)%20==0:print('sieved to',upper,'prime count',primecount,'bins',bins,'seconds',time.time()-start,flush=True)
    print('partial',total,'psi',psi,'phase_gain',gain,'phase_boxes',pnodes,'bins',bins,'bin excess',bin_excess,'seconds',time.time()-start,flush=True)
    L0=arb(N).log();Lfar=max(200,int((deg+30)/float(alpha)))
    def inc(k,X,beta):
        return (-beta*X).exp()*sum((arb(math.factorial(k))/math.factorial(i)*X**i/beta**(k-i+1) for i in range(k+1)),arb(0))
    qq=[abs(a)+abs(b) for a,b in zip(pa,pb)]
    while True:
        far=sum((q*inc(i,arb(Lfar),alpha_base) for i,q in enumerate(qq)),arb(0))+2*inc(0,arb(Lfar),alpha_base)
        for cc,vv,kk in centres:
            gamma=cc-1;far+=kk/pi*(-gamma*Lfar).exp()/(gamma*Lfar)
        if far<arb('1e-25'):break
        Lfar+=50
        assert Lfar<10000
    # Analytic integration uses Arb's rigorous adaptive Gauss quadrature.
    integ=acb(0);edges=[L0]+[arb(x) for x in range(math.ceil(float(L0)),Lfar+1,5)]
    if edges[-1]!=Lfar:edges.append(arb(Lfar))
    for l,r in zip(edges,edges[1:]):
        mid=(l+r)/2;shift=arb_poly([mid,1]);as_=acb_poly(ap(shift));bs_=acb_poly(bp(shift))
        def integrand(z,analytic):
            factor=(-acb(beta_base)*z).exp();a=factor*as_(z-mid);b=factor*(bs_(z-mid)+((-acb(da)*z).exp()-2)/(pi*z))
            for cc,vv,kk in centres:
                pref=kk/(pi*z)*(-acb(cc-sig)*z).exp();a-=pref*(vv*z).cos();b+=pref*(vv*z).sin()
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
        r=min(l+dl,Q(Lfar));Lb=box(l,r);aa,bb,aa1,bb1,aa2,bb2=fulljet(Lb);hh=normball(aa,bb)
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
        farerr+=q*sigbase*inc(i,arb(Lfar),alpha_base)
        if i:farerr+=q*i*inc(i-1,arb(Lfar),alpha_base)
    # derivative of (exp(-dL)-2)/L bounded by d*exp(-dL)/L+2/L^2.
    farerr+=(2*sigbase+2)*inc(0,arb(Lfar),alpha_base)+da*inc(0,arb(Lfar),alpha_base+da)
    for cc,vv,kk in centres:
        gamma=cc-1;muabs=((cc-sig)*(cc-sig)+vv*vv).sqrt()
        farerr+=kk/pi*(-gamma*Lfar).exp()/gamma*((sig+muabs)/Lfar+arb(1)/(Lfar*Lfar))
    err+=arb('1.994e-8')*farerr
    correction=(N-psi)*h(L0)*(-sig*L0).exp();tail=I+correction+err-removed
    Cz=total+tail
    result=dict(certified=True,N0=N,P0=P0,Czeta_upper=up_str(Cz,24),partial_upper=up_str(total,24),
                tail_upper=up_str(tail,24),integral_upper=up_str(I,24),far_upper=up_str(far,24),error_upper=up_str(err,24),
                boundary_correction_upper=up_str(correction,24),phase_gain_lower=down_str(gain,24),
                phase_boxes=pnodes,error_boxes=boxes,seconds=time.time()-start,
                bin_log_width=binwidth,bin_count=bins,bin_excess_upper=up_str(bin_excess,24),prime_count=int(primecount),
                step=step,phase_tolerance=tol,precision=ctx.prec,extra_prime_power_cutoff=extra,chunk_size=chunk_size,
                removed_tail_norm_lower=down_str(removed,24),
                input_sha256=sha256(path),code_sha256=CODE_HASH,Lfar=Lfar,centre_mode='joint_prime_phase',sigma_common=str(sigq),
                theorem_source='JRT Lemmas 6,7,8; unconditional, ranges checked in code')
    body=json.dumps(result,indent=2)
    Path(path).with_name(Path(path).stem+f'_arithmetic_coupled_binned_N{N}.json').write_text(body)
    Path(path).with_name(Path(path).stem+f'_arithmetic_coupled_binned_N{N}_P{P0}_{result["code_sha256"][:10]}_step{step}_extra{extra}.json').write_text(body)
    print(json.dumps(result,indent=2),flush=True);return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('path');ap.add_argument('--N',type=int,default=10**8);ap.add_argument('--P0',type=int,default=1000)
    ap.add_argument('--step',default='0.02');ap.add_argument('--binwidth',default='0.0001');ap.add_argument('--extra',type=int,default=10**30);ap.add_argument('--chunk-size',type=int,default=5000000);a=ap.parse_args();certify(a.path,a.N,a.P0,step=a.step,binwidth=a.binwidth,extra=a.extra,chunk_size=a.chunk_size)
