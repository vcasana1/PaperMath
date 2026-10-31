# Sweep with longer kernels (m = 7, 10) for the explicit all-T lines.
import json, sys, time, itertools
from opt_line import optimize
Ls=[float(x) for x in sys.argv[1].split(',')]; out=sys.argv[2]
ds=[0.65,0.75,0.85]; bases=[(7,7),(10,10)]
for L in Ls:
    for (mR,mI),d in itertools.product(bases,ds):
        t=time.time()
        try:
            r=optimize(d,mR,mI,L,verbose=False); r['val']=r['C1']*L+r['A3_est']; r['time']=time.time()-t
            open(out,'a').write(json.dumps(r)+'\n')
            print('L*=%g d=%.2f m=(%d,%d) A1=%.5f A3=%.4f val=%.4f %.0fs'%(L,d,mR,mI,r['C1'],r['A3_est'],r['val'],r['time']),flush=True)
        except Exception as e:
            print('L*=%g d=%.2f m=(%d,%d) FAILED %s'%(L,d,mR,mI,e),flush=True)
print('SWEEPC_DONE',flush=True)
