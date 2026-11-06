"""Tabulate executed arithmetic costs; comparisons keep the kernel fixed."""
import json,hashlib
from pathlib import Path
from decimal import Decimal
BASE=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
groups={}
for p in (BASE/'candidates').glob('*_arithmetic*.json'):
    r=json.loads(p.read_text())
    if not r.get('certified') or 'Czeta_upper' not in r:continue
    group=groups.setdefault(r['input_sha256'],{})
    key=(r['N0'],r['P0'],r.get('step'),r.get('extra_prime_power_cutoff',0),r.get('bin_log_width'))
    if key not in group or Decimal(r['Czeta_upper'])<Decimal(group[key][1]['Czeta_upper']):group[key]=(p,r)
names={sha(p):p.stem for p in (BASE/'candidates').glob('*.json') if '"B"' in p.read_text()[:1000] and '"c"' in p.read_text()}
text='# Coste y beneficio de la certificación aritmética\n\nLos tiempos son mediciones de ejecución, afectadas por la carga concurrente.\nLas comparaciones dentro de cada bloque usan exactamente los mismos coeficientes.\nEl término de error de ψ es una contribución al mayorante, no una brecha de optimalidad del núcleo.\n\n'
out=[]
for key,group in groups.items():
    if len(group)<2:continue
    name=names.get(key,key[:12]);text+=f'## {name}\n\n| N | P0 | Cζ superior | Error ψ superior | Exceso de bins | Segundos |\n|---:|---:|---:|---:|---:|---:|\n'
    for p,r in sorted(group.values(),key=lambda z:(z[1]['N0'],z[1]['P0'],Decimal(z[1]['Czeta_upper']))):
        text+=f"| {r['N0']} | {r['P0']} | {r['Czeta_upper']} | {r.get('error_upper','—')} | {r.get('bin_excess_upper','—')} | {r.get('seconds',0):.1f} |\n"
        out.append(dict(kernel_sha256=key,certificate=str(p.relative_to(BASE)),**r))
    text+='\n'
text+='La cola principal se integra con el peso original. Aumentar N reduce la incertidumbre de ψ y la aproximación por normas de las potencias aún no acopladas; no elimina la contribución aritmética verdadera. No se ha demostrado que los parámetros del núcleo sean óptimos.\n'
(BASE/'ARITHMETIC_BUDGET.md').write_text(text);(BASE/'certificates/arithmetic_budget.json').write_text(json.dumps(out,indent=2))
print('arithmetic budget rows',len(out))
