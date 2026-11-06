"""Check the implemented weight derivatives against independent Arb series AD.
Extract ONLY the trusted fulljet function from the delivered verifier; do not
run its prime summation. Series AD also checks the x-space bin curvature.
"""
import sys,json,ast,math,hashlib
from pathlib import Path
from fractions import Fraction as Q
from flint import arb,acb,arb_poly,acb_series,ctx
BASE=Path(__file__).resolve().parents[1];ctx.prec=512
source=Path(sys.argv[2]) if len(sys.argv)>2 else BASE/'src/certify_arithmetic_coupled.py';tree=ast.parse(source.read_text());outer=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='certify');jet=next(n for n in outer.body if isinstance(n,ast.FunctionDef) and n.name=='fulljet')
s=json.loads(Path(sys.argv[1]).read_text());d=Q(s['d']);B=[tuple(x) for x in s['B']];pi=arb.pi()
def A(q):return arb(q.numerator)/q.denominator if isinstance(q,Q) else arb(q)
pa=[arb(0)]*s['m'];pb=pa.copy()
for (kind,j),v in zip(B,s['c']):(pa if kind=='R' else pb).__setitem__(j-1,-A(Q(v))/math.factorial(j-1)/pi)
cq=[(Q(str(g['c'])),Q(str(g['v'])),Q(k)) for g,k in zip(s['geometries'],s['geometry_weights'])];sigq=min([d+Q(1,2)]+[c for c,v,k in cq]);sig=A(sigq);sigbase=A(d+Q(1,2));beta=sigbase-sig;centres=[tuple(A(v) for v in row) for row in cq]
env=dict(arb=arb,acb=acb,arb_poly=arb_poly,ap=arb_poly(pa),bp=arb_poly(pb),da=A(d),pi=pi,beta_base=beta,sig=sig,centres=centres,cache={})
exec(compile(ast.Module(body=[jet],type_ignores=[]),str(source),'exec'),env)
def original_series(S):
    def poly(coeff):
        out=acb_series([0],prec=3)
        for c in reversed(coeff):out=out*S+c
        return out
    a=(-beta*S).exp()*poly(pa);b=(-beta*S).exp()*(poly(pb)+((-A(d)*S).exp()-2)/(pi*S))
    for c,v,k in centres:
        p=k/(pi*S)*(-(c-sig)*S).exp();a-=p*(v*S).cos();b+=p*(v*S).sin()
    return a,b
rows=[]
for x in [2,1009,10**8]:
    L=arb(x).log();j=env['fulljet'](L);S=acb_series([acb(L),1],prec=3);aa,bb=original_series(S)
    expected=[aa[0].real,bb[0].real,aa[1].real,bb[1].real,2*aa[2].real,2*bb[2].real]
    assert all((u-v).contains(0) for u,v in zip(j,expected)),('coupled derivative identity',x,j,expected)
    X=acb_series([x,1],prec=3);LS=X.log();aa,bb=original_series(LS);phi=LS*(-sig*LS).exp()*(aa*aa+bb*bb).sqrt();automatic=2*phi[2].real
    a,b,ap,bp,app,bpp=j;h=(a*a+b*b).sqrt();hp=(a*ap+b*bp)/h;hpp=(ap*ap+a*app+bp*bp+b*bpp)/h-(a*ap+b*bp)**2/h**3
    explicit=(-(sig+2)*L).exp()*(L*hpp+(2-(2*sig+1)*L)*hp+(sig*(sig+1)*L-(2*sig+1))*h)
    assert (automatic-explicit).contains(0),('x curvature identity',x,automatic,explicit)
    rows.append(dict(x=x,weight_derivatives_pass=True,x_curvature_pass=True))
r=dict(passed=True,method='independent automatic differentiation with Arb power series',precision=ctx.prec,verifier_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),candidate=sys.argv[1],checks=rows)
(BASE/'certificates/coupled_weight_validation.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
