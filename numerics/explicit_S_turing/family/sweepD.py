# Sweep with per-prime phase maximum in the objective (PPMAX=300), m=10, finer d grid.
import json, sys, time, itertools, os
os.environ.setdefault('PPMAX', '300')
from opt_line_pp import optimize
Ls=[float(x) for x in sys.argv[1].split(',')]; out=sys.argv[2]
ds=[0.8,0.85,0.9,0.95,1.0]
for L in Ls:
    for d in ds:
        t=time.time()
        try:
            r=optimize(d,10,10,L,verbose=False); r['val']=r['C1']*L+r['A3_est']; r['time']=time.time()-t; r['pp']=300
            open(out,'a').write(json.dumps(r)+'\n')
            print('L*=%g d=%.2f m=(10,10) A1=%.5f A3=%.4f val=%.4f %.0fs'%(L,d,r['C1'],r['A3_est'],r['val'],r['time']),flush=True)
        except Exception as e:
            print('L*=%g d=%.2f FAILED %s'%(L,d,e),flush=True)
print('SWEEPD_DONE',flush=True)
