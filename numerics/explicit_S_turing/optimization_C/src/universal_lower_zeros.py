"""Improve the universal necessary lower bound by searching 20000 true zeros.
Only one rational nonordinate and its certified N(T) enter the final proof.
"""
import sys,json,time
from pathlib import Path
from fractions import Fraction as Q
from flint import arb,acb,ctx
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'hybrid_asymptotic'))
from certutil import A,exact,down_str,up_str,sha256
start=time.time();ctx.prec=64;pi=arb.pi();top=[]
for first in range(1,20001,1000):
    zeros=acb.zeta_zeros(first,1000)
    for index,z in enumerate(zeros,first):
        T=z.imag;theta=acb(arb(1)/4,T/2).lgamma().imag-T*pi.log()/2
        for n in [index-1,index]:
            v=abs(n-1-theta/pi)-arb('.08382')*T.log();score=float(v)
            if len(top)<10 or score>top[-1][0]:top.append((score,index,n));top.sort(reverse=True);top=top[:10]
    print('zeros searched',first+999,'best',top[0],'seconds',time.time()-start,flush=True)
ctx.prec=256;pi=arb.pi();best=None
for _,index,n in top:
    z=acb.zeta_zero(index).imag
    endpoint=exact(z.lower())-Q(1,10**40) if n==index-1 else exact(z.upper())+Q(1,10**40)
    T=A(endpoint);N=T.zeta_nzeros();assert N.is_exact() and exact(N)==n
    theta=acb(arb(1)/4,T/2).lgamma().imag-T*pi.log()/2;S=N-1-theta/pi;v=abs(S)-arb('.08382')*T.log()
    if best is None or v.lower()>best[0].lower():best=(v,endpoint,N,S,index)
v,t,N,S,index=best
result=dict(certified=True,C_lower=down_str(v,24),T_rational=str(t),T_decimal=up_str(A(t),24),N=str(int(exact(N))),
            S_lower=down_str(S,24),S_upper=up_str(S,24),zero_index=index,
            scope='necessary lower bound for any uniform S(T) inequality, including arbitrary kernel envelopes',
            method='Arb certified zeta_nzeros and lgamma at a rational nonordinate',search_range='first 20000 zeros',
            seconds=time.time()-start,code_sha256=sha256(__file__))
Path('certificates/universal_lower_zeros.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2),flush=True)
