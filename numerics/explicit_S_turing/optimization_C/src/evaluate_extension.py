"""Independent DENSER NUMERICAL re-evaluation. This is not an Arb proof.
Integrate in sqrt(log x) to resolve high-order Laguerre oscillations.
Compare the candidate and incumbent on exactly the same data and nodes.
"""
import sys,json,math,time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar
from optimize_extension import weighted_laguerre
BASE=Path(__file__).resolve().parents[1]

def evaluate(path,ng=64):
    start=time.time();s=json.loads(Path(path).read_text());assert float(s['d'])==1.;m=s['m'];r=np.array(s['parameters'][:m],float);ii=np.array(s['parameters'][m:],float)
    # L L_{j-2}^1(L)/(j-1)=L_{j-2}(L)-L_{j-1}(L).
    q=np.zeros(m);q[:-1]+=ii;q[1:]-=ii;orders=np.flatnonzero((r!=0)|(q!=0)).tolist()
    def ab(L):
        L=np.array(L);lag=weighted_laguerre(L,orders);a=sum((r[j]*lag[j] for j in orders),np.zeros(len(L)))/(-np.pi)
        b=sum((q[j]*lag[j] for j in orders),np.zeros(len(L)))/(-np.pi)+np.exp(-L/2)*(np.exp(-L)-2)/(np.pi*L)
        return a,b
    cache=np.load(BASE/'inputs/empirical_primoss_PP1000_width002.npz');L=cache['L'];W=cache['W'];aa,bb=ab(L);finite=np.sum(W*np.exp(L/2)*np.hypot(aa,bb))
    x,w=np.polynomial.legendre.leggauss(ng);edges=np.linspace(np.sqrt(np.log(10**10)),np.sqrt(max(700,6*m+100)),max(48,m//8)+1);Lall=[];Wall=[]
    for lo,hi in zip(edges,edges[1:]):
        y=(lo+hi)/2+(hi-lo)*x/2;Lall.extend(y*y);Wall.extend(w*(hi-lo)*y)
    aa,bb=ab(Lall);tail=float(np.dot(Wall,np.hypot(aa,bb)))
    sv=np.ones(1001,bool);sv[:2]=False
    for p in range(2,32):
        if sv[p]:sv[p*p::p]=False
    coupled=0.
    for p in np.flatnonzero(sv):
        ks=np.arange(1,int(np.log(10**10)/np.log(p))+1);L=ks*np.log(p);aa,bb=ab(L);weight=np.log(p)*np.exp(-L);aa*=weight;bb*=weight
        xx=np.linspace(0,2*np.pi,512,endpoint=False);vv=np.cos(np.outer(xx,ks))@aa+np.sin(np.outer(xx,ks))@bb;best=float(vv.max())
        for j in np.where((vv>=np.roll(vv,1))&(vv>=np.roll(vv,-1)))[0]:
            rr=minimize_scalar(lambda x:-float(np.cos(ks*x)@aa+np.sin(ks*x)@bb),bounds=(xx[j]-2*np.pi/512,xx[j]+2*np.pi/512),method='bounded');best=max(best,-rr.fun)
        coupled+=best
    A=r.sum()/(2*np.pi);C=finite+tail+coupled-A*np.log(2*np.pi)+(A-.08382)*135
    return dict(candidate=str(path),m=m,gauss_nodes=ng,C_numerical=float(C),tail_numerical=tail,finite_uncoupled_numerical=float(finite),coupled_numerical=coupled,A=float(A),seconds=time.time()-start,certified=False)

if __name__=='__main__':
    rows=[]
    for p in sys.argv[1:]:
        for ng in [64,128,256]:
            row=evaluate(p,ng);rows.append(row);print(json.dumps(row),flush=True)
    (BASE/'certificates/extension_numerical_recheck.json').write_text(json.dumps(rows,indent=2))
