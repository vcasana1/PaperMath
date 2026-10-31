#!/bin/bash
# Recompute certified C_zeta with the per-prime phase maximum for every line; write summary_pp.json
cd /home/claude/papermath/numerics/explicit_S_turing/family
for D in line_L5 line_L20 line_L60 line_L150 line_L400 line_L1000 line_L2500 line_C400; do
  [ -e $D/sol_czpp.json ] || nice -n 5 python3 cz_gen_pp.py $D/sol.json 1e8 1000 > $D/cert_czeta_pp.txt 2>&1
  python3 - $D <<'PY'
import json, math, sys, os
D=sys.argv[1]; r=json.load(open(D+'/sol.json')); cz=float(json.load(open(D+'/sol_czpp.json'))['Czeta_upper'])
s=json.load(open(D+'/summary.json')) if os.path.exists(D+'/summary.json') else None
fs=float(json.load(open(D+'/sol_elem.json'))['Fsup_upper']); A1=s['A1'] if s else '%.5f'%(math.ceil(r['C1']*1e5)/1e5)
out={'A1':A1,'A3_N':'%.3f'%(math.ceil((cz+fs)*1e3)/1e3),'Czeta_pp_upper':cz,'Fsup_upper':fs}
if os.path.exists(D+'/sol_elemS.json'):
    fS=float(json.load(open(D+'/sol_elemS.json'))['Fsup_upper']); out['A3_S']='%.3f'%(math.ceil((cz+fS)*1e3)/1e3)
json.dump(out,open(D+'/summary_pp.json','w'),indent=1); print(D, out, flush=True)
PY
done
echo RECERT_DONE
