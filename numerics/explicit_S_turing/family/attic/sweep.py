import json, sys, time, itertools, traceback
from opt_line import optimize
Ls=[float(x) for x in sys.argv[1].split(',')]; out=sys.argv[2]
ds=[0.65,0.75,0.85,1.0,1.2]; bases=[(2,3),(3,3),(4,4),(5,5)]
for L in Ls:
    for d,(mR,mI) in itertools.product(ds,bases):
        t=time.time()
        try:
            r=optimize(d,mR,mI,L,verbose=False); r['val']=r['C1']*L+r['A3_est']; r['time']=time.time()-t
            open(out,'a').write(json.dumps(r)+'\n')
            print('L*=%g d=%.2f m=(%d,%d) A1=%.5f A3=%.4f val=%.4f %.0fs'%(L,d,mR,mI,r['C1'],r['A3_est'],r['val'],r['time']),flush=True)
        except Exception as e:
            print('L*=%g d=%.2f m=(%d,%d) FAILED %s'%(L,d,mR,mI,e),flush=True)
