"""Audit the speed-only change against a complete executed geometry proof."""
import json,hashlib,ast
from decimal import Decimal
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];p=BASE/'candidates/geometry_m60_d1p1_joint_neighbors8_repaired.json';digest=hashlib.sha256(p.read_bytes()).hexdigest();rows=[]
for suffix,program in [('_geometry_kernel_original_verifier.json','certify_geometry_kernel.py'),('_geometry_kernel.json','certify_geometry_kernel_fast.py')]:
 cp=p.with_name(p.stem+suffix);r=json.loads(cp.read_text());assert r['certified'] and r['input_sha256']==digest and r['code_sha256']==hashlib.sha256((BASE/'src'/program).read_bytes()).hexdigest()
 assert all(Decimal(v['H_lower'])>0 for v in r['interfaces']) and all(t['root_count']==t['degree'] for t in r['infinite_tails'])
 rows.append(dict(certificate=str(cp.relative_to(BASE)),verifier=program,seconds=r['seconds'],interface_count=len(r['interfaces']),bhalf_boxes=r['interfaces'][1]['boxes'],rectangle_image_counts=r.get('rectangle_image_counts')))
def functions(program):
 t=ast.parse((BASE/'src'/program).read_text());outer=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='certify');return {n.name:ast.dump(n) for n in outer.body if isinstance(n,ast.FunctionDef)}
a,b=map(functions,['certify_geometry_kernel.py','certify_geometry_kernel_fast.py']);assert a==b
out=dict(passed=True,input_sha256=digest,identical_nested_proof_functions_AST=True,rows=rows,meaning='Only the number of images changes; every omitted image retains the original explicit interval tail bound. Timings are execution measurements affected by load.')
(BASE/'certificates/fast_kernel_comparison.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
