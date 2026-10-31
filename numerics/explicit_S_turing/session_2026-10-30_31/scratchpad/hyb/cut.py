# cutting-plane LP: solve on a coarse grid, add the worst points of a fine grid until the fine-grid violation is <= tol.
from lp import *
import sys, time
def rows(d,B,discs,bb,tt,sc):
    G=np.array([basis(d+bb,tt,k,j)+basis(d-bb,tt,k,j) for (k,j) in B]).T*sc
    W=np.array([np.maximum(0,np.log(R/np.sqrt((c-0.5-bb)**2+(tt+v)**2))) for (c,R,v) in discs]).T if discs else np.zeros((len(bb),0))
    return np.hstack([G,W]), f(bb,tt,d)
def run(d,m,discs,prof,tol=1e-7,nbf=201,ntf=30001,maxit=30):
    B=[('R',j) for j in range(1,m+1)]+[('I',j) for j in range(2,m+1)]
    sc=np.array([(d-0.5)**j for (_,j) in B])
    J=[jensen(prof,c,R) for (c,R,v) in discs]
    obj=np.concatenate([[sc[0]/(2*np.pi)],np.zeros(len(B)-1),np.array(J)/np.pi])
    bnds=[(None,None)]*len(B)+[(0,None)]*len(discs)
    bg=np.linspace(0,0.5,26); tg=tgrid(300.)
    bb,tt=[a.ravel() for a in np.meshgrid(bg,tg,indexing='ij')]
    A,F=rows(d,B,discs,bb,tt,sc)
    bfine=np.linspace(0,0.5,nbf); tp=np.geomspace(1e-8,3000.,ntf//2); tfine=np.concatenate([-tp[::-1],tp])
    for it in range(maxit):
        r=linprog(obj,A_ub=-A,b_ub=-F,bounds=bnds,method='highs'); x=r.x
        newb=[];newt=[];worst=0
        for b in bfine:
            Ar,Fr=rows(d,B,discs,np.full_like(tfine,b),tfine,sc)
            v=Fr-Ar@x; worst=max(worst,v.max())
            idx=np.where((v>tol)&(v>=np.roll(v,1))&(v>=np.roll(v,-1)))[0]
            newb+= [b]*len(idx); newt+=list(tfine[idx])
        if not newb: break
        A2,F2=rows(d,B,discs,np.array(newb),np.array(newt),sc); A=np.vstack([A,A2]); F=np.concatenate([F,F2])
    xs=x.copy(); xs[:len(B)]*=sc
    return r.fun, worst, it, xs, B, J
if __name__=='__main__':
    m=int(sys.argv[1]); d=float(sys.argv[2]); pr=sys.argv[3]
    prof=explicit_profile() if pr=='E' else bourgain()
    discs=[] if pr=='none' else [(c,R,v) for c in [1.0001,1.03,1.06,1.1,1.15,1.2,1.25,1.3,1.4] for R in [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.5,0.6] if c-R<1.0 for v in [-0.5,-0.3,-0.15,0,0.15,0.3,0.5]]
    t0=time.time(); val,w,it,x,B,J=run(d,m,discs,prof)
    kern=x[0]/(2*np.pi)
    print('prof=%s m=%d d=%.2f C1=%.5f (kernel %.5f, Jensen %.5f) residual viol=%.1e iters=%d  %.0fs'%(pr,m,d,val,kern,val-kern,w,it,time.time()-t0),flush=True)
    np.save('x_%s_m%d_d%.2f.npy'%(pr,m,d),x)
