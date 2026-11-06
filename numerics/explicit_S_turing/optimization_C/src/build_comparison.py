"""Refresh theorems for representative kernels, then write comparison tables."""
import sys,json,hashlib,subprocess
from pathlib import Path
from decimal import Decimal
BASE=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
tags=['d085_m10','adaptive_m10_d1.006257','d085_m12','d100_m15','d100_m20','d100_m25_lag',
      'd100_m40_lag','d105_m40_repaired','d110_m60_panel','d100_m80_lag','d100_m100_critical',
      'd100_m100_empirical','d100_m100_empirical_pp10000','d110_m100_empirical',
      'd100_m100_margin_repaired','d100_m100_lowmargin']
rows=[]
for tag in tags:
    source=BASE/'candidates'/f'{tag}.json'
    if not source.exists():continue
    sol=json.loads(source.read_text());inputhash=sha(source);options=[]
    for p in source.parent.glob(tag+'_arithmetic*.json'):
        r=json.loads(p.read_text())
        if r.get('certified') and r.get('input_sha256')==inputhash:options.append((Decimal(r['Czeta_upper']),p,r))
    if not options:continue
    _,arith,ar=min(options,key=lambda x:x[0])
    with (BASE/'logs'/f'comparison_{tag}.log').open('w') as log:
        subprocess.run([sys.executable,str(BASE/'src/certify_kernel_critical.py'),str(source)],cwd=BASE,stdout=log,stderr=subprocess.STDOUT,check=True)
        subprocess.run([sys.executable,str(BASE/'src/certify_envelope.py'),str(source.relative_to(BASE)),str(arith.relative_to(BASE)),'--Lswitch','auto'],cwd=BASE,stdout=log,stderr=subprocess.STDOUT,check=True)
    env=json.loads(source.with_name(source.stem+'_envelope.json').read_text())
    rows.append(dict(d=sol['d'],m=sol['m'],coefficients=len(sol['c']),C_upper=env['C_upper'],N0=ar['N0'],P0=ar['P0'],
                     solution=str(source.relative_to(BASE)),envelope=str(source.with_name(source.stem+'_envelope.json').relative_to(BASE))))
rows.sort(key=lambda x:(x['m'],float(x['d'])))
(BASE/'certificates/comparison.json').write_text(json.dumps(rows,indent=2))
text='# Comparación de resultados\n\nTodas las cotas de esta tabla cubren **todo T>1**, con pendiente de referencia 0.08382.\nLa cifra anterior 4.40577136 se conserva como referencia del autor; su paquete no fue localizado.\n\n| d | m | Coeficientes | C certificado | Corte N | Fases hasta p |\n|---:|---:|---:|---:|---:|---:|\n'
for r in rows:text+=f"| {r['d']} | {r['m']} | {r['coefficients']} | {r['C_upper']} | {r['N0']} | {r['P0']} |\n"
text+='\nSon mejores cotas superiores encontradas y certificadas para esos datos; no son pruebas de optimalidad en d o m.\n\n'
gap=json.loads((BASE/'certificates/fixed_family_gap_d095_m10.json').read_text())
text+=f"Para un único núcleo con d=0.95,m=10, la dualidad exacta prueba {gap['C_min']} <= C_opt <= {gap['C_max']}; brecha certificada {gap['gap']}. Esta comparación no se aplica a la unión de todas las familias ni a todas las envolventes.\n\n"
text+='La búsqueda HiGHS de orden 100 empleó una caja de parámetros [-10,10]. Su brecha impresa es numérica para ese modelo finito; no se usa como certificado. Los candidatos no incluidos en la tabla quedan como datos de búsqueda, aun si su estimación es favorable.\n'
(BASE/'COMPARACION.md').write_text(text)
print('comparison refreshed',len(rows),'kernels')
