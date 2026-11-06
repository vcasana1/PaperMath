"""Freeze the best COMPLETE geometric proof, retaining every prior snapshot."""
import sys,json,hashlib,shutil,subprocess
from pathlib import Path
from decimal import Decimal
BASE=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
options=[]
for p in (BASE/'candidates').glob('*_geometry_envelope.json'):
    r=json.loads(p.read_text())
    if r.get('certified') and all((BASE/q).exists() and sha(BASE/q)==h for q,h in r['hashes'].items()):options.append((Decimal(r['C_upper']),p,r))
assert options,'No complete geometric proof with intact dependencies'
_,p,env=min(options,key=lambda z:z[0]);names=list(env['hashes']);source,arithmetic,cost,kernel,PL,low,lowarith,lowelem,lowkernel=[BASE/n for n in names[:9]]
oldpath=BASE/'certificates/FINAL_RESULT.json'
if oldpath.exists():
    old=json.loads(oldpath.read_text());tag='PURE_KERNEL' if old.get('bound_type')!='Green_Jensen_uniform' else 'C'+old['C_new'].replace('.','_')
    archive=BASE/'certificates'/f'{tag}_FINAL_RESULT.json'
    if not archive.exists():shutil.copy2(oldpath,archive)
    num=BASE/'certificates'/f'{tag}_FINAL_NUMBERS.md'
    if not num.exists():shutil.copy2(BASE/'FINAL_NUMBERS.md',num)
    if tag=='PURE_KERNEL' and (BASE/'certificates/reproduction_status.json').exists():shutil.copy2(BASE/'certificates/reproduction_status.json',BASE/'certificates/pure_kernel_reproduction_status.json')
profile=env.get('boundary_profile','baseline');suffix={'baseline':'','subweyl':'_subweyl','pruned_subweyl':'_pruned'}[profile];envscript='certify_geometry_envelope'+suffix+'.py'
signature=hashlib.sha256((''.join(sha(q) for q in [source,arithmetic,cost,kernel,PL,low,lowarith,lowelem,lowkernel])+sha(BASE/'src'/envscript)).encode()).hexdigest()
out=BASE/'certificates'/('final_geometry_C'+env['C_upper'].replace('.','_'))
if out.exists():
    record=out/'snapshot_signature.json'
    if not record.exists() or json.loads(record.read_text()).get('signature')!=signature:out=out.with_name(out.name+'_proof_'+signature[:10])
out.mkdir(exist_ok=True)
(out/'snapshot_signature.json').write_text(json.dumps(dict(signature=signature),indent=2))
for src,name in [(source,'solution.json'),(arithmetic,'solution_arithmetic.json'),(cost,'solution_geometry_costs.json'),(kernel,'solution_geometry_kernel.json'),(PL,'PL_inputs.json'),
                 (low,'low.json'),(lowarith,'low_arithmetic.json'),(lowelem,'low_elemS.json'),(lowkernel,'low_kernel.json')]:shutil.copy2(src,out/name)
rel=out.relative_to(BASE)
profile=env.get('boundary_profile','baseline');suffix={'baseline':'','subweyl':'_subweyl','pruned_subweyl':'_pruned'}[profile];envscript='certify_geometry_envelope'+suffix+'.py';costscript='certify_geometry_costs'+suffix+'.py';plscript='certify_pl_inputs'+('_subweyl' if profile!='baseline' else '')+'.py'
with (out/'envelope.log').open('w') as log:
    subprocess.run([sys.executable,str(BASE/'src'/envscript),str(rel/'solution.json'),str(rel/'solution_arithmetic.json'),
                    '--low',str(rel/'low.json'),'--low-arithmetic',str(rel/'low_arithmetic.json'),'--low-elementary',str(rel/'low_elemS.json'),
                    '--PL',str(rel/'PL_inputs.json'),'--Lswitch',env['Lswitch']],cwd=BASE,stdout=log,stderr=subprocess.STDOUT,check=True)
coupled=env.get('coupled_centres',False);envelope_name='solution_joint_geometry_envelope.json' if coupled else 'solution_geometry_envelope.json'
fenv=json.loads((out/envelope_name).read_text());assert fenv['C_upper']==env['C_upper']
ar=json.loads(arithmetic.read_text());s=json.loads(source.read_text());la=json.loads(lowarith.read_text());lower=json.loads((BASE/'certificates/universal_lower_zeros.json').read_text())['C_lower']
f=dict(proved=True,kernel_verifier=env.get('kernel_verifier','certify_geometry_kernel.py'),arithmetic_verifier=env.get('arithmetic_verifier','certify_arithmetic_coupled.py' if coupled else 'certify_arithmetic_binned.py'),boundary_profile=profile,envelope_verifier=envscript,cost_verifier=costscript,PL_verifier=plscript,bound_type='Green_Jensen_uniform',C_previous='4.40577136',C_previous_audited=False,C_new=fenv['C_upper'],C_inferior_universal=lower,A='0.08382',domain='T>1',global_optimality_proved=False,
    solution=str(rel/'solution.json'),arithmetic_certificate=str(rel/'solution_arithmetic.json'),kernel_certificate=str(rel/'solution_geometry_kernel.json'),geometry_cost_certificate=str(rel/'solution_geometry_costs.json'),PL_certificate=str(rel/'PL_inputs.json'),
    envelope_certificate=str(rel/envelope_name),selected_from=str(source.relative_to(BASE)),d=s['d'],m=s['m'],coefficients=len(s['c']),geometries=fenv['geometries'],rectangles=fenv['rectangles'],circles=fenv['geometries']-fenv['rectangles'],coupled_centres=coupled,
    low_solution=str(rel/'low.json'),N0=ar['N0'],P0=ar['P0'],step=ar['step'],arithmetic_method='coupled_binned' if coupled else 'binned',bin_log_width=ar['bin_log_width'],extra_prime_power_cutoff=ar['extra_prime_power_cutoff'],chunk_size=ar.get('chunk_size',5000000),
    kernel_method='piecewise_harmonic_geometry',Lswitch=fenv['Lswitch'],low_N0=la['N0'],low_P0=la['P0'],low_step='0.02',low_kernel_T1=json.loads(lowkernel.read_text())['T1'],
    universal_lower_certificate='certificates/universal_lower_zeros.json',fixed_family_certificate='certificates/fixed_family_gap_d095_m10.json',dependency_versions='certificates/environment.json',base_commit='e41acb3936b6b97c224ed7f31c7eb18bf6d9c5c1')
oldpath.write_text(json.dumps(f,indent=2))
text=f'''# Números finales demostrados\n\n\\[\\boxed{{|S(T)|\\le0.08382\\log T+{f['C_new']},\\qquad T>1.}}\\]\n\n| Cantidad | Valor | Alcance |\n|---|---:|---|\n| C anterior | 4.40577136 | Referencia del autor; paquete anterior no localizado |\n| C nuevo | {f['C_new']} | Cota superior uniforme certificada con Green--Jensen |\n| C inferior | {lower} | Necesaria para cualquier desigualdad uniforme, incluidas envolventes |\n\nReducción respecto a la referencia: **{Decimal(f['C_previous'])-Decimal(f['C_new'])}**.\nNúcleo racional: d={s['d']}, m={s['m']}, {len(s['c'])} coeficientes; {f['rectangles']} rectángulos y {f['circles']} discos con pesos no negativos.\nA total <= {fenv['A_total_upper']}; B de log log T <= {fenv['B_loglog_upper']}.\nPerfil de borde: {profile}; centros acoplados: {coupled}.
El término B se absorbe usando la holgura de pendiente y el máximo analítico en log T.\nCorte aritmético {ar['N0']}; fases conjuntas hasta p={ar['P0']}; cobertura baja hasta log T={fenv['Lswitch']}.\n\nNo se ha probado optimalidad global. Las cotas duales de familias fijas sin rectángulos no se trasladan a esta familia.\n'''
(BASE/'FINAL_NUMBERS.md').write_text(text);print(json.dumps(f,indent=2))
