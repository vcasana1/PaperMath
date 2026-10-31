# Certify one candidate line: kernel inequality, C_zeta, elementary part; write line_<tag>/summary.json
import json, sys, os, subprocess, math, glob
from fractions import Fraction as Fr
tag=sys.argv[1]; src=sys.argv[2]
r=json.loads(open(src).read()) if src.endswith('.json') else None
if r is None:   # pick best candidate for L*=src from sweeps
    L=float(src); rs=[json.loads(l) for f in glob.glob('sweep*.jsonl') for l in open(f)]
    r=min((x for x in rs if x['Lstar']==L), key=lambda x:x['val'])
D='line_'+tag; os.makedirs(D,exist_ok=True); sol=D+'/sol.json'; json.dump(r,open(sol,'w'))
def run(cmd,log):
    with open(D+'/'+log,'w') as fh: p=subprocess.run(cmd,stdout=fh,stderr=subprocess.STDOUT,cwd='.')
    out=open(D+'/'+log).read(); print(out.strip().splitlines()[-1],flush=True); return p.returncode,out
A1=math.ceil(r['C1']*1e5)/1e5; A1s='%.5f'%A1
rc1,o1=run(['python3','../hybrid_asymptotic/certify_hybrid.py',sol,'100'],'cert_kernel.txt')
if not (rc1==0 and 'all certified' in o1): rc1,o1=run(['python3','../hybrid_asymptotic/certify_hybrid.py',sol,'2000'],'cert_kernel.txt')
rc2,o2=run(['python3','cz_gen.py',sol,'1e8'],'cert_czeta.txt')
rc3,o3=run(['python3','elem_gen.py',sol,A1s,'10000'],'cert_elem.txt')
ok = rc1==0 and 'all certified' in o1 and rc2==0 and rc3==0
if ok:
    cz=float(json.load(open(sol.replace('.json','_cz.json')))['Czeta_upper']); fs=float(json.load(open(sol.replace('.json','_elem.json')))['Fsup_upper'])
    A3=math.ceil((cz+fs)*1e3)/1e3
    json.dump({'A1':A1s,'A3':'%.3f'%A3,'Czeta_upper':cz,'Fsup_upper':fs,'d':r['d'],'B':r['B'],'Lstar':r['Lstar']},open(D+'/summary.json','w'),indent=1)
    print('LINE %s CERTIFIED: |N(T)-main| <= %s log T + %.3f  (T>=1)'%(tag,A1s,A3),flush=True)
else: print('LINE %s FAILED'%tag,flush=True)
