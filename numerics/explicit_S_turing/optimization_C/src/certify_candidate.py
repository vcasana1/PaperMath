"""Sequential proof pipeline: a failed stage stops all dependent work."""
import sys,argparse,subprocess
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('candidate');ap.add_argument('--N',type=int,default=10**10)
ap.add_argument('--P0',type=int,default=10**6);ap.add_argument('--binwidth',default='0.0001')
ap.add_argument('--chunk-size',type=int,default=5000000);a=ap.parse_args()
source=Path(a.candidate)
steps=[('kernel',[BASE/'src/certify_kernel_critical.py',source]),
       ('arithmetic',[BASE/'src/certify_arithmetic_binned.py',source,'--N',a.N,'--P0',a.P0,'--step','0.005','--binwidth',a.binwidth,'--chunk-size',a.chunk_size]),
       ('envelope',[BASE/'src/certify_envelope.py',source,source.with_name(source.stem+f'_arithmetic_binned_N{a.N}.json'),'--Lswitch','auto'])]
for name,args in steps:
    log=BASE/'logs'/f'pipeline_{source.stem}_{name}_N{a.N}.log'
    with log.open('w') as f:subprocess.run([sys.executable,*map(str,args)],cwd=BASE,stdout=f,stderr=subprocess.STDOUT,check=True)
    print(name,'PASS',flush=True)
