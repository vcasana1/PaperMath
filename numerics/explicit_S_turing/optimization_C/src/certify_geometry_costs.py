"""Rigorous harmonic boundary costs J,G,A for selected circles/rectangles.
The logarithmic Euler singularity at sigma=1 is removed before quadrature;
an explicitly bounded omitted sliver remains. No numerical DST is used.
"""
import sys,json,time,math,argparse
from pathlib import Path
from fractions import Fraction as Q
from flint import arb,acb,acb_series,ctx
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parent/'hybrid_asymptotic'))
from certutil import A,up_str,down_str,sha256,provenance
X=[Q(1,2)]+[1-Q(k,2**k-2) for k in range(4,10)]+[Q(1)]
E=[Q(1,6)]+[Q(1,2**k-2) for k in range(4,10)]+[Q(0)]

def certify(path,PL=None):
    start=time.time();s=json.loads(Path(path).read_text());ctx.prec=512;pi=arb.pi();AA=[arb('.618').log()]+[arb('1.546').log()]*6+[arb(0)];delta=Q(1,2**48)
    pl=Path(PL) if PL else BASE/'certificates/geometry_PL_inputs.json';assert json.loads(pl.read_text())['certified']
    def val(x,kind):
        xq=x if isinstance(x,Q) else Q(x)
        if xq>1:return arb(0) if kind!='A' else A(xq).zeta().log()
        if kind=='G':return arb(1)
        ys=[A(e) for e in E] if kind=='J' else AA
        for i in range(len(X)-1):
            if X[i]<=xq<=X[i+1]:return ys[i]+(ys[i+1]-ys[i])*A((xq-X[i])/(X[i+1]-X[i]))
        raise ValueError(xq)
    def linpieces(a,b,kind):
        cuts=sorted(set([a,min(b,Q(1))]+[x for x in X if a<x<min(b,Q(1))]));out=[]
        for lo,hi in zip(cuts,cuts[1:]):
            if lo>=hi:continue
            yl,yh=val(lo,kind),val(hi,kind);beta=(yh-yl)/A(hi-lo);alpha=yl-beta*A(lo);out.append((lo,hi,alpha,beta))
        return out
    def integral(fun,lo,hi):
        # Bounded analytic integrands on a finite log coordinate interval.
        lo,hi=A(lo) if isinstance(lo,Q) else lo,A(hi) if isinstance(hi,Q) else hi
        steps=max(1,math.ceil(float(hi-lo)/2));total=acb(0)
        for j in range(steps):
            left=lo+(hi-lo)*j/steps;right=lo+(hi-lo)*(j+1)/steps
            z=acb.integral(fun,acb(left),acb(right),abs_tol=arb('1e-24'),rel_tol=arb('1e-22'),eval_limit=20000);assert z.is_finite() and z.imag.contains(0),('harmonic integral unresolved',j,z)
            total+=z
        return total.real
    def log_euler_u(u,analytic):
        z=u.exp();sg=1+z;whole=1+z*acb_series([sg],prec=1).zeta(deflate=True)[0]
        return whole.log(analytic=analytic)-u
    rows=[]
    for gi,g in enumerate(s['geometries']):
        q={k:Q(str(v)) for k,v in g.items() if k in ['a','b','c','H','R','v']};c=q['c'];center=A(c).zeta().log()-A(2*c).zeta().log()
        assert c>1
        extent=q['H'] if g['kind']=='rectangle' else q['R'];right=q['b'] if g['kind']=='rectangle' else c+q['R']
        assert extent+abs(q['v'])<=10 and right+3<=10
        if g['kind']=='rectangle':
            a,b,H=q['a'],q['b'],q['H'];W=A(b-a);ha={t:val(a,t) for t in ['J','G','A']};hb={t:val(b,t) for t in ['J','G','A']};qq=pi*A(H)/W
            N=max(16,math.ceil(50/float(qq)));tail=4/W*(-(N+1)*qq).exp()/(1-(-qq).exp());assert tail<arb('1e-16')
            kn=[n*pi/W for n in range(1,N+1)];co=[2/W*(k*A(c-a)).sin()/(k*A(H)).cosh() for k in kn]
            def sint(lo,hi,alpha,beta,k):
                def F(x):
                    xx=A(x);return -(alpha+beta*xx)*(k*(xx-A(a))).cos()/k+beta*(k*(xx-A(a))).sin()/(k*k)
                return F(hi)-F(lo)
            def P(z):return sum((acb(v)*(k*(z-A(a))).sin() for k,v in zip(kn,co)),acb(0))
            values={}
            for typ in ['J','G','A']:
                beta=(hb[typ]-ha[typ])/W;alpha=ha[typ]-beta*A(a);v=alpha+beta*A(c)
                for k,coef in zip(kn,co):
                    v-=coef*sint(a,b,alpha,beta,k)
                    for lo,hi,al,be in linpieces(a,b,typ):v+=coef*sint(lo,hi,al,be,k)
                if typ=='A':
                    def fun(u,analytic):
                        e=u.exp();return log_euler_u(u,analytic)*P(1+e)*e
                    v+=integral(fun,A(delta).log(),A(b-1).log())
                    pmax=sum((abs(v) for v in co),arb(0));v+=pmax*A(delta)*(A(b).log()-A(delta).log()+1)
                    absolute_integral=W*max(abs(AA[0]).abs_upper(),abs(AA[1]).abs_upper())+A(b)*A(b).log()-A(b-1)*A(b-1).log()
                elif typ=='G':absolute_integral=W
                else:absolute_integral=W*A(Q(1,6))
                err=tail*(absolute_integral+W*max(abs(ha[typ]).abs_upper(),abs(hb[typ]).abs_upper()))
                values[typ]=v+err
            values['A']+=center
            detail=dict(method='exact sine integrals for linear profiles; Arb Euler integral; rigorous geometric Fourier tail',Fourier_terms=N,Poisson_tail_upper=up_str(tail,24))
        else:
            R=q['R'];left=c-R;theta1=((1-A(c))/A(R)).acos();assert theta1-A(delta)>pi/2;values={}
            for typ in ['J','G','A']:
                v=arb(0)
                for lo,hi,alpha,beta in linpieces(left,Q(1),typ):
                    tl=((A(hi)-A(c))/A(R)).acos();tr=((A(lo)-A(c))/A(R)).acos()
                    v+=(alpha+beta*A(c))*(tr-tl)+beta*A(R)*(tr.sin()-tl.sin())
                if typ=='A':
                    # theta=theta1-exp(u), away from the integrable endpoint.
                    def fun(u,analytic):
                        e=u.exp();theta=acb(theta1)-e;sg=A(c)+A(R)*theta.cos();whole=1+(sg-1)*acb_series([sg],prec=1).zeta(deflate=True)[0]
                        return (whole.log(analytic=analytic)-(sg-1).log(analytic=analytic))*e
                    v+=integral(fun,A(delta).log(),theta1.log())
                    v+=A(delta)*((A(c+R)/(A(R)*theta1.sin())).log()-A(delta).log()+1)
                values[typ]=v/pi
            values['A']+=center
            detail=dict(method='exact circle integrals for linear profiles; Arb log-coordinate Euler integral; explicit endpoint sliver')
        assert values['J']>0 and values['G']>0
        row=dict(geometry={k:v for k,v in g.items() if k!='cost'},J_upper=up_str(values['J'],25),G_upper=up_str(values['G'],25),A_upper=up_str(values['A'],25),**detail)
        rows.append(row);print('HARMONIC COST CERTIFIED',gi,row['J_upper'],row['G_upper'],row['A_upper'],'seconds',time.time()-start,flush=True)
    result=dict(certified=True,input_sha256=sha256(path),code_sha256=sha256(__file__),PL_certificate_sha256=sha256(pl),precision=ctx.prec,endpoint_sliver=str(delta),geometries=rows,
        height_domain='harmonic coefficients independent of T; explicit height correction valid for log T>=10, |v|+extent<=10 and Q+maximum real boundary coordinate<=10',
        explicit_height_correction_per_weight='G*pi^2/(8*(log T)^2)+400/T',seconds=time.time()-start)
    Path(path).with_name(Path(path).stem+'_geometry_costs.json').write_text(json.dumps(result,indent=2));print('ALL HARMONIC COSTS CERTIFIED',flush=True)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('candidate');ap.add_argument('--PL');a=ap.parse_args();certify(a.candidate,a.PL)
