"""Re-execute the final proof, preserving all delivered certificate files."""
import sys,json,subprocess,shutil,time,argparse
from pathlib import Path
from decimal import Decimal
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parent
ap=argparse.ArgumentParser();ap.add_argument('--binwidth',default=None,help='Alternate rigorous bin width; final rounded bound must still pass');args=ap.parse_args()
final=json.loads((BASE/'certificates/FINAL_RESULT.json').read_text())
if final.get('bound_type')=='Green_Jensen_uniform':
    subprocess.run([sys.executable,str(BASE/'src/reproduce_geometry.py'),*sys.argv[1:]],check=True)
    sys.exit(0)
run=BASE/'reproduction'/time.strftime('%Y%m%d_%H%M%S');run.mkdir(parents=True)
checks=[]
def execute(name,args):
    with (run/(name+'.log')).open('w') as log:subprocess.run([sys.executable,*map(str,args)],cwd=BASE,stdout=log,stderr=subprocess.STDOUT,check=True)
    print(name,'PASS',flush=True)
    checks.append(name)
high=run/'high.json';low=run/'low.json'
shutil.copy2(BASE/final['solution'],high);shutil.copy2(BASE/final['low_solution'],low)
execute('low_kernel',[BASE/'src/certify_kernel.py',low,final['low_kernel_T1']])
execute('low_arithmetic',[BASE/'src/certify_arithmetic.py',low,'--N',final['low_N0'],'--P0',final['low_P0'],'--step',final['low_step']])
execute('low_elementary',[BASE/'src/certify_elementary.py',low,'0.09473','10000'])
if final.get('kernel_method')=='critical_polynomial':execute('high_kernel',[BASE/'src/certify_kernel_critical.py',high])
else:execute('high_kernel',[BASE/'src/certify_kernel.py',high,final['kernel_T1']])
binned=final.get('arithmetic_method')=='binned'
arith_script='certify_arithmetic_binned.py' if binned else 'certify_arithmetic.py'
arith_args=[BASE/'src'/arith_script,high,'--N',final['N0'],'--P0',final['P0'],'--step',final['step']]
if binned:arith_args+=['--binwidth',args.binwidth or final['bin_log_width'],'--extra',final['extra_prime_power_cutoff'],'--chunk-size',final['chunk_size']]
execute('high_arithmetic',arith_args)
arith_name=f'high_arithmetic_{"binned_" if binned else ""}N{final["N0"]}.json'
execute('envelope',[BASE/'src/certify_envelope.py',high,run/arith_name,
                    '--low',low,'--low-arithmetic',run/f'low_arithmetic_N{final["low_N0"]}.json',
                    '--low-elementary',run/'low_elemS.json','--Lswitch',final['Lswitch']])
value=json.loads((run/'high_envelope.json').read_text())['C_upper']
assert Decimal(value)<=Decimal(final['C_new']), (value,final['C_new'])
execute('universal_lower',[BASE/'src/verify_universal.py',BASE/final['universal_lower_certificate']])
status=dict(complete=True,C_reproduced=value,C_claimed=final['C_new'],checks=checks,output=str(run.relative_to(BASE)),bin_log_width=args.binwidth or final['bin_log_width'])
(run/'result.json').write_text(json.dumps(status,indent=2));(BASE/'certificates/reproduction_status.json').write_text(json.dumps(status,indent=2))
print('REPRODUCTION COMPLETE',value,'output',run,flush=True)
