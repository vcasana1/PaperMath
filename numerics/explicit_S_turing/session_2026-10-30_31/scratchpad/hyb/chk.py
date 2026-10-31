from lp import *
import sys
e=explicit_profile()
m=4; d=0.7
discs=[(c,R,v) for c in [1.0001,1.03,1.06,1.1,1.15,1.2,1.25,1.3,1.4] for R in [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.5,0.6] if c-R<1.0 for v in [-0.5,-0.3,-0.15,0,0.15,0.3,0.5]]
r0=solve_scaled(d,m,nb=26); print('pure',r0[0], 'viol',check(d,r0[1],r0[2],(),nb=101,nt=20001))
r=solve_scaled(d,m,discs=discs,prof=e,nb=26); print('hyb',r[0],'viol',check(d,r[1],r[2],discs,nb=101,nt=20001))
np.save('sol_m4_E.npy',r[1])
