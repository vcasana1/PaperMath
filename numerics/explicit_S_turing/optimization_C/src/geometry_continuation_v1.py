"""Executed adaptive outer search. Only Arb proof outputs select the best.
A stage limit yields an unfinished checkpoint; it is not a stopping proof.
"""
import argparse,json,subprocess,sys,time
from decimal import Decimal
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('seed');ap.add_argument('--start',type=int,default=3);ap.add_argument('--stages',type=int,default=4);ap.add_argument('--factor',default='2');a=ap.parse_args()
seed=Path(a.seed);factor=Decimal(a.factor);history=[];begin=time.time()
def run(label,args,limit=600):
    p=BASE/'logs'/f'geometry_continuation_{label}.log'
    with p.open('w') as f:subprocess.run([sys.executable,*map(str,args)],cwd=BASE,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=limit)
for i in range(a.start,a.start+a.stages):
    t=time.time();prefix=f'geometry_m40_joint_neighbors{i}';pool=Path('inputs')/(prefix+'_pool.json');out=Path('candidates')/(prefix+'.json');fixed=out.with_name(out.stem+'_repaired.json')
    run(prefix+'_pool',[BASE/'src/refine_geometry_pool.py',seed,pool,str(factor)])
    run(prefix+'_search',[BASE/'src/screen_geometry_joint.py','--m',40,'--maxit',1,'--geometry','both','--primes','inputs/empirical_primoss_PP1000_width002.npz','--pool',pool,'--seed',seed,'--out',out])
    run(prefix+'_proof',[BASE/'src/geometry_pipeline.py',out,fixed,'--joint','--Lswitch','auto'])
    env=fixed.with_name(fixed.stem+'_joint_geometry_envelope.json');e=json.loads((BASE/env).read_text())
    oldenv=seed.with_name(seed.stem+'_joint_geometry_envelope.json');old=json.loads((BASE/oldenv).read_text());gain=Decimal(old['C_upper'])-Decimal(e['C_upper']);record=dict(stage=i,factor=str(factor),seed=str(seed),candidate=str(fixed),C=e['C_upper'],previous_C=old['C_upper'],gain=str(gain),seconds=time.time()-t)
    history.append(record);print(json.dumps(record),flush=True)
    if gain>0:seed=fixed
    if gain<Decimal('.0001'):factor/=2
    state=dict(status='checkpoint',selected=str(seed),stages=history,elapsed_seconds=time.time()-begin,criterion='gain >= 0.0001 with reasonable local runtime; checkpoint is not a global optimum')
    (BASE/'certificates/geometry_continuation_status.json').write_text(json.dumps(state,indent=2))
    if factor<Decimal('.125'):
        state['status']='local_step_refinement_stagnated';(BASE/'certificates/geometry_continuation_status.json').write_text(json.dumps(state,indent=2));break
