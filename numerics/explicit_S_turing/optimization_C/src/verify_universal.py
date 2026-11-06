"""Verify a necessary lower bound from one rational nonordinate only."""
import sys,json
from pathlib import Path
from fractions import Fraction as Q
from flint import arb,acb,ctx
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'hybrid_asymptotic'))
from certutil import A,exact,down_str,provenance
ctx.prec=256
data=json.loads(Path(sys.argv[1]).read_text());T=A(Q(data['T_rational']));N=T.zeta_nzeros()
assert N.is_exact() and exact(N)==int(data['N'])
neighborhood=A(Q(data['T_rational'])-Q(1,10**45)).union(A(Q(data['T_rational'])+Q(1,10**45)))
Ninterval=neighborhood.zeta_nzeros()
assert Ninterval.is_exact() and exact(Ninterval)==exact(N), 'nonordinate neighborhood not certified'
pi=arb.pi();theta=acb(arb(1)/4,T/2).lgamma().imag-T*pi.log()/2;value=abs(N-1-theta/pi)-arb('0.08382')*T.log()
assert value.lower()>=arb(data['C_lower'])
print(provenance(sys.argv[1],__file__))
print('UNIVERSAL NECESSARY LOWER BOUND VERIFIED:',down_str(value,24))
print('N(T) constant on the rational neighborhood of radius 1e-45: nonordinate certified')
