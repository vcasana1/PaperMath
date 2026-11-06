"""Independent global (K) certificate by exact critical-point isolation.

At b=1/2 the derivative of U-f is rational N(t)/D(t), D(t)>0 on R.
Build N exactly over Q, isolate ALL its roots with FLINT, and evaluate U-f
on every possible real critical root. Together with U(b,0)>pi and the
uniform limit U-f -> 0 at infinity, this proves the entire boundary.
The harmonic minimum principle then proves (K) on the whole strip.

Root-isolation contract: python-flint fmpz_poly.complex_roots;
https://flintlib.org/doc/arb_fmpz_poly.html . No approximate root list is used.
"""
import sys,json,time,math
from pathlib import Path
from fractions import Fraction as Q
from flint import fmpq,fmpq_poly,arb,acb,acb_poly,ctx
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'hybrid_asymptotic'))
from certutil import A,box,up_str,down_str,provenance,sha256

def verify(path):
    start=time.time();sol=json.loads(Path(path).read_text());d=Q(sol['d']).limit_denominator(10**6)
    B=[tuple(x) for x in sol['B']];cq=[Q(x) for x in sol['c']];m=max(j for _,j in B)
    assert d>Q(1,2) and len(B)==len(cq) and len(set(B))==len(B) and B[0]==('R',1)
    assert not sol.get('discs') and all((k=='R' and j>=1) or (k=='I' and j>=2) for k,j in B)
    def fq(x):return fmpq(x.numerator,x.denominator) if isinstance(x,Q) else fmpq(x)
    def polynomial(values):return fmpq_poly([fq(v) for v in values])
    x1=d+Q(1,2);x2=d-Q(1,2);y3=2*d+Q(1,2);y4=2*d-Q(1,2)
    def rational_numerator(x):
        D=polynomial([x*x,0,1]);powers=[fmpq_poly([1])]
        for _ in range(m+1):powers.append(powers[-1]*D)
        P=fmpq_poly([])
        for (kind,j),c in zip(B,cq):
            coeff=[Q(0)]*(j+1)
            for r in range(j+1):
                if kind=='R' and r%2==0:coeff[r]=c*math.comb(j,r)*x**(j-r)*(-1)**(r//2)
                elif kind=='I' and r%2==1:coeff[r]=c*math.comb(j,r)*x**(j-r)*(-1)**((r-1)//2)
            P+=polynomial(coeff)*powers[m-j]
        return D,powers,P
    D1,p1,P1=rational_numerator(x1);D2,p2,P2=rational_numerator(x2)
    D3=polynomial([y3*y3,0,1]);D4=polynomial([y4*y4,0,1])
    denominator=p1[m+1]*p2[m+1]*D3*D4
    numerator=(P1.derivative()*D1-m*P1*D1.derivative())*p2[m+1]*D3*D4
    numerator+=(P2.derivative()*D2-m*P2*D2.derivative())*p1[m+1]*D3*D4
    numerator+=fq(2*x1)*p1[m]*p2[m+1]*D3*D4+fq(2*x2)*p2[m]*p1[m+1]*D3*D4
    numerator-=fq(y3)*p1[m+1]*p2[m+1]*D4+fq(y4)*p1[m+1]*p2[m+1]*D3
    # Independent exact derivative identity checks catch indexing/sign mistakes.
    def cmul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
    def cpow(a,k):
        v=(Q(1),Q(0))
        for _ in range(k):v=cmul(v,a)
        return v
    for t in map(Q,['0','1/7','1','-1','13/7']):
        derivative=Q(0)
        for x in [x1,x2]:
            inv=(x/(x*x+t*t),-t/(x*x+t*t))
            for (kind,j),c in zip(B,cq):
                w=cpow(inv,j+1);v=(j*w[1],-j*w[0])
                derivative+=c*(v[0] if kind=='R' else -v[1])
        derivative+=2*x1/(x1*x1+t*t)+2*x2/(x2*x2+t*t)-y3/(y3*y3+t*t)-y4/(y4*y4+t*t)
        assert numerator(fq(t))/denominator(fq(t))==fq(derivative)
    common=numerator.gcd(denominator);numerator=numerator//common
    integer_poly=numerator.numer()
    print(provenance(path,__file__,ROOT/'hybrid_asymptotic/certutil.py'),flush=True)
    print('exact derivative numerator degree',integer_poly.degree(),'built in',time.time()-start,flush=True)
    ctx.prec=256;roots=integer_poly.complex_roots()
    assert sum(int(mult) for _,mult in roots)==integer_poly.degree()
    print('all polynomial roots isolated',len(roots),'elapsed',time.time()-start,flush=True)
    ctx.prec=max(256,8*m);ca=[A(c) for c in cq];da=A(d);pi=arb.pi();lam=2*da-1
    stable=sol.get('representation')=='laguerre'
    if stable:
        rq=[Q(x) for x in sol['parameters']];check=[Q(0)]*len(B)
        for col,(kind,j) in enumerate(B):
            off=1 if kind=='R' else 2
            for k in range(j-off+1):check[B.index((kind,k+off))]+=rq[col]*math.comb(j-off,k)*(-(2*d-1))**k
        assert check==cq
        rp=[arb(0)]*m;ip=[arb(0)]*(m-1)
        for (kind,j),v in zip(B,rq):(rp if kind=='R' else ip).__setitem__(j-1 if kind=='R' else j-2,A(v))
        RP=acb_poly(rp);IP=acb_poly(ip);RP1=RP.derivative();RP2=RP1.derivative()
        def U(b,t):
            return sum(((RP(1-lam/z)/z).real-(IP(1-lam/z)/(z*z)).imag for z in [acb(da+b,t),acb(da-b,t)]),arb(0))
        def zero_der(b,order):
            value=arb(0)
            for x,sg in [(da+b,1),(da-b,-1)]:
                inv=1/acb(x);w=1-lam*inv
                if order==0:g=inv*RP(w)
                elif order==1:g=-inv**2*RP(w)+lam*inv**3*RP1(w)
                else:g=2*inv**3*RP(w)-4*lam*inv**4*RP1(w)+lam*lam*inv**5*RP2(w)
                value+=sg**order*g.real
            return value
    else:
        def U(b,t):
            value=arb(0)
            for x in [da+b,da-b]:
                inv=1/acb(x,t)
                for (kind,j),c in zip(B,ca):
                    z=inv**j;value+=c*(z.real if kind=='R' else -z.imag)
            return value
        def zero_der(b,order):
            return sum((c*((-1)**order*math.prod(range(j,j+order)) if order else 1)*
                        ((da+b)**(-j-order)+(-1)**order*(da-b)**(-j-order))
                        for (kind,j),c in zip(B,ca) if kind=='R'),arb(0))
    def f(t,sign):return sign*pi-2*(t/A(x1)).atan()-2*(t/A(x2)).atan()+(t/A(y3)).atan()+(t/A(y4)).atan()
    # Entire t=0 boundary, not only the endpoint b=1/2.
    stack=[(Q(0),Q(1,2),0)];boxes=0;minimum=None
    while stack:
        lo,hi,depth=stack.pop();boxes+=1;mid=(lo+hi)/2;delta=box(-(hi-lo)/2,(hi-lo)/2)
        value=zero_der(A(mid),0)-pi+zero_der(A(mid),1)*delta+zero_der(box(lo,hi),2)*(delta*delta)/2
        if value>0:
            minimum=value.lower() if minimum is None or value.lower()<minimum else minimum;continue
        if depth>=65:raise RuntimeError('zero boundary unresolved')
        stack.extend([(lo,mid,depth+1),(mid,hi,depth+1)])
    critical=[]
    for z,mult in roots:
        if not z.imag.contains(0):continue
        t=z.real;signs=[1] if t>0 else [-1] if t<0 else [1,-1]
        for sign in signs:
            value=U(arb(1)/2,t)-f(t,sign)
            assert value>0,('critical point not positive',z,value)
            critical.append(dict(t_lower=down_str(t,50),t_upper=up_str(t,50),multiplicity=int(mult),sign=sign,H_lower=down_str(value,30),H_upper=up_str(value,30)))
    limit=2*da*ca[0]-2*ca[B.index(('R',2))];assert limit>0
    polynomial_data=dict(coefficients=[str(v) for v in integer_poly],degree=integer_poly.degree())
    pfile=Path(path).with_name(Path(path).stem+'_critical_polynomial.json');pfile.write_text(json.dumps(polynomial_data))
    result=dict(certified=True,kernel_method='critical_polynomial',T1=None,
                method='exact rational derivative; complete certified polynomial-root isolation; harmonic minimum principle',
                input_sha256=sha256(path),code_sha256=sha256(__file__),polynomial_sha256=sha256(pfile),
                degree=integer_poly.degree(),root_count_with_multiplicity=sum(int(v) for _,v in roots),
                root_precision=256,evaluation_precision=ctx.prec,
                critical_real_candidates=critical,zero_boundary_boxes=boxes,zero_boundary_lower=down_str(minimum,30),
                infinity_limit_t2H_lower=down_str(limit,30),C1_upper=up_str(ca[0]/(2*pi),24),seconds=time.time()-start)
    Path(path).with_name(Path(path).stem+'_kernel.json').write_text(json.dumps(result,indent=2))
    print('GLOBAL (K) CERTIFIED BY ALL CRITICAL POINTS',len(critical),'seconds',time.time()-start,flush=True)
    return result
if __name__=='__main__':verify(sys.argv[1])
