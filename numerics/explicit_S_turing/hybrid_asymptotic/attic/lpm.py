# LP with margin: f <= sum c_j G_j + sum kappa_k W_k - eta/(1+t^2) on (b,t) in [0,1/2] x (R\{0}), cutting planes.
import numpy as np, sys, json
from fractions import Fraction as Fr
from scipy.optimize import linprog
def f(b,t,d): return 2*np.arctan((b+d)/t)+2*np.arctan((d-b)/t)-np.arctan((b+2*d)/t)-np.arctan((2*d-b)/t)
def F(x,t,k,j):
    z=(x+1j*t)**(-j); return z.real if k=='R' else -z.imag
def bourgain_nodes():
    k,l=Fr(13,84),Fr(55,84); nodes=[]
    for _ in range(8):
        nodes.append((l-k,k)); k,l=k/(2*k+2),Fr(1,2)+l/(2*k+2)
    nodes.append((Fr(1),Fr(0))); return nodes
def explicit_nodes():
    return [(Fr(1,2),Fr(27,164))]+[(1-Fr(m,2**m-2),Fr(1,2**m-2)) for m in range(4,10)]+[(Fr(1),Fr(0))]
def J_float(nodes,c,R,n=200001):
    xs=np.array([float(a) for a,_ in nodes]); es=np.array([float(e) for _,e in nodes])
    th=np.linspace(0,np.pi,n); s=c+R*np.cos(th); v=np.where(s>=1,0,np.interp(s,xs,es))
    return np.trapezoid(v,th)/np.pi
def rows(d,B,discs,bb,tt,eta):
    G=np.array([F(d+bb,tt,k,j)+F(d-bb,tt,k,j) for (k,j) in B]).T
    W=np.array([np.maximum(0,np.log(R/np.sqrt((c-0.5-bb)**2+(tt+v)**2))) for (c,R,v) in discs]).T
    return np.hstack([G,W]), f(bb,tt,d)+eta/(1+tt**2)
def tgrid(tmax):
    p=np.unique(np.concatenate([[1e-9],np.geomspace(1e-4,tmax,700),np.linspace(0,4,400)[1:]])); return np.concatenate([-p[::-1],p])
def solve(d,m,discs,nodes,eta,maxit=40,tol=0.0):
    B=[('R',j) for j in range(1,m+1)]+[('I',j) for j in range(2,m+1)]
    sc=np.array([(d-0.5)**j for (_,j) in B])
    J=[J_float(nodes,c,R) for (c,R,v) in discs]
    obj=np.concatenate([[1/(2*np.pi)],np.zeros(len(B)-1),np.array(J)/np.pi])
    bnds=[(None,None)]*len(B)+[(0,None)]*len(discs)
    bb,tt=[a.ravel() for a in np.meshgrid(np.linspace(0,0.5,26),tgrid(300.),indexing='ij')]
    A,Fv=rows(d,B,discs,bb,tt,eta)
    S=np.concatenate([sc,np.ones(len(discs))])
    bfine=np.linspace(0,0.5,201); tp=np.geomspace(1e-8,3000.,15000); tfine=np.concatenate([-tp[::-1],tp])
    # asymptotic constraint 2d c_R1 - 2 c_R2 >= eta
    arow=np.zeros(len(B)+len(discs)); arow[0]=2*d; arow[1]=-2
    for it in range(maxit):
        r=linprog(obj*S,A_ub=-np.vstack([A,arow])*S,b_ub=-np.concatenate([Fv,[eta]]),bounds=bnds,method='highs'); x=r.x*S
        nb=[];nt=[];worst=-1
        used=[k for k in range(len(discs)) if x[len(B)+k]>0]
        dU=[discs[k] for k in used]; xU=np.concatenate([x[:len(B)],x[len(B)+np.array(used,dtype=int)]]) if used else x[:len(B)]
        for b in bfine:
            Ar,Fr_=rows(d,B,dU,np.full_like(tfine,b),tfine,eta) if used else (np.array([F(d+b,tfine,k,j)+F(d-b,tfine,k,j) for (k,j) in B]).T, f(b,tfine,d)+eta/(1+tfine**2))
            v=Fr_-Ar@xU; worst=max(worst,v.max())
            idx=np.where((v>tol)&(v>=np.roll(v,1))&(v>=np.roll(v,-1)))[0]; nb+=[b]*len(idx); nt+=list(tfine[idx])
        if not nb: break
        A2,F2=rows(d,B,discs,np.array(nb),np.array(nt),eta); A=np.vstack([A,A2]); Fv=np.concatenate([Fv,F2])
    return obj@x, x, B, J, worst, it
if __name__=='__main__':
    m=int(sys.argv[1]); d=float(sys.argv[2]); prof=sys.argv[3]; eta=float(sys.argv[4])
    nodes=bourgain_nodes() if prof=='B' else explicit_nodes()
    discs=[(c,R,v) for c in [1.03,1.06,1.1,1.15,1.2,1.25,1.3,1.4] for R in [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.5,0.6] if c-R>=0.5 and c-R<1 for v in [-0.5,-0.3,-0.15,0,0.15,0.3,0.5]]
    val,x,B,J,w,it=solve(d,m,discs,nodes,eta)
    keep=[k for k in range(len(discs)) if x[len(B)+k]>1e-10]
    print('m=%d d=%.2f prof=%s eta=%g C=%.6f kernel=%.6f viol=%.2e it=%d ndiscs_used=%d'%(m,d,prof,eta,val,x[0]/(2*np.pi),w,it,len(keep)),flush=True)
    json.dump({'m':m,'d':d,'prof':prof,'eta':eta,'B':B,'c':list(x[:len(B)]),'discs':[discs[k] for k in keep],'kappa':[x[len(B)+k] for k in keep],'J':[J[k] for k in keep],'C':val},open('sol_m%d_%s_eta%g.json'%(m,prof,eta),'w'))
