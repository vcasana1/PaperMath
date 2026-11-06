"""Sequential executed proof pipeline. Stop at the first failed proof stage."""
import sys,argparse,subprocess
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('output');ap.add_argument('--N',type=int,default=10**8);ap.add_argument('--P0',type=int,default=10000);ap.add_argument('--step',default='0.02');ap.add_argument('--joint',action='store_true');ap.add_argument('--general',action='store_true');ap.add_argument('--profile',choices=['baseline','subweyl','pruned_subweyl'],default='baseline');ap.add_argument('--Lswitch',default='100');a=ap.parse_args()
source,out=Path(a.source),Path(a.output)
suffix={'baseline':'','subweyl':'_subweyl','pruned_subweyl':'_pruned'}[a.profile]
steps=[('repair',[BASE/'src'/('repair_geometry_general.py' if a.general else 'repair_geometry.py'),source,out]),
 ('kernel',[BASE/'src/certify_geometry_kernel_fast.py',out]),
 ('costs',[BASE/'src'/('certify_geometry_costs'+suffix+'.py'),out]),
 ('arithmetic',[BASE/'src'/('certify_arithmetic_coupled_fast.py' if a.joint else 'certify_arithmetic_binned.py'),out,'--N',a.N,'--P0',a.P0,'--step',a.step]),
 ('envelope',[BASE/'src'/('certify_geometry_envelope'+suffix+'.py'),out,out.with_name(out.stem+f'_arithmetic_{"coupled_binned" if a.joint else "binned"}_N{a.N}.json'),'--Lswitch',a.Lswitch])]
for name,args in steps:
    log=BASE/'logs'/f'geometry_pipeline_{out.stem}_{name}.log'
    with log.open('w') as f:subprocess.run([sys.executable,*map(str,args)],cwd=BASE,stdout=f,stderr=subprocess.STDOUT,check=True)
    print(name,'PASS',flush=True)
