from lp import *
import sys
e=explicit_profile() if sys.argv[3]=='E' else bourgain()
m=int(sys.argv[1]); ds=[float(x) for x in sys.argv[2].split(',')]
discs=[(c,R,v) for c in [1.0001,1.03,1.06,1.1,1.15,1.2,1.25,1.3,1.4] for R in [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.5,0.6] if c-R<1.0 for v in [-0.5,-0.3,-0.15,0,0.15,0.3,0.5]]
for d in ds:
    r=solve_scaled(d,m,discs=discs,prof=e,nb=26)
    k=len(r[2]); kap=r[1][k:]
    print('prof=%s m=%d d=%.2f hybrid=%.5f  kernel part=%.5f  jensen part=%.5f'%(sys.argv[3],m,d,r[0],r[1][0]/(2*np.pi),r[0]-r[1][0]/(2*np.pi)),flush=True)
