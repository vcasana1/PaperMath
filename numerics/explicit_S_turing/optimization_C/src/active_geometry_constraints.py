"""Extract certified slacks and shape parameters; no optimality assertion."""
import json
from pathlib import Path
from decimal import Decimal
BASE=Path(__file__).resolve().parents[1]
f=json.loads((BASE/'certificates/FINAL_RESULT.json').read_text());assert f['bound_type']=='Green_Jensen_uniform'
s=json.loads((BASE/f['solution']).read_text());k=json.loads((BASE/f['kernel_certificate']).read_text());e=json.loads((BASE/f['envelope_certificate']).read_text())
rows=sorted(k['interfaces'],key=lambda r:Decimal(r['H_lower']))
a=dict(certified_data=True,global_optimality_proved=False,C=f['C_new'],solution=f['solution'],A_total_upper=e['A_total_upper'],slope_slack_lower=e['slope_slack_lower'],B_loglog_upper=e['B_loglog_upper'],peak_logT_lower=e['peak_logT_lower'],peak_logT_upper=e['peak_logT_upper'],Lswitch=e['Lswitch'],high_upper=e['high_upper'],low_upper=e['low_upper'],smallest_certified_interface_slacks=rows[:20],infinite_tails=k['infinite_tails'],geometries=[dict(geometry={x:y for x,y in g.items() if x!='cost'},weight=w) for g,w in zip(s['geometries'],s['geometry_weights'])],meaning='Arb lower bounds on interface slacks; not a dual certificate of geometric optimality')
(BASE/'certificates/active_geometry_constraints.json').write_text(json.dumps(a,indent=2));print('geometry constraints',f['C_new'],'interfaces',len(rows))
