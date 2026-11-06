"""Record executed geometric proof history; do not equate search with proof."""
import json,hashlib
from pathlib import Path
from decimal import Decimal
BASE=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for p in sorted((BASE/'candidates').glob('*_geometry_envelope.json')):
    e=json.loads(p.read_text())
    if not e.get('certified'):continue
    deps=list(e['hashes']);source=BASE/deps[0]
    if not source.exists() or sha(source)!=e['hashes'][deps[0]]:continue
    s=json.loads(source.read_text());k=BASE/deps[3];a=json.loads((BASE/deps[1]).read_text())
    if not k.exists() or not json.loads(k.read_text()).get('certified'):continue
    rows.append(dict(candidate=str(source.relative_to(BASE)),envelope=str(p.relative_to(BASE)),C=e['C_upper'],boundary_profile=e.get('boundary_profile','baseline'),m=s['m'],coefficients=len(s['c']),geometries=e['geometries'],rectangles=e['rectangles'],circles=e['geometries']-e['rectangles'],joint_centres=e.get('coupled_centres',False),N=a['N0'],P0=a['P0'],current_dependencies_intact=all((BASE/q).exists() and sha(BASE/q)==h for q,h in e['hashes'].items()),kernel_input_sha256=json.loads(k.read_text())['input_sha256']))
rows.sort(key=lambda r:Decimal(r['C']),reverse=True)
(BASE/'certificates/geometry_search_history.json').write_text(json.dumps(rows,indent=2))
p=BASE/'COMPARACION.md';text=p.read_text().split('<!-- GEOMETRY_RESULTS -->')[0].rstrip()
text+='\n\n<!-- GEOMETRY_RESULTS -->\n\n## Ampliación geométrica ejecutada\n\n| C superior | m | Rectángulos | Discos | Perfil | Centros conjuntos | N | Candidato |\n|---:|---:|---:|---:|---|:---:|---:|---|\n'
for r in rows:text+=f"| {r['C']} | {r['m']} | {r['rectangles']} | {r['circles']} | {r['boundary_profile']} | {'sí' if r['joint_centres'] else 'no'} | {r['N']} | {Path(r['candidate']).stem} |\n"
text+='\nSon resultados de cadenas ejecutadas, conservados como historial. El resultado seleccionado y reproducido con los verificadores principales actuales es el de `certificates/FINAL_RESULT.json`. Los metadatos indican qué certificados históricos conservan todos sus enlaces con las versiones actuales. Las versiones anteriores de los verificadores se preservan por separado.\n\nLa primera familia incluyó discos y rectángulos; la primera selección utilizó rectángulos; la búsqueda con centros conjuntos puede seleccionar también discos. La tabla no certifica optimalidad entre geometrías. Los ensayos de orden 1000 son búsquedas numéricas de 269 parámetros, no resultados de esta tabla. El intento geométrico de orden 100 se dejó sin certificar al encarecerse la prueba y resultar inferior a los candidatos de orden 40.\n'
p.write_text(text);print('geometry proof history',len(rows))
