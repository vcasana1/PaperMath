"""Keep numerical objectives separate from uniform proved constants."""
import json,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];rows=[]
for p in (BASE/'candidates').glob('*.json'):
 r=json.loads(p.read_text())
 if r.get('certified') or not r.get('centre_coupled') or 'C_numerical' not in r:continue
 rows.append(dict(candidate=str(p.relative_to(BASE)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),C_numerical=r['C_numerical'],d=r['d'],m=r['m'],geometries=len(r['geometries']),minimum_scaled_residual_numerical=r.get('numerical_worst'),phase_gap_numerical=r.get('phasegap'),height_gap_numerical=r.get('height_gap'),seconds=r.get('seconds')))
rows.sort(key=lambda r:r['C_numerical']);out=dict(certified=False,meaning='Numerical objectives with finite constraints; a lower value is not a proved uniform constant, even if a nearby repaired input has been proved.',best=rows[0] if rows else None,candidates=rows)
(BASE/'certificates/unproved_candidate_summary.json').write_text(json.dumps(out,indent=2));print(json.dumps(out['best'],indent=2))
