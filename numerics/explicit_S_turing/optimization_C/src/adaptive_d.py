"""Adaptive nonconvex outer search in d. Inner problems remain convex.
No global optimality in d or m is claimed. Values rounded to six decimals
are exact rational parameters of the final independently certified kernels.
"""
import json,time,contextlib
from pathlib import Path
from scipy.optimize import minimize_scalar
from optimize import search
prior=Path('certificates/adaptive_d_search.json')
cache={float(k):v for k,v in json.loads(prior.read_text()).get('values',{}).items()} if prior.exists() else {}
start=time.time()
def objective(x):
    d=round(float(x),6)
    if d not in cache:
        tag=f'adaptive_m10_d{d:.6f}'
        with open('logs/'+tag+'.log','w') as f,contextlib.redirect_stdout(f):r=search(d,10,eta=1e-7,representation='laguerre')
        if r is None:val=1e4
        else:
            Path('candidates/'+tag+'.json').write_text(json.dumps(r,indent=2));val=r['C_est']
        cache[d]=val;print('adaptive',d,val,'elapsed',time.time()-start,flush=True)
    return cache[d]
r=minimize_scalar(objective,bounds=(.85,1.2),method='bounded',options={'xatol':1e-4,'maxiter':30})
Path('certificates/adaptive_d_search.json').write_text(json.dumps(dict(success=bool(r.success),best_d=min(cache,key=cache.get),values=cache,seconds=time.time()-start,certified=False),indent=2))
