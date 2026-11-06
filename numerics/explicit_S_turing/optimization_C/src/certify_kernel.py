"""Independent Arb boundary certificate for (K), using v11 section 7.1.

H=U-f is harmonic on [-1/2,1/2] x (0,infinity) and its negative
counterpart. H is even in b, H -> 0 uniformly as |t| -> infinity.
On t=0+, H=U(b,0)-pi; on t=0-, H=U(b,0)+pi.
Thus positivity on b=1/2, t != 0 and U(b,0)>=pi imply H>=0 by
the minimum principle on truncated rectangles, then epsilon -> 0.
This is a proof on the entire half-strip, not sampled interior data.
"""
import sys,json,time
from pathlib import Path
from fractions import Fraction as Q
from flint import arb,acb,acb_poly
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'hybrid_asymptotic'))
from certutil import A,box,up_str,down_str,provenance,sha256

def certify(path,T1=100):
    sol=json.loads(Path(path).read_text());d=Q(sol['d']).limit_denominator(10**6)
    B=[tuple(x) for x in sol['B']];c=[A(Q(x)) for x in sol['c']]
    assert d>Q(1,2) and len(B)==len(c) and len(set(B))==len(B) and B[0]==('R',1)
    assert all((k=='R' and j>=1) or (k=='I' and j>=2) for k,j in B)
    assert not sol.get('discs') and T1>=2*d+Q(1,2)
    da=A(d);pi=arb.pi();half=A(Q(1,2));J=max(j for _,j in B)
    rt=[arb(0)]*(J-1);it=[arb(0)]*(J-1)
    for (kind,j),cc in zip(B,c):
        if j>=2:(rt if kind=='R' else it).__setitem__(j-2,cc)
    rtail=acb_poly(rt);itail=acb_poly(it)
    rtailp=rtail.derivative();itailp=itail.derivative()
    stable=sol.get('representation')=='laguerre'
    if stable:
        import math
        rq=[Q(x) for x in sol['parameters']];lamq=2*d-1;check=[Q(0) for _ in B]
        for col,(kind,j) in enumerate(B):
            off=1 if kind=='R' else 2
            for k in range(j-off+1):check[B.index((kind,k+off))]+=rq[col]*math.comb(j-off,k)*(-lamq)**k
        assert check==[Q(x) for x in sol['c']], 'change of basis must be exact'
        rcoeff=[A(x) for x in rq];lam=A(lamq)
        rp=[arb(0)]*J;ip=[arb(0)]*(J-1)
        for (kind,j),cc in zip(B,rcoeff):(rp if kind=='R' else ip).__setitem__(j-1 if kind=='R' else j-2,cc)
        rpoly=acb_poly(rp);ipoly=acb_poly(ip)
        polydata=[('R',1,rpoly,rpoly.derivative(),rpoly.derivative().derivative()),
                  ('I',2,ipoly,ipoly.derivative(),ipoly.derivative().derivative())]
    def proj(k,z):return z.real if k=='R' else -z.imag
    def uder(b,t,axis,order):
        val=arb(0)
        for x,sg in [(da+b,1),(da-b,-1)]:
            inv=1/acb(x,t);pw=[acb(1)]
            for _ in range(6 if stable else J+order):pw.append(pw[-1]*inv)
            if stable:
                w=1-lam*inv
                for k,off,p,p1,p2 in polydata:
                    if order==0:g=pw[off]*p(w)
                    elif order==1:
                        g=-off*pw[off+1]*p(w)+lam*pw[off+2]*p1(w)
                    elif order==2:
                        g=off*(off+1)*pw[off+2]*p(w)-2*lam*(off+1)*pw[off+3]*p1(w)+lam*lam*pw[off+4]*p2(w)
                    else:raise ValueError(order)
                    factor=acb(0,1)**order if axis=='t' else sg**order
                    val+=proj(k,factor*g)
                continue
            for (k,j),cc in zip(B,c):
                mul=1
                for q in range(order):mul*=-(j+q)
                factor=(acb(0,1)**order if axis=='t' else sg**order)*mul
                val+=cc*proj(k,factor*pw[j+order])
        return val
    def f(b,t,sign):
        return sign*pi-2*(t/(da+b)).atan()-2*(t/(da-b)).atan()+(t/(2*da+b)).atan()+(t/(2*da-b)).atan()
    def ft(b,t):
        return sum((-a*y/(y*y+t*t) for a,y in [(2,da+b),(2,da-b),(-1,2*da+b),(-1,2*da-b)]),arb(0))
    def ftt(b,t):
        return sum((2*a*y*t/(y*y+t*t)**2 for a,y in [(2,da+b),(2,da-b),(-1,2*da+b),(-1,2*da-b)]),arb(0))
    def main_bound(lo,hi,sign):
        m=(lo+hi)/2;delta=box(-(hi-lo)/2,(hi-lo)/2);tb=box(lo,hi);tm=A(m)
        H=uder(half,tm,'t',0)-f(half,tm,sign)
        hp=uder(half,tm,'t',1)-ft(half,tm)
        hpp=uder(half,tb,'t',2)-ftt(half,tb)
        return H+hp*delta+hpp*(delta*delta)/2
    def zero_bound(lo,hi):
        m=(lo+hi)/2;delta=box(-(hi-lo)/2,(hi-lo)/2)
        return uder(A(m),arb(0),'b',0)-pi+uder(A(m),arb(0),'b',1)*delta+uder(box(lo,hi),arb(0),'b',2)*(delta*delta)/2
    # Exact boundary expansion of t^2 f through atan degree 17.
    # The next alternating-series remainder is <=sum |alpha| y^19 |u|^17/19.
    ys=[(Q(2),d+Q(1,2)),(Q(2),d-Q(1,2)),(Q(-1),2*d+Q(1,2)),(Q(-1),2*d-Q(1,2))]
    fcoeff=[A(sum((a*y**(2*r+1) for a,y in ys),Q(0))*Q((-1)**r,2*r+1)) for r in range(1,9)]
    frem=A(sum((abs(a)*y**19 for a,y in ys),Q(0))/19)
    def ipow(x,k):
        result=arb(1)
        while k:
            if k&1:result*=x
            k//=2
            if k:x*=x
        return result
    def tail_raw(u):
        v=arb(0)
        for x in [da+half,da-half]:
            inv=1/acb(x*u,1);z=acb(u)*inv
            v+=c[0]*x/(1+x*x*u*u)+(inv*inv*rtail(z)).real-(inv*inv*itail(z)).imag
        polynomial=sum((cc*ipow(u,2*r-1) for r,cc in enumerate(fcoeff,1)),arb(0))
        return v-polynomial-frem*ipow(abs(u),17)
    def tail_derivative(u,sign):
        v=arb(0)
        for x in [da+half,da-half]:
            inv=1/acb(x*u,1);z=acb(u)*inv
            dr=-2*x*inv**3*rtail(z)+acb(0,1)*inv**4*rtailp(z)
            di=-2*x*inv**3*itail(z)+acb(0,1)*inv**4*itailp(z)
            v+=-2*c[0]*x*x*x*u/(1+x*x*u*u)**2+dr.real-di.imag
        v-=sum(((2*r-1)*cc*ipow(u,2*r-2) for r,cc in enumerate(fcoeff,1)),arb(0))
        return v-17*sign*frem*ipow(abs(u),16)
    def tail_bound(lo,hi):
        m=(lo+hi)/2;delta=box(-(hi-lo)/2,(hi-lo)/2)
        return tail_raw(A(m))+tail_derivative(box(lo,hi),-1 if hi<=0 else 1)*delta
    def bisect(fun,lo,hi):
        stack=[(Q(lo),Q(hi),0)];n=0;minlower=None
        while stack:
            l,h,dep=stack.pop();n+=1;v=fun(l,h)
            if v>0:
                z=v.lower();minlower=z if minlower is None or z<minlower else minlower
                continue
            if dep>=65:raise RuntimeError(f'uncertified interval {l} {h}: {v}')
            mid=(l+h)/2;stack.extend([(l,mid,dep+1),(mid,h,dep+1)])
        return dict(boxes=n,positive_lower=down_str(minlower,16))
    print(provenance(path,__file__,ROOT/'hybrid_asymptotic/certutil.py'),flush=True)
    result={}
    for label,fn,lo,hi in [('t_zero',zero_bound,0,Q(1,2)),('positive',lambda a,b:main_bound(a,b,1),0,T1),('negative',lambda a,b:main_bound(a,b,-1),-T1,0),('tail_positive',tail_bound,0,Q(1,T1)),('tail_negative',tail_bound,-Q(1,T1),0)]:
        t=time.time();result[label]=bisect(fn,lo,hi);result[label]['seconds']=time.time()-t
        print(label,result[label],flush=True)
    result.update(certified=True,method='harmonic minimum principle, Arb boundary Taylor intervals and degree-17 atan tail',T1=T1,
                  input_sha256=sha256(path),code_sha256=sha256(__file__),C1_upper=up_str(c[0]/(2*pi),22))
    out=Path(path).with_name(Path(path).stem+'_kernel.json');out.write_text(json.dumps(result,indent=2))
    print('ALL KERNEL BOUNDARIES AND GLOBAL (K) CERTIFIED',flush=True)
    return result
if __name__=='__main__':certify(sys.argv[1],int(sys.argv[2]) if len(sys.argv)>2 else 100)
