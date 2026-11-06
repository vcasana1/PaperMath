"""Check linkage/integrity of the executed proofs; does not replace them."""
import json,hashlib,argparse
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
def read(p):return json.loads((BASE/p).read_text())
def sha(p):
    p=Path(p)
    if p.is_absolute() and 'optimization_C' in p.parts:
        p=Path(*p.parts[p.parts.index('optimization_C')+1:])
    elif p.is_absolute() and 'explicit_S_turing' in p.parts:
        p=Path('..')/Path(*p.parts[p.parts.index('explicit_S_turing')+1:])
    return hashlib.sha256((BASE/p).read_bytes()).hexdigest()
ap=argparse.ArgumentParser();ap.add_argument('--final',default='certificates/FINAL_RESULT.json');ap.add_argument('--reproduction',default='certificates/reproduction_status.json');ap.add_argument('--output',default='certificates/proof_chain_status.json');args=ap.parse_args()
f=read(args.final);assert f['proved'] and not f['global_optimality_proved']
env=read(f['envelope_certificate']);assert env['certified'] and env['C_upper']==f['C_new']
for p,h in env['hashes'].items():assert sha(p)==h,('envelope dependency mismatch',p)
high=read(f['kernel_certificate']);arith=read(f['arithmetic_certificate'])
assert high['certified'] and arith['certified'] and high['input_sha256']==arith['input_sha256']==sha(f['solution'])
assert arith['code_sha256']==sha('src/'+f.get('arithmetic_verifier','certify_arithmetic_coupled.py' if f.get('coupled_centres') else 'certify_arithmetic_binned.py'))
if f.get('bound_type')=='Green_Jensen_uniform':
    assert high['code_sha256']==sha('src/'+f.get('kernel_verifier','certify_geometry_kernel.py'))
    assert high['interface_coordinates']=='constructed independently in exact rational arithmetic'
    assert all(t['root_count']==t['degree'] for t in high['infinite_tails'])
    co=read(f['geometry_cost_certificate']);pl=read(f['PL_certificate'])
    assert co['certified'] and pl['certified'] and co['input_sha256']==sha(f['solution'])
    assert co['code_sha256']==sha('src/'+f.get('cost_verifier','certify_geometry_costs.py')) and pl['code_sha256']==sha('src/'+f.get('PL_verifier','certify_pl_inputs.py'))
    assert co['PL_certificate_sha256']==sha(f['PL_certificate'])
else:
    assert high['code_sha256']==sha('src/certify_kernel_critical.py')
    assert high['polynomial_sha256']==sha('certificates/final/critical_polynomial.json')
    assert high['root_count_with_multiplicity']==high['degree']
for p in ['certificates/fixed_family_gap_d095_m10.json','certificates/fixed_family_gap_d1006257_m10.json']:
    g=read(p);assert g['certified']
    for q,h in g['hashes'].items():assert sha(q)==h,('fixed family dependency mismatch',q)
r=read(args.reproduction);assert r['complete'] and r['C_reproduced']==r['C_claimed']==f['C_new']
assert sha(r['output']+'/high.json')==sha(f['solution'])
out=dict(passed=True,C=f['C_new'],checks=['envelope dependencies','kernel and arithmetic input linkage','current independent verifier code hashes',
    'complete critical polynomial linkage','fixed-family proof linkage','executed reproduction matches final solution'],meaning='integrity check in addition to the executed mathematical verifiers')
(BASE/args.output).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
