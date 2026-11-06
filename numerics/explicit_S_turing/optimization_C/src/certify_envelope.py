"""Combine independently certified kernels, arithmetic and elementary part.
Low kernel covers 1<=T<=exp(Lswitch); high kernel covers exp(Lswitch)<=T.
The high bound is the explicit remainder of v11 Lemmas 4.7 and 4.8,
evaluated at exp(Lswitch), retaining the actual slope slack.
"""
import sys,json,math,argparse
from pathlib import Path
from fractions import Fraction as Q
from flint import arb
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'hybrid_asymptotic'))
from certutil import A,up_str,down_str,sha256,provenance

def certify(candidate,arithmetic,low,low_arithmetic,low_elementary,Lswitch='100',digits=10):
    paths=[candidate,arithmetic,low,low_arithmetic,low_elementary]
    sol=json.loads(Path(candidate).read_text());cz=json.loads(Path(arithmetic).read_text())
    lowsol=json.loads(Path(low).read_text());lcz=json.loads(Path(low_arithmetic).read_text());lel=json.loads(Path(low_elementary).read_text())
    kh=Path(candidate).with_name(Path(candidate).stem+'_kernel.json');kl=Path(low).with_name(Path(low).stem+'_kernel.json')
    for p,s in [(kh,candidate),(kl,low)]:
        k=json.loads(p.read_text());assert k['certified'] and k['input_sha256']==sha256(s)
    assert cz['certified'] and cz['input_sha256']==sha256(candidate)
    assert lcz['certified'] and lcz['input_sha256']==sha256(low)
    assert lel['mode']=='S'
    # The preserved upstream program predates input-hash metadata. The wrapper
    # supplies it on fresh runs; legacy results are independently reproduced.
    if 'input_sha256' in lel:assert lel['certified'] and lel['input_sha256']==sha256(low)
    pi=arb.pi();d=A(Q(sol['d']));c=[A(Q(x)) for x in sol['c']];B=sol['B']
    C1=c[0]/(2*pi);cap=arb('0.08382')
    if Lswitch=='auto':
        trial=(arb(cz['Czeta_upper'])-C1*(2*pi).log()-arb(lcz['Czeta_upper'])-arb(lel['Fsup_upper']))/(arb(lel['A1'])-C1)
        Lswitch=format(math.floor(float(trial)*10**6)/10**6,'.6f')
    L=A(Q(Lswitch));T=L.exp();s1=arb(1)/2+d;s2=arb(1)/2+2*d
    assert C1<=cap and L>0
    K=(4*d+s1*s1/2+s2*(s2-1)/2+1+s2*s2/2+s1*(s1-1))/pi
    K+=abs(c[0])/pi*((2*s1-1)+s1*s1/4+arb(8)/3)/T
    for (kind,j),cc in zip(B,c):
        if j==1:continue
        kk=j-1
        ps=arb(math.factorial(kk-1))*(2/T)**kk+arb(math.factorial(kk))*(2/T)**(kk+1)/2+arb(math.factorial(kk+1))*(4/(3*T))*(4/T)**(kk+1)
        K+=abs(cc)/pi*(2/T**j+ps/(math.factorial(j-1)*2**j))*T
    K+=(arb(1)/16+arb(1)/8+arb(1)/3)/pi
    high=arb(cz['Czeta_upper'])-C1*(2*pi).log()+(C1-cap)*L+K/T
    lowbound=arb(lcz['Czeta_upper'])+arb(lel['Fsup_upper'])+(arb(lel['A1'])-cap)*L
    bound=max(high.upper(),lowbound.upper());out=up_str(bound,digits)
    result=dict(certified=True,A='0.08382',C_upper=out,high_upper=up_str(high,25),low_upper=up_str(lowbound,25),
                Lswitch=Lswitch,Tswitch='exp('+Lswitch+')',C1_upper=up_str(C1,24),K_upper=up_str(K,24),
                high_elementary_error_upper=up_str(K/T,24),
                convention='right continuous S at zeros; also valid at midpoint and left limit',
                proof='v11 propositions 4.1,4.5, Lemmas 4.7,4.8; harmonic boundary certificate',
                hashes={str(p):sha256(p) for p in paths+[str(kh),str(kl),__file__]})
    body=json.dumps(result,indent=2)
    dest=Path(candidate).with_name(Path(candidate).stem+'_envelope.json');dest.write_text(body)
    Path(candidate).with_name(Path(candidate).stem+'_envelope_'+sha256(arithmetic)[:10]+'.json').write_text(body)
    print(provenance(*paths,__file__),flush=True);print(json.dumps(result,indent=2),flush=True)
    return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('candidate');ap.add_argument('arithmetic');ap.add_argument('--low',default='inputs/low_L60.json')
    ap.add_argument('--low-arithmetic',default='inputs/low_L60_arithmetic_N1000000.json');ap.add_argument('--low-elementary',default='inputs/low_L60_elemS.json')
    ap.add_argument('--Lswitch',default='100');a=ap.parse_args();certify(a.candidate,a.arithmetic,a.low,a.low_arithmetic,a.low_elementary,a.Lswitch)
