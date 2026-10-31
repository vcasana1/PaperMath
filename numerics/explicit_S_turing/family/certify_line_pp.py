# Certify one line with the per-prime phase maximum in C_zeta: kernel inequality, C_zeta (cz_gen_pp), elementary part (N and S).
import json, sys, os, subprocess, math, glob
tag=sys.argv[1]; src=sys.argv[2]; pat=sys.argv[3] if len(sys.argv)>3 else 'sweep*.jsonl'
if src.endswith('.json'): r=json.load(open(src))
else:
    L=float(src); rs=[json.loads(l) for f in glob.glob(pat) for l in open(f)]
    r=min((x for x in rs if x['Lstar']==L), key=lambda x:x['val'])
D='line_'+tag; os.makedirs(D,exist_ok=True); sol=D+'/sol.json'; json.dump(r,open(sol,'w'))
def run(cmd,log):
    with open(D+'/'+log,'w') as fh: p=subprocess.run(cmd,stdout=fh,stderr=subprocess.STDOUT)
    out=open(D+'/'+log).read(); lines=out.strip().splitlines(); print(lines[-1] if lines else '(no output)',flush=True); return p.returncode,out
A1=math.ceil(r['C1']*1e5)/1e5; A1s='%.5f'%A1
print('candidate', tag, 'd=',r['d'], 'C1=',r['C1'], 'A3_est=',r['A3_est'], flush=True)
rc1,o1=run(['python3','../hybrid_asymptotic/certify_hybrid.py',sol,'100'],'cert_kernel.txt')
if not (rc1==0 and 'all certified' in o1): rc1,o1=run(['python3','../hybrid_asymptotic/certify_hybrid.py',sol,'2000'],'cert_kernel.txt')
rc2,o2=run(['python3','cz_gen_pp.py',sol,'1e8','1000'],'cert_czeta_pp.txt')
rc3,o3=run(['python3','elem_gen.py',sol,A1s,'10000'],'cert_elem.txt')
rc4,o4=run(['python3','elem_gen.py',sol,A1s,'10000','S'],'cert_elem_S.txt')
if rc1==0 and 'all certified' in o1 and rc2==0 and rc3==0 and rc4==0:
    cz=float(json.load(open(sol.replace('.json','_czpp.json')))['Czeta_upper'])
    fN=float(json.load(open(sol.replace('.json','_elem.json')))['Fsup_upper']); fS=float(json.load(open(sol.replace('.json','_elemS.json')))['Fsup_upper'])
    AN=math.ceil((cz+fN)*1e3)/1e3; AS=math.ceil((cz+fS)*1e3)/1e3
    json.dump({'A1':A1s,'A3_N':'%.3f'%AN,'A3_S':'%.3f'%AS,'Czeta_pp_upper':cz,'Fsup_N':fN,'Fsup_S':fS,'d':r['d'],'B':r['B'],'Lstar':r['Lstar']},open(D+'/summary_pp.json','w'),indent=1)
    print('LINE %s CERTIFIED: |N(T)-main| <= %s log T + %.3f ;  |S(T)| <= %s log T + %.3f  (T>=1)'%(tag,A1s,AN,A1s,AS),flush=True)
else: print('LINE %s FAILED'%tag,flush=True)
