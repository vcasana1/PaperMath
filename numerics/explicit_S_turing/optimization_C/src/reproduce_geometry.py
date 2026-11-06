"""Re-execute every component of a frozen uniform Green--Jensen proof."""
import sys,json,subprocess,shutil,time,argparse,hashlib
from pathlib import Path
from decimal import Decimal
BASE=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--binwidth');a=ap.parse_args();f=json.loads((BASE/'certificates/FINAL_RESULT.json').read_text());assert f['bound_type']=='Green_Jensen_uniform'
run=BASE/'reproduction_geometry'/time.strftime('%Y%m%d_%H%M%S');run.mkdir(parents=True);checks=[]
def execute(name,args):
    with (run/(name+'.log')).open('w') as log:subprocess.run([sys.executable,*map(str,args)],cwd=BASE,stdout=log,stderr=subprocess.STDOUT,check=True)
    checks.append(name);print(name,'PASS',flush=True)
high=run/'high.json';low=run/'low.json';PL=run/'PL_inputs.json';shutil.copy2(BASE/f['solution'],high);shutil.copy2(BASE/f['low_solution'],low)
execute('low_kernel',[BASE/'src/certify_kernel.py',low,f['low_kernel_T1']])
execute('low_arithmetic',[BASE/'src/certify_arithmetic.py',low,'--N',f['low_N0'],'--P0',f['low_P0'],'--step',f['low_step']])
execute('low_elementary',[BASE/'src/certify_elementary.py',low,'.09473','10000'])
execute('PL_inputs',[BASE/'src'/f.get('PL_verifier','certify_pl_inputs.py'),PL])
execute('geometric_kernel',[BASE/'src'/f.get('kernel_verifier','certify_geometry_kernel.py'),high])
execute('harmonic_costs',[BASE/'src'/f.get('cost_verifier','certify_geometry_costs.py'),high,'--PL',PL])
coupled=f.get('coupled_centres',False);arithscript=f.get('arithmetic_verifier','certify_arithmetic_coupled.py' if coupled else 'certify_arithmetic_binned.py');arithsuffix='coupled_binned' if coupled else 'binned'
execute('high_arithmetic',[BASE/'src'/arithscript,high,'--N',f['N0'],'--P0',f['P0'],'--step',f['step'],
    '--binwidth',a.binwidth or f['bin_log_width'],'--extra',f['extra_prime_power_cutoff'],'--chunk-size',f['chunk_size']])
execute('uniform_envelope',[BASE/'src'/f.get('envelope_verifier','certify_geometry_envelope.py'),high,run/f'high_arithmetic_{arithsuffix}_N{f["N0"]}.json','--PL',PL,
    '--low',low,'--low-arithmetic',run/f'low_arithmetic_N{f["low_N0"]}.json','--low-elementary',run/'low_elemS.json','--Lswitch',f['Lswitch']])
value=json.loads((run/('high_joint_geometry_envelope.json' if coupled else 'high_geometry_envelope.json')).read_text())['C_upper'];assert Decimal(value)<=Decimal(f['C_new']),(value,f['C_new'])
execute('universal_lower',[BASE/'src/verify_universal.py',BASE/f['universal_lower_certificate']])
status=dict(complete=True,bound_type='Green_Jensen_uniform',C_reproduced=value,C_claimed=f['C_new'],checks=checks,output=str(run.relative_to(BASE)),bin_log_width=a.binwidth or f['bin_log_width'])
(run/'result.json').write_text(json.dumps(status,indent=2));(BASE/'certificates'/('reproduction_geometry_C'+f['C_new'].replace('.','_')+'.json')).write_text(json.dumps(status,indent=2))
current=json.loads((BASE/'certificates/FINAL_RESULT.json').read_text())
if current['C_new']==f['C_new'] and current['solution']==f['solution']:(BASE/'certificates/reproduction_status.json').write_text(json.dumps(status,indent=2))
print('GEOMETRY REPRODUCTION COMPLETE',value,'output',run,flush=True)
