"""Select an existing completed proof; freeze inputs and recompute its envelope.
This script does not turn numerical candidates into certificates.
"""
import sys,json,hashlib,shutil,subprocess
from pathlib import Path
from decimal import Decimal
BASE=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
options=[]
for p in (BASE/'candidates').glob('*_envelope.json'):
    r=json.loads(p.read_text())
    if not r.get('certified'):continue
    names=list(r['hashes'])[:5]
    if all((BASE/x).exists() and sha(BASE/x)==r['hashes'][x] for x in names):options.append((Decimal(r['C_upper']),p,r,names))
assert options,'No completed proof with intact input hashes'
_,path,env,names=min(options,key=lambda x:x[0]);out=BASE/'certificates/final';out.mkdir(exist_ok=True)
source,arithmetic,low,lowarith,lowelem=[BASE/x for x in names]
with (out/'kernel_refresh.log').open('w') as log:subprocess.run([sys.executable,str(BASE/'src/certify_kernel_critical.py'),str(source)],stdout=log,stderr=subprocess.STDOUT,check=True)
with (out/'source_envelope_refresh.log').open('w') as log:
    subprocess.run([sys.executable,str(BASE/'src/certify_envelope.py'),str(source.relative_to(BASE)),str(arithmetic.relative_to(BASE)),
                    '--low',str(low.relative_to(BASE)),'--low-arithmetic',str(lowarith.relative_to(BASE)),
                    '--low-elementary',str(lowelem.relative_to(BASE)),'--Lswitch','auto'],cwd=BASE,stdout=log,stderr=subprocess.STDOUT,check=True)
copies=[(source,'solution.json'),(arithmetic,'solution_arithmetic.json'),(low,'low.json'),(lowarith,'low_arithmetic.json'),(lowelem,'low_elemS.json'),
        (source.with_name(source.stem+'_kernel.json'),'solution_kernel.json'),(low.with_name(low.stem+'_kernel.json'),'low_kernel.json')]
for src,dest in copies:shutil.copy2(src,out/dest)
polyfile=source.with_name(source.stem+'_critical_polynomial.json')
if polyfile.exists():shutil.copy2(polyfile,out/'critical_polynomial.json')
args=[sys.executable,str(BASE/'src/certify_envelope.py'),'certificates/final/solution.json','certificates/final/solution_arithmetic.json',
      '--low','certificates/final/low.json','--low-arithmetic','certificates/final/low_arithmetic.json','--low-elementary','certificates/final/low_elemS.json','--Lswitch','auto']
with (out/'envelope.log').open('w') as log:subprocess.run(args,cwd=BASE,stdout=log,stderr=subprocess.STDOUT,check=True)
result=json.loads((out/'solution_envelope.json').read_text());ar=json.loads(arithmetic.read_text());la=json.loads(lowarith.read_text());sol=json.loads(source.read_text())
universal='certificates/universal_lower_zeros.json';lower=json.loads((BASE/universal).read_text())['C_lower']
final=dict(proved=True,C_previous='4.40577136',C_previous_audited=False,C_new=result['C_upper'],C_inferior_universal=lower,
           A='0.08382',domain='T>1',global_optimality_proved=False,solution='certificates/final/solution.json',
           arithmetic_certificate='certificates/final/solution_arithmetic.json',kernel_certificate='certificates/final/solution_kernel.json',
           envelope_certificate='certificates/final/solution_envelope.json',selected_from=str(source.relative_to(BASE)),d=sol['d'],m=sol['m'],coefficients=len(sol['c']),
           low_solution='certificates/final/low.json',N0=ar['N0'],P0=ar['P0'],step=ar.get('step','0.005'),
           arithmetic_method='binned' if 'bin_count' in ar else 'direct',bin_log_width=ar.get('bin_log_width','0.0001'),extra_prime_power_cutoff=ar.get('extra_prime_power_cutoff',0),chunk_size=ar.get('chunk_size',5000000),
           kernel_T1=json.loads((out/'solution_kernel.json').read_text()).get('T1'),
           kernel_method=json.loads((out/'solution_kernel.json').read_text()).get('kernel_method','interval'),Lswitch=result['Lswitch'],
           low_N0=la['N0'],low_P0=la['P0'],low_step='0.02',low_kernel_T1=json.loads((out/'low_kernel.json').read_text())['T1'],
           universal_lower_certificate=universal,fixed_family_certificate='certificates/fixed_family_gap_d095_m10.json',
           dependency_versions='certificates/environment.json',base_commit='e41acb3936b6b97c224ed7f31c7eb18bf6d9c5c1')
(BASE/'certificates/FINAL_RESULT.json').write_text(json.dumps(final,indent=2))
improvement=Decimal(final['C_previous'])-Decimal(final['C_new'])
text=f'''# Números finales demostrados\n\n\\[\\boxed{{|S(T)|\\le0.08382\\log T+{final['C_new']},\\qquad T>1.}}\\]\n\n| Cantidad | Valor | Alcance |\n|---|---:|---|\n| C anterior | 4.40577136 | Referencia del autor; paquete anterior no localizado |\n| C nuevo | {final['C_new']} | Cota superior uniforme certificada |\n| C inferior | {lower} | Cota inferior necesaria para cualquier desigualdad uniforme, incluidas envolventes |\n\nReducción certificada respecto a la cifra de referencia: **{improvement}**.\nNúcleo alto: d={sol['d']}, m={sol['m']}, {len(sol['c'])} coeficientes.\nCorte aritmético: {ar['N0']}; fases acopladas hasta p={ar['P0']}; transición log T={result['Lswitch']}.\n\nNo se ha probado optimalidad global. Para la familia fija de un núcleo d=0.95,m=10,\nla cota dual es 3.280652819907774820834 y la cota superior 3.56656806163738605688624;\nesta segunda comparación no se extiende a todas las envolventes.\n'''
(BASE/'FINAL_NUMBERS.md').write_text(text)
print(json.dumps(final,indent=2))
