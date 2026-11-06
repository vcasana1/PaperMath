"""Necessary lower bound for ANY uniform S(T) inequality, including envelopes.
The search is numerical. Only the final rational point with Arb's certified
N(T) and theta(T) provides the lower bound; no global RH is assumed.
"""
import sys,json,time
from pathlib import Path
from fractions import Fraction as Q
from flint import arb,acb,ctx
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'hybrid_asymptotic'))
from certutil import A,exact,down_str,up_str,provenance,sha256
start=time.time();ctx.prec=53;pi=arb.pi();candidates=[]
for t in range(1,20001):
    T=arb(t);N=T.zeta_nzeros()
    if not N.is_exact():continue
    H=acb(arb(1)/4,T/2).lgamma().imag/pi-T*pi.log()/(2*pi)+1
    S=N-H;v=float(abs(S)-arb('.08382')*T.log())
    if len(candidates)<20 or v>candidates[-1][0]:
        candidates.append((v,t,int(exact(N)),float(S)));candidates.sort(reverse=True);candidates=candidates[:20]
    if t%2000==0:print('T scanned',t,'best',candidates[0],'seconds',time.time()-start,flush=True)
ctx.prec=256;pi=arb.pi();best=None
for _,t,n,s in candidates:
    index=n if s>0 else n+1
    if index<1:continue
    z=acb.zeta_zero(index).imag
    for endpoint in [exact(z.lower())-Q(1,10**40),exact(z.upper())+Q(1,10**40)]:
        T=A(endpoint);N=T.zeta_nzeros()
        if not N.is_exact():continue
        theta=acb(arb(1)/4,T/2).lgamma().imag-T*pi.log()/2;S=N-1-theta/pi
        v=abs(S)-arb('.08382')*T.log()
        if best is None or v.lower()>best[0].lower():best=(v,endpoint,N,S,index)
v,t,N,S,index=best
result=dict(certified=True,C_lower=down_str(v,24),T_rational=str(t),T_decimal=up_str(A(t),24),N=str(int(exact(N))),
            S_lower=down_str(S,24),S_upper=up_str(S,24),zero_index=index,
            scope='necessary lower bound for any bound |S(T)|<=.08382 log(T)+C for all T>1, including any kernel envelope',
            method='Arb certified zeta_nzeros and lgamma at a rational nonordinate',
            search_range='integer heights 1..20000; refine only top 20 candidates; not a global maximum claim',
            seconds=time.time()-start,code_sha256=sha256(__file__))
Path('certificates/universal_lower.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2),flush=True)
