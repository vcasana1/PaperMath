"""Certified slacks at the final kernel; no claim of optimality."""
import sys,json
from pathlib import Path
from fractions import Fraction as Q
from flint import arb,ctx
ROOT=Path(__file__).resolve().parents[2];BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'hybrid_asymptotic'));from certutil import A,up_str,down_str,sha256
final=json.loads((BASE/'certificates/FINAL_RESULT.json').read_text());p=BASE/final['solution'];s=json.loads(p.read_text())
ctx.prec=max(256,8*s['m']);c=[A(Q(x)) for x in s['c']];B=[tuple(x) for x in s['B']];d=A(Q(s['d']));pi=arb.pi()
C1=c[0]/(2*pi);slack=arb('0.08382')-C1;limit=2*d*c[0]-2*c[B.index(('R',2))]
k=json.loads((BASE/final['kernel_certificate']).read_text());points=[]
for r in k.get('critical_real_candidates',[]):
    t=arb(r['t_lower']).union(arb(r['t_upper']));H=arb(r['H_lower']).union(arb(r['H_upper']));scaled=H*(1+t*t)
    points.append(dict(t_lower=r['t_lower'],t_upper=r['t_upper'],scaled_slack_lower=down_str(scaled,24),scaled_slack_upper=up_str(scaled,24)))
points.sort(key=lambda r:float(r['scaled_slack_upper']))
zero=[]
for b in [arb(0),arb(1)/2]:
    U=sum((cc*((d+b)**(-j)+(d-b)**(-j)) for (kind,j),cc in zip(B,c) if kind=='R'),arb(0))-pi
    zero.append(dict(b=up_str(b,4),slack_lower=down_str(U,24),slack_upper=up_str(U,24)))
result=dict(input_sha256=sha256(p),leading_slope_lower=down_str(C1,24),leading_slope_upper=up_str(C1,24),
            slope_cap_slack_lower=down_str(slack,24),slope_cap_slack_upper=up_str(slack,24),
            tail_limit_lower=down_str(limit,24),tail_limit_upper=up_str(limit,24),
            zero_boundary_point_slacks=zero,closest_critical_constraints=points[:20],
            numerical_Lpeak=s.get('Lpeak_est'),interpretation='Certified slacks and numerical dual-height diagnostic; not an optimality certificate')
(BASE/'certificates/active_constraints.json').write_text(json.dumps(result,indent=2));print('active-constraint slacks saved')
