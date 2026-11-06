"""Independent Arb proof of the Green-weighted kernel inequality.
Each open cell cut out by circle/rectangle interfaces is harmonic. Certify
all interfaces and the domain boundary, then apply the minimum principle.
On both vertical infinite tails isolate all rational-derivative roots exactly.
No geometry-search evaluations or numerical tolerances are imported.
"""
import sys,json,time,math,hashlib
from pathlib import Path
from fractions import Fraction as Q
from flint import arb,acb,acb_poly,fmpq,fmpq_poly,ctx
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parent/'hybrid_asymptotic'))
from certutil import A,box,up_str,down_str,sha256,provenance

def tail_polynomial(d,b,B,c,m):
    def fq(x):return fmpq(x.numerator,x.denominator) if isinstance(x,Q) else fmpq(x)
    def poly(xs):return fmpq_poly([fq(v) for v in xs])
    def numerator(x):
        D=poly([x*x,0,1]);powers=[fmpq_poly([1])]
        for _ in range(m+1):powers.append(powers[-1]*D)
        P=fmpq_poly([])
        for (kind,j),cc in zip(B,c):
            if not cc:continue
            coeff=[Q(0)]*(j+1)
            for r in range(j+1):
                if kind=='R' and r%2==0:coeff[r]=cc*math.comb(j,r)*x**(j-r)*(-1)**(r//2)
                elif kind=='I' and r%2==1:coeff[r]=cc*math.comb(j,r)*x**(j-r)*(-1)**((r-1)//2)
            P+=poly(coeff)*powers[m-j]
        return D,powers,P
    x1,x2=d+b,d-b;y1,y2=2*d+b,2*d-b;D1,p1,P1=numerator(x1);D2,p2,P2=numerator(x2);D3=poly([y1*y1,0,1]);D4=poly([y2*y2,0,1])
    den=p1[m+1]*p2[m+1]*D3*D4
    num=(P1.derivative()*D1-m*P1*D1.derivative())*p2[m+1]*D3*D4
    num+=(P2.derivative()*D2-m*P2*D2.derivative())*p1[m+1]*D3*D4
    num+=fq(2*x1)*p1[m]*p2[m+1]*D3*D4+fq(2*x2)*p2[m]*p1[m+1]*D3*D4
    num-=fq(y1)*p1[m+1]*p2[m+1]*D4+fq(y2)*p1[m+1]*p2[m+1]*D3
    return (num//num.gcd(den)).numer()

def certify(path):
    start=time.time();s=json.loads(Path(path).read_text());d=Q(s['d']);B=[tuple(x) for x in s['B']];cq=[Q(x) for x in s['c']];pq=[Q(x) for x in s['parameters']];m=s['m'];gs=s['geometries'];kq=[Q(x) for x in s['geometry_weights']]
    assert d>Q(1,2) and len(cq)==len(B)==len(pq) and all(k>=0 for k in kq) and len(kq)==len(gs)
    assert B==[('R',j) for j in range(1,m+1)]+[('I',j) for j in range(2,m+1)]
    check=[Q(0)]*len(B);lamq=2*d-1
    for col,(kind,j) in enumerate(B):
        off=1 if kind=='R' else 2
        for k in range(j-off+1):check[B.index((kind,k+off))]+=pq[col]*math.comb(j-off,k)*(-lamq)**k
    assert check==cq
    ctx.prec=max(512,8*m);pi=arb.pi();da=A(d);lam=A(lamq);kap=[A(k) for k in kq]
    rp=[arb(0)]*m;ip=[arb(0)]*(m-1)
    for (kind,j),p in zip(B,pq):(rp if kind=='R' else ip).__setitem__(j-1 if kind=='R' else j-2,A(p))
    RP=acb_poly(rp);IP=acb_poly(ip);R1=RP.derivative();R2=R1.derivative();I1=IP.derivative();I2=I1.derivative()
    def rational(z,kind,order):
        inv=1/z;w=1-lam*inv;p,p1,p2=(RP,R1,R2) if kind=='R' else (IP,I1,I2);off=1 if kind=='R' else 2
        if order==0:return inv**off*p(w)
        if order==1:return -off*inv**(off+1)*p(w)+lam*inv**(off+2)*p1(w)
        return off*(off+1)*inv**(off+2)*p(w)-2*lam*(off+1)*inv**(off+3)*p1(w)+lam*lam*inv**(off+4)*p2(w)
    def base(w,order):
        z1=da+w;z2=da-w;z3=2*da+w;z4=2*da-w;ii=acb(0,1)
        if order==0:return rational(z1,'R',0)+rational(z2,'R',0)+ii*(rational(z1,'I',0)-rational(z2,'I',0))-2*ii*(z1.log()-z2.log())+ii*(z3.log()-z4.log())
        if order==1:return rational(z1,'R',1)-rational(z2,'R',1)+ii*(rational(z1,'I',1)+rational(z2,'I',1))-2*ii*(1/z1+1/z2)+ii*(1/z3+1/z4)
        return rational(z1,'R',2)+rational(z2,'R',2)+ii*(rational(z1,'I',2)-rational(z2,'I',2))+2*ii*(1/z1**2-1/z2**2)-ii*(1/z3**2-1/z4**2)
    # Independent point identities check the analytic-potential normalization
    # and the derivatives against the original basis, not the stable basis.
    for bq,tq in [(Q(0),Q(1)),(Q(1,5),Q(-3,7)),(Q(1,2),Q(2))]:
        b,t=A(bq),A(tq);w=acb(b,t);U=arb(0);Ut=arb(0);Utt=arb(0)
        for xx in [da+b,da-b]:
            z=acb(xx,t)
            for (kind,j),c0 in zip(B,cq):
                def proj(z):return z.real if kind=='R' else -z.imag
                U+=A(c0)*proj(z**(-j));Ut+=A(c0)*proj(-acb(0,1)*j*z**(-j-1));Utt+=A(c0)*proj(-j*(j+1)*z**(-j-2))
        f=(-pi if tq<0 else pi)-2*(t/(da+b)).atan()-2*(t/(da-b)).atan()+(t/(2*da+b)).atan()+(t/(2*da-b)).atan()
        ft=sum((-a*x/(x*x+t*t) for a,x in [(2,da+b),(2,da-b),(-1,2*da+b),(-1,2*da-b)]),arb(0))
        ftt=sum((2*a*x*t/(x*x+t*t)**2 for a,x in [(2,da+b),(2,da-b),(-1,2*da+b),(-1,2*da-b)]),arb(0))
        assert (base(w,0).real-(-pi if tq<0 else pi)-(U-f)).contains(0)
        assert (-base(w,1).imag-(Ut-ft)).contains(0)
        assert (-base(w,2).real-(Utt-ftt)).contains(0)
    data=[]
    for g in gs:
        q={k:Q(str(v)) for k,v in g.items() if k in ['a','b','c','H','R','v']};v={k:A(x) for k,x in q.items()}
        if g['kind']=='rectangle':
            assert q['a']>=Q(1,2) and q['a']<q['c']<q['b'] and q['c']>1 and q['H']>0
            v['W']=v['b']-v['a'];v['k']=pi/(2*v['H']);v['N']=1
            # Inside a rectangle, both |x-c| and |x+c-2a| are <=2W.
            # Thus D>=2NW. Choose N using exact Arb inequalities; the
            # original per-box exponential tails below remain unchanged.
            rr=(-pi*v['W']/v['H']).exp()
            while True:
                qq=(-v['N']*pi*v['W']/v['H']).exp()
                if qq<arb('.01'):
                    tail=8*qq/((1-rr)*(1-qq*qq))
                    all_orders=tail*(1+v['k']+v['k']**2*(1+qq*qq)/(1-qq*qq))
                    if all_orders<arb('1e-18'):break
                v['N']+=1
                assert v['N']<10000
        else:assert q['c']>1 and q['R']>0 and q['c']-q['R']>=Q(1,2)
        data.append((g['kind'],v))
    def inside(j,w):
        kind,g=data[j];x=w.real+arb(1)/2;y=w.imag+g['v']
        if kind=='circle':return abs(acb(x-g['c'],y))<g['R']
        return x>g['a'] and x<g['b'] and abs(y)<g['H']
    def geom(j,w,order):
        kind,g=data[j];x=w.real+arb(1)/2;y=w.imag+g['v'];z=acb(x-g['c'],y)
        if kind=='circle':
            if order==0:return acb(g['R'].log()-abs(z).log())
            return -1/z if order==1 else 1/z**2
        k=g['k'];W=g['W'];a=g['a'];N=g['N'];M=max(abs(x-g['c']).abs_upper(),abs(x+g['c']-2*a).abs_upper());D=2*(N+1)*W-M;assert D>0
        q=(-k*D).exp();r=(-2*k*W).exp();assert q<arb('0.01')
        if order==0:tail=8*q/((1-r)*(1-q*q))
        elif order==1:tail=8*k*q/((1-r)*(1-q*q))
        else:tail=8*k*k*q*(1+q*q)/((1-r)*(1-q*q)**2)
        value=acb(0)
        for n in range(-N,N+1):
            for sign,dx in [(1,x-g['c']+2*n*W),(-1,x+g['c']-2*a+2*n*W)]:
                if order==0:term=acb(((k*y).cos()/(k*dx).cosh()).atanh())
                else:
                    zz=k*acb(dx,y);sn=zz.sinh()
                    term=-k/sn if order==1 else k*k*zz.cosh()/(sn*sn)
                value+=sign*term
        err=arb(0,1)*tail.abs_upper()
        return value+acb(err,arb(0) if order==0 else err)
    def curve(c,u):
        if c['kind']=='line':
            p=[A(Q(str(v))) for v in c['p']];q=[A(Q(str(v))) for v in c['q']];mid=acb((p[0]+q[0])/2,(p[1]+q[1])/2);slope=acb((q[0]-p[0])/2,(q[1]-p[1])/2)
            return mid+slope*u,slope,acb(0)
        ca=A(Q(str(c['c'])));R=A(Q(str(c['R'])));v=A(Q(str(c['v'])));theta=((ca-1)/R).acos();z=acb(0,-theta*u).exp()
        return acb(ca-arb(1)/2,-v)-R*z,acb(0,1)*R*theta*z,R*theta*theta*z
    def bound(c,lo,hi):
        mid=(lo+hi)/2;ub=box(lo,hi);w,dw,ddw=curve(c,ub);wm,dwm,_=curve(c,A(mid));ids=[j for j,k in enumerate(kq) if k and inside(j,w)]
        v0=base(wm,0).real;v1=base(wm,1);d1=base(w,1);d2=base(w,2)
        for j in ids:
            v0+=kap[j]*geom(j,wm,0).real;v1+=kap[j]*geom(j,wm,1);d1+=kap[j]*geom(j,w,1);d2+=kap[j]*geom(j,w,2)
        sign=-1 if w.imag<0 else 1;v0-=sign*pi;delta=box(-(hi-lo)/2,(hi-lo)/2);sq=box(Q(0),((hi-lo)/2)**2)
        hp=(v1*dwm).real;hpp=(d2*dw*dw+d1*ddw).real
        value=v0+hp*delta+hpp*sq/2
        # Completing the square uses a certified positive lower bound on H''.
        # It is valid on the whole parameter interval, not just at a sample.
        if hpp>0:
            aa=hp.abs_upper();convex=v0-aa*aa/(2*hpp.lower())
            if convex>0:return convex
        derivative=hp+hpp*delta
        if derivative>0 or derivative<0:
            endpoint=lo if derivative>0 else hi;we,_,_=curve(c,A(endpoint));ev=base(we,0).real-sign*pi
            for j in ids:ev+=kap[j]*geom(j,we,0).real
            if ev>0:return ev
        return value
    T=Q(s.get('geometry_boundary_T',6));assert all((Q(str(g['R'])) if g['kind']=='circle' else Q(str(g['H'])))+abs(Q(str(g['v'])))<T for g in gs)
    # Construct proof interfaces in Q, independently of the FLOAT search helper.
    # In particular, 0.7-0.5 must be the exact rational 1/5.
    cc=[dict(kind='line',p=['0',str(-T)],q=['0',str(T)],name='b0'),
        dict(kind='line',p=['1/2',str(-T)],q=['1/2',str(T)],name='bhalf'),
        dict(kind='line',p=['0','0'],q=['1/2','0'],name='t0')]
    for j,g in enumerate(gs):
        if g['kind']=='circle':cc.append(dict(kind='arc',c=str(Q(str(g['c']))),R=str(Q(str(g['R']))),v=str(Q(str(g['v']))),name=f'circle_{j}'))
        else:
            left=Q(str(g['a']))-Q(1,2);v=Q(str(g['v']));H=Q(str(g['H']))
            assert 0<=left<=Q(1,2)
            cc.append(dict(kind='line',p=[str(left),str(-v-H)],q=[str(left),str(-v+H)],name=f'rect_{j}_left'))
            for sign in [-1,1]:cc.append(dict(kind='line',p=[str(left),str(-v+sign*H)],q=['1/2',str(-v+sign*H)],name=f'rect_{j}_{sign}'))
    result=[]
    print(provenance(path,__file__),flush=True)
    for c in cc:
        stack=[(Q(-1),Q(1),0)];count=0;minimum=None;begin=time.time()
        while stack:
            lo,hi,depth=stack.pop();count+=1;v=bound(c,lo,hi)
            if v>0:
                minimum=v.lower() if minimum is None or v.lower()<minimum else minimum;continue
            if depth>=65:raise RuntimeError(('geometric interface unresolved',c['name'],str(lo),str(hi),v))
            mid=(lo+hi)/2;stack.extend([(lo,mid,depth+1),(mid,hi,depth+1)])
        r=dict(curve=c,boxes=count,H_lower=down_str(minimum,24),seconds=time.time()-begin);result.append(r);print('INTERFACE PASS',c['name'],count,'seconds',r['seconds'],flush=True)
    tails=[]
    for b in [Q(0),Q(1,2)]:
        poly=tail_polynomial(d,b,B,cq,m);ctx.prec=256;roots=poly.complex_roots();assert sum(int(k) for _,k in roots)==poly.degree();ctx.prec=max(512,8*m);checked=[]
        for z,mult in roots:
            if not z.imag.contains(0):continue
            t=z.real
            if abs(t)<A(T):continue
            v=base(acb(A(b),t),0).real-(-1 if t<0 else 1)*pi;assert v>0,('negative kernel tail critical point',b,z,v)
            checked.append(dict(t_lower=down_str(t,40),t_upper=up_str(t,40),H_lower=down_str(v,24)))
        tails.append(dict(b=str(b),degree=poly.degree(),root_count=sum(int(k) for _,k in roots),critical_points_outside_geometry=checked,polynomial=[str(v) for v in poly]));print('INFINITE VERTICAL TAIL PASS',b,poly.degree(),len(checked),flush=True)
    out=dict(certified=True,image_tail_target='value and first two derivatives <=1e-18 on complete interior boxes',rectangle_image_counts=[v['N'] for kind,v in data if kind=='rectangle'],method='piecewise harmonic minimum principle on every cell; Arb interface Taylor bounds; exact complete critical-root isolation on both infinite vertical tails',
             input_sha256=sha256(path),code_sha256=sha256(__file__),interface_coordinates='constructed independently in exact rational arithmetic',precision=ctx.prec,interfaces=result,infinite_tails=tails,
             kernel_boundary_T=str(T),infinity_limit_uniform='U-f -> 0 uniformly in b; all Green weights vanish outside a bounded t interval',seconds=time.time()-start)
    Path(path).with_name(Path(path).stem+'_geometry_kernel.json').write_text(json.dumps(out,indent=2));print('GLOBAL GEOMETRIC KERNEL CERTIFIED seconds',out['seconds'],flush=True)
    return out
if __name__=='__main__':certify(sys.argv[1])
