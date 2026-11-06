"""Combine a fixed-family dual with the SAME family's single-kernel upper bound."""
import json,sys,hashlib
from pathlib import Path
from flint import arb
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parent/'hybrid_asymptotic'))
from certutil import up_str
source=BASE/'candidates/adaptive_m10_d1.006257.json';stem=source.with_suffix('')
arith=source.with_name(source.stem+'_arithmetic_N100000000.json');elem=source.with_name(source.stem+'_elemS.json')
dual=source.with_name(source.stem+'_dual_certificate.json');din=source.with_name(source.stem+'_dual_input.json');kernel=source.with_name(source.stem+'_kernel.json')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ar,el,du,ke=[json.loads(p.read_text()) for p in [arith,elem,dual,kernel]]
assert ar['certified'] and ke['certified'] and du['certified'] and el['certified']
assert ar['input_sha256']==ke['input_sha256']==el['input_sha256']==sha(source)
assert du['input_sha256']==sha(din) and el['A1']=='0.08382'
hi=arb(ar['Czeta_upper'])+arb(el['Fsup_upper']);low=arb(du['C_lower'])
r=dict(certified=True,scope='single kernel d=1.006257,m=10,A<=0.08382; full uniform objective; not arbitrary envelopes',
       C_min=du['C_lower'],C_max=up_str(hi,25),gap=up_str(hi-low,25),
       hashes={str(p.relative_to(BASE)):sha(p) for p in [source,arith,elem,dual,din,kernel]})
(BASE/'certificates/fixed_family_gap_d1006257_m10.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
