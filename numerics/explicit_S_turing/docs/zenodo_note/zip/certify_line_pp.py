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
from decimal import Decimal, ROUND_CEILING
A1s=str(Decimal(repr(r['C1'])).quantize(Decimal('0.00001'),rounding=ROUND_CEILING)); A1=float(A1s)
print('candidate', tag, 'd=',r['d'], 'C1=',r['C1'], 'A3_est=',r['A3_est'], flush=True)
rc1,o1=run(['python3','../hybrid_asymptotic/certify_hybrid.py',sol,'100'],'cert_kernel.txt')
if not (rc1==0 and 'all certified' in o1): rc1,o1=run(['python3','../hybrid_asymptotic/certify_hybrid.py',sol,'2000'],'cert_kernel.txt')
rc2,o2=run(['python3','cz_gen_pp.py',sol,'1e8','1000'],'cert_czeta_pp.txt')
rc3,o3=run(['python3','elem_gen.py',sol,A1s,'10000'],'cert_elem.txt')
rc4,o4=run(['python3','elem_gen.py',sol,A1s,'10000','S'],'cert_elem_S.txt')
def finish(D, sol, r, A1s, tag):
    # The certified upper endpoints are decimal strings; keep them as decimals and round up to three decimals.
    from decimal import Decimal, ROUND_CEILING, localcontext
    with localcontext() as dc:
        dc.prec = 60
        cz=Decimal(json.load(open(sol.replace('.json','_czpp.json')))['Czeta_upper'])
        fN=Decimal(json.load(open(sol.replace('.json','_elem.json')))['Fsup_upper'])
        fS=Decimal(json.load(open(sol.replace('.json','_elemS.json')))['Fsup_upper'])
        AN=(cz+fN).quantize(Decimal('0.001'),rounding=ROUND_CEILING); AS=(cz+fS).quantize(Decimal('0.001'),rounding=ROUND_CEILING)
    json.dump({'A1':A1s,'A3_N':str(AN),'A3_S':str(AS),'Czeta_pp_upper':str(cz),'Fsup_N':str(fN),'Fsup_S':str(fS),'d':r['d'],'B':r['B'],'Lstar':r['Lstar']},open(D+'/summary_pp.json','w'),indent=1)
    print('LINE %s CERTIFIED: |N(T)-main| <= %s log T + %s ;  |S(T)| <= %s log T + %s  (T>=1)'%(tag,A1s,AN,A1s,AS),flush=True)
if rc1==0 and 'all certified' in o1 and rc2==0 and rc3==0 and rc4==0: finish(D, sol, r, A1s, tag)
else: print('LINE %s FAILED'%tag,flush=True)
