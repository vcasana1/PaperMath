from lp import *
import itertools, sys
e=bourgain()
m=int(sys.argv[1])
discs=[(c,R,v) for c in [1.0001,1.05,1.1,1.2,1.3] for R in [0.3,0.4,0.5,0.6,0.7,0.8,1.0,1.2] for v in [-0.6,-0.3,0,0.3,0.6]]
for d in [0.7,0.8,0.9]:
    r0=solve_scaled(d,m,nb=26)
    r=solve_scaled(d,m,discs=discs,prof=e,nb=26)
    used=[(discs[k],round(r[1][len(r[2])+k],4)) for k in range(len(discs)) if r[1][len(r[2])+k]>1e-7]
    print('m=%d d=%.2f pure=%.5f hybrid=%.5f'%(m,d,r0[0],r[0]),used[:8],flush=True)
