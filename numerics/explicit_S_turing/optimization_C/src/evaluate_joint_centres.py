"""NUMERICAL screen of exact joint Euler phases of kernel and Jensen centres."""
import sys,json,math,time
from pathlib import Path
import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import zeta
from optimize_extension import weighted_laguerre
BASE=Path(__file__).resolve().parents[1]
def evaluate(path,ng=32):
    start=time.time();s=json.loads(Path(path).read_text());m=s['m'];r=np.array(s['parameters'][:m],float);ii=np.array(s['parameters'][m:],float);q=np.zeros(m);q[:-1]+=ii;q[1:]-=ii;orders=np.flatnonzero((r!=0)|(q!=0)).tolist();gs=s['geometries'];ks0=np.array(s['geometry_weights'],float)
    def ab(L):
        L=np.array(L);lag=weighted_laguerre(L,orders);a=-sum((r[j]*lag[j] for j in orders),np.zeros(len(L)))/np.pi;b=-sum((q[j]*lag[j] for j in orders),np.zeros(len(L)))/np.pi+np.exp(-L/2)*(np.exp(-L)-2)/(np.pi*L)
        for g,k in zip(gs,ks0):
            w=k*np.exp(-(g['c']-1)*L)/(np.pi*L);a-=w*np.cos(g['v']*L);b+=w*np.sin(g['v']*L)
        return a,b
    cache=np.load(BASE/'inputs/empirical_primoss_PP1000_width002.npz');L,W=cache['L'],cache['W'];a,b=ab(L);finite=float(np.dot(W*np.exp(L/2),np.hypot(a,b)))
    far=max(700.,60/min(g['c']-1 for g in gs));xx,ww=np.polynomial.legendre.leggauss(ng);edges=np.linspace(np.log(10**10),far,int(far/2)+1);ls=[];ws=[]
    for lo,hi in zip(edges,edges[1:]):ls.extend((lo+hi)/2+(hi-lo)*xx/2);ws.extend((hi-lo)*ww/2)
    a,b=ab(ls);tail=float(np.dot(ws,np.hypot(a,b)))
    sv=np.ones(1001,bool);sv[:2]=False
    for p in range(2,32):
        if sv[p]:sv[p*p::p]=False
    coupled=0.
    for p in np.flatnonzero(sv):
        ks=np.arange(1,int(np.log(10**10)/np.log(p))+1);L=ks*np.log(p);a,b=ab(L);w=np.log(p)*np.exp(-L);a*=w;b*=w;xx=np.linspace(0,2*np.pi,512,endpoint=False);vv=np.cos(np.outer(xx,ks))@a+np.sin(np.outer(xx,ks))@b;best=float(vv.max())
        for j in np.where((vv>=np.roll(vv,1))&(vv>=np.roll(vv,-1)))[0]:
            rr=minimize_scalar(lambda x:-float(np.cos(ks*x)@a+np.sin(ks*x)@b),bounds=(xx[j]-2*np.pi/512,xx[j]+2*np.pi/512),method='bounded');best=max(best,-rr.fun)
        coupled+=best
    joint=finite+tail+coupled;center=sum(k*np.log(zeta(g['c'],1)/zeta(2*g['c'],1))/np.pi for g,k in zip(gs,ks0));envpath=Path(path).with_name(Path(path).stem+'_geometry_envelope.json');estimate=None
    if envpath.exists():
        env=json.loads(envpath.read_text());arith=Path(list(env['hashes'])[1]);ar=json.loads(arith.read_text());estimate=float(env['high_upper'])-float(ar['Czeta_upper'])-center+joint
    return dict(candidate=path,gauss_nodes=ng,Czeta_joint_numerical=joint,centre_fee_separate=center,uniform_C_numerical=estimate,tail_numerical=tail,seconds=time.time()-start,certified=False)
if __name__=='__main__':
    rows=[]
    for p in sys.argv[1:]:
        for ng in [32,64]:r=evaluate(p,ng);rows.append(r);print(json.dumps(r),flush=True)
    (BASE/'certificates/joint_centres_numerical.json').write_text(json.dumps(rows,indent=2))
