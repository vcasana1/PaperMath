"""Check linkage/integrity of the executed proofs; does not replace them."""
import json,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
def read(p):return json.loads((BASE/p).read_text())
def sha(p):return hashlib.sha256((BASE/p).read_bytes()).hexdigest()
f=read('certificates/FINAL_RESULT.json');assert f['proved'] and not f['global_optimality_proved']
env=read(f['envelope_certificate']);assert env['certified'] and env['C_upper']==f['C_new']
for p,h in env['hashes'].items():assert sha(p)==h,('envelope dependency mismatch',p)
high=read(f['kernel_certificate']);arith=read(f['arithmetic_certificate'])
assert high['certified'] and arith['certified'] and high['input_sha256']==arith['input_sha256']==sha(f['solution'])
assert high['code_sha256']==sha('src/certify_kernel_critical.py')
assert arith['code_sha256']==sha('src/certify_arithmetic_binned.py')
assert high['polynomial_sha256']==sha('certificates/final/critical_polynomial.json')
assert high['root_count_with_multiplicity']==high['degree']
for p in ['certificates/fixed_family_gap_d095_m10.json','certificates/fixed_family_gap_d1006257_m10.json']:
    g=read(p);assert g['certified']
    for q,h in g['hashes'].items():assert sha(q)==h,('fixed family dependency mismatch',q)
r=read('certificates/reproduction_status.json');assert r['complete'] and r['C_reproduced']==r['C_claimed']==f['C_new']
assert sha(r['output']+'/high.json')==sha(f['solution'])
out=dict(passed=True,C=f['C_new'],checks=['envelope dependencies','kernel and arithmetic input linkage','current independent verifier code hashes',
    'complete critical polynomial linkage','fixed-family proof linkage','executed reproduction matches final solution'],meaning='integrity check in addition to the executed mathematical verifiers')
(BASE/'certificates/proof_chain_status.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
