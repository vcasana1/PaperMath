import sys, math, numpy as np
sys.path.insert(0,'../hyb'); from lp import build, tgrid
from scipy.optimize import linprog
from czeta2 import sieve, czeta
from czeta3 import tail_pnt
from elem import elem
P=sieve(10**7)
def lp_min(d,B,eta=1e-4):
    tg=tgrid(); bb,tt,G,F=build(d,B,np.linspace(0,0.5,41),tg)
    F=F+eta/(1+tt**2)
    obj=np.zeros(len(B)); obj[0]=1/(2*math.pi)
    r=linprog(obj,A_ub=-G,b_ub=-F,bounds=[(None,None)]*len(B),method='highs'); return r.x
for d,B in [(0.713,[('R',1),('R',2),('I',2),('I',3)]),(0.72,[('R',1),('R',2),('I',2),('I',3)]),(0.75,[('R',1),('R',2),('R',3),('I',2),('I',3)])]:
    x=lp_min(d,B); cR={j:v for (k,j),v in zip(B,x) if k=='R'}; cI={j:v for (k,j),v in zip(B,x) if k=='I'}
    C1=cR[1]/(2*math.pi); cz=czeta(d,cR,cI,P,10**7)+tail_pnt(d,cR,cI,10**7)
    F=max(max(float(elem(T,d,cR,cI)[0]),-float(elem(T,d,cR,cI)[1]))-C1*math.log(T) for T in [1,2,5,20,100,1e4,1e8])
    print('d=%.3f basis=%s  C1=%.5f  Czeta~%.3f  elem sup~%.3f  => const~%.3f'%(d,[k+str(j) for k,j in B],C1,cz,F,cz+F),flush=True)
