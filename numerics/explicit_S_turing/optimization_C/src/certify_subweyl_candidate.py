"""Change only the proved boundary profile, retaining identical kernel data.
An exact byte/hash identity transfers K and arithmetic proofs; new harmonic
costs and the entire height envelope are independently re-executed.
"""
import sys,json,hashlib,shutil,subprocess
from decimal import Decimal
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=Path(sys.argv[1]);p=p if p.is_absolute() else BASE/p;assert p.exists();digest=sha(p);kp=p.with_name(p.stem+'_geometry_kernel.json');kr=json.loads(kp.read_text());assert kr['certified'] and kr['input_sha256']==digest and kr['code_sha256'] in [sha(BASE/'src/certify_geometry_kernel.py'),sha(BASE/'src/certify_geometry_kernel_fast.py')]
choices=[]
for q in p.parent.glob(p.stem+'_arithmetic_coupled_binned_N*.json'):
 r=json.loads(q.read_text())
 if r.get('certified') and r['input_sha256']==digest and r['code_sha256'] in [sha(BASE/'src/certify_arithmetic_coupled.py'),sha(BASE/'src/certify_arithmetic_coupled_fast.py')]:choices.append((Decimal(r['Czeta_upper']),q,r))
assert choices;_,ap,ar=min(choices,key=lambda r:r[0]);pruned='--pruned' in sys.argv;profile='pruned_subweyl' if pruned else 'subweyl';suffix='_pruned' if pruned else '_subweyl';out=p.with_name(p.stem+suffix+'.json');shutil.copy2(p,out);assert sha(out)==digest
newk=out.with_name(out.stem+'_geometry_kernel.json');newa=out.with_name(out.stem+f'_arithmetic_coupled_binned_N{ar["N0"]}.json');shutil.copy2(kp,newk);shutil.copy2(ap,newa)
for stage,args in [('costs',[BASE/'src'/('certify_geometry_costs'+suffix+'.py'),out]),('envelope',[BASE/'src'/('certify_geometry_envelope'+suffix+'.py'),out,newa,'--Lswitch','auto'])]:
 with (BASE/'logs'/f'subweyl_{out.stem}_{stage}.log').open('w') as log:subprocess.run([sys.executable,*map(str,args)],cwd=BASE,stdout=log,stderr=subprocess.STDOUT,check=True)
 print(stage,'PASS',flush=True)
transfer=dict(certified=True,meaning='Identical complete input bytes: unchanged coefficients, geometry parameters and weights; only the boundary estimate changes',original_input=str(p.relative_to(BASE)),profile_input=str(out.relative_to(BASE)),identical_sha256=digest,original_kernel_certificate=str(kp.relative_to(BASE)),original_arithmetic_certificate=str(ap.relative_to(BASE)),boundary_profile=profile,PL_certificate='certificates/geometry_PL_inputs_subweyl.json',source='https://arxiv.org/html/2302.13444v1')
out.with_name(out.stem+'_profile_transfer.json').write_text(json.dumps(transfer,indent=2));print(json.loads(out.with_name(out.stem+'_joint_geometry_envelope.json').read_text())['C_upper'])
