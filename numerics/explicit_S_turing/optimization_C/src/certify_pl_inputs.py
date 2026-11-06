"""Certify compact parts of the vertical-line inputs. No zero hypothesis.
The pole at 1 is removed with FLINT's deflated zeta, without an assumed
Stieltjes-constant error. Published estimates supply |t|>=3, except that
the elementary 1-line bound log(t) is verified here through t=50.
"""
import json,time,hashlib,sys
from pathlib import Path
from fractions import Fraction as Q
from flint import arb,acb,acb_series,ctx
BASE=Path(__file__).resolve().parents[1];ctx.prec=192;start=time.time()
lines=[(Q(1,2),Q(1,6),'0.618')]+[(1-Q(k,2**k-2),Q(1,2**k-2),'1.546') for k in range(4,10)]+[(Q(1),Q(0),'1')]
def aq(q):return arb(q.numerator)/q.denominator
rows=[]
for sigma,alpha,A in lines:
    worst=arb(0)
    for i in range(1500):
        tb=(arb(i)/500).union(arb(i+1)/500);s=acb(aq(sigma),tb)
        if sigma==1:whole=1+(s-1)*acb_series([s],prec=1).zeta(deflate=True)[0]
        else:whole=(s-1)*s.zeta()
        z=abs(acb(3+aq(sigma),tb));ratio=abs(whole)/(arb(A)*z**(1+aq(alpha))*z.log())
        assert ratio<1,(sigma,i,ratio)
        worst=max(worst,ratio.upper())
    rows.append(dict(sigma=str(sigma),alpha=str(alpha),A=A,ratio_upper=str(worst),boxes=1500))
    print('WHOLE LINE COMPACT PART PASS',sigma,worst,flush=True)
worst=arb(0)
for i in range(4700):
    tb=(arb(3)+arb(i)/100).union(arb(3)+arb(i+1)/100)
    ratio=abs(acb(1,tb).zeta())/tb.log();assert ratio<1,(i,ratio);worst=max(worst,ratio.upper())
result=dict(certified=True,precision=ctx.prec,compact_PL_inputs=rows,one_line_3_to_50_ratio_upper=str(worst),one_line_boxes=4700,
            code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            one_line_from_50='Backlund bound |zeta(1+it)| <= log(t), as stated in Trudgian arXiv:1210.6743; independent compact check bridges [3,50]',
            sources=['https://arxiv.org/html/2207.02366v1','https://arxiv.org/html/2301.03165v2','https://arxiv.org/abs/1210.6743'],seconds=time.time()-start)
(Path(sys.argv[1]) if len(sys.argv)>1 else BASE/'certificates/geometry_PL_inputs.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2),flush=True)
