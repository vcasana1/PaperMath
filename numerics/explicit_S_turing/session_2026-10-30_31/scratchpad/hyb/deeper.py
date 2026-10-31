from lp import *
import sys
e=bourgain(); m=int(sys.argv[1]); d=float(sys.argv[2])
discs=[(c,R,v) for c in [1.02,1.04,1.06,1.08,1.1,1.13,1.16,1.2,1.25,1.3,1.35,1.4,1.5] for R in [0.06,0.08,0.1,0.13,0.16,0.2,0.25,0.3,0.35,0.4,0.5,0.6,0.7] if 0.5<=c-R<1.0 for v in [-0.6,-0.45,-0.3,-0.2,-0.1,0,0.1,0.2,0.3,0.45,0.6]]
r=solve_scaled(d,m,discs=discs,prof=e,nb=21)
print('m=%d d=%.2f ndiscs=%d hybrid(grid)=%.5f'%(m,d,len(discs),r[0]),flush=True)
