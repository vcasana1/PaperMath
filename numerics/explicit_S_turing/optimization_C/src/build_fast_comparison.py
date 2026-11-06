"""Compare two executed rigorous summations on identical complete inputs."""
from pathlib import Path
from decimal import Decimal
import json,hashlib,ast
BASE=Path(__file__).resolve().parents[1];source=BASE/'candidates/geometry_m60_d1p1_joint_neighbors7_repaired.json';digest=hashlib.sha256(source.read_bytes()).hexdigest();rows=[]
for p in (BASE/'candidates').glob(source.stem+'_arithmetic_coupled_binned_N100000000_P*.json'):
 r=json.loads(p.read_text());assert r['certified'] and r['input_sha256']==digest
 programs={hashlib.sha256((BASE/'src'/name).read_bytes()).hexdigest():name for name in ['certify_arithmetic_coupled.py','certify_arithmetic_coupled_fast.py']};assert r['code_sha256'] in programs
 rows.append(dict(certificate=str(p.relative_to(BASE)),verifier=programs[r['code_sha256']],code_sha256=r['code_sha256'],Czeta_upper=r['Czeta_upper'],seconds=r['seconds'],Lfar=r['Lfar'],error_boxes=r['error_boxes']))
assert len(rows)==2
rows.sort(key=lambda r:r['seconds'])
def jet(name):
 tree=ast.parse((BASE/'src'/name).read_text());outer=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='certify');return ast.dump(next(n for n in outer.body if isinstance(n,ast.FunctionDef) and n.name=='fulljet'))
assert jet('certify_arithmetic_coupled.py')==jet('certify_arithmetic_coupled_fast.py')
out=dict(certified_comparison=True,same_input_sha256=digest,identical_derivative_code_AST=True,upper_difference=str(abs(Decimal(rows[0]['Czeta_upper'])-Decimal(rows[1]['Czeta_upper']))),rows=rows,meaning='Both are rigorous upper bounds for identical input bytes. All omitted mass remains bounded explicitly.')
(BASE/'certificates/coupled_fast_comparison.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
