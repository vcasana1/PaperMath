"""NUMERICAL geometry for screening, not a certificate.
Circles: manuscript v11 §5. Rectangles: Green--Jensen adaptation, derived in
GEOMETRY.md. Weights use image sums in a horizontal strip; costs use the
Dirichlet harmonic extension of each boundary profile.
"""
import math
import numpy as np
from scipy.special import zeta
from scipy.fft import dst
from scipy import sparse
X=np.array([.5]+[1-k/(2**k-2) for k in range(4,10)]+[1.])
E=np.array([1/6]+[1/(2**k-2) for k in range(4,10)]+[0.])
A=np.log([.618]+[1.546]*6+[1.])

def profile(x,which):
    x=np.asarray(x);inside=x<=1
    if which=='J':return np.where(inside,np.interp(x,X,E),0.)
    if which=='G':return inside.astype(float)
    out=np.zeros_like(x);out[inside]=np.interp(x[inside],X,A);out[~inside]=np.log(zeta(x[~inside],1));return out

def circle_cost(c,R,n=160):
    # Split at every profile breakpoint and at the integrable Euler pole.
    breaks=[0.,np.pi]
    for q in X:
        if c-R<q<c+R:breaks.append(math.acos((q-c)/R))
    breaks=sorted(set(breaks));xx,ww=np.polynomial.legendre.leggauss(n);out=[]
    for typ in ['J','G','A']:
        val=0.
        for lo,hi in zip(breaks,breaks[1:]):
            th=(lo+hi)/2+(hi-lo)*xx/2;val+=float(np.dot(ww,profile(c+R*np.cos(th),typ)))*(hi-lo)/2/np.pi
        out.append(val)
    out[2]+=math.log(float(zeta(c,1)/zeta(2*c,1)));return out

def rectangle_cost(a,b,c,H,n=2048):
    W=b-a;x=a+(np.arange(n)+.5)*W/n;u=(c-a)/W;ns=np.arange(1,n+1)
    damping=2*np.exp(-ns*np.pi*H/W)/(1+np.exp(-2*ns*np.pi*H/W));out=[]
    for typ in ['J','G','A']:
        ha,hb=profile(np.array([a,b]),typ);lin=ha+(hb-ha)*(x-a)/W
        coeff=dst(profile(x,typ)-lin,type=2)/n
        value=ha+(hb-ha)*u+np.dot(coeff,np.sin(ns*np.pi*u)*damping)
        out.append(float(value))
    out[2]+=math.log(float(zeta(c,1)/zeta(2*c,1)));return out

def strip_green(dx,y,H):
    k=np.pi/(2*H);q=np.exp(-k*np.abs(dx));ratio=np.cos(k*y)*2*q/(1+q*q)
    return np.arctanh(np.clip(ratio,-1+1e-15,1-1e-15))

def rectangle_green(a,b,c,H,x,y):
    x,y=np.broadcast_arrays(x,y);v=np.zeros_like(x,dtype=float);mask=(x>a)&(x<b)&(np.abs(y)<H)
    xx=x[mask];yy=y[mask];W=b-a;N=math.ceil(30*H/(np.pi*W))+3;z=np.zeros(len(xx))
    for n in range(-N,N+1):z+=strip_green(xx-c+2*n*W,yy,H)-strip_green(xx+c-2*a+2*n*W,yy,H)
    v[mask]=np.maximum(0,z);return v

def weight(g,beta,t):
    x=.5+np.asarray(beta);y=np.asarray(t)+g['v']
    if g['kind']=='circle':return np.maximum(0,np.log(g['R']/np.hypot(g['c']-x,y)))
    return rectangle_green(g['a'],g['b'],g['c'],g['H'],x,y)

def matrix(pool,beta,t,scaling=None):
    values=[];rows=[];cols=[]
    for j,g in enumerate(pool):
        v=weight(g,beta,t)
        if scaling is not None:v*=scaling
        keep=np.flatnonzero(v>0);values.extend(v[keep]);rows.extend(keep);cols.extend([j]*len(keep))
    return sparse.csr_matrix((values,(rows,cols)),shape=(len(t),len(pool)))

def make_pool(mode='both'):
    pool=[];offsets=[-1.5,-1.,-.5,0.,.5,1.,1.5]
    if mode in ['circle','both']:
        for c in [1.03,1.1,1.25,1.5,2.,3.]:
            for a in [.5,.65,.8,.9]:
                cost=circle_cost(c,c-a)
                for v in offsets:pool.append(dict(kind='circle',c=c,R=c-a,v=v,cost=cost))
    if mode in ['rectangle','both']:
        for c in [1.03,1.1,1.3,1.7,2.5]:
            for a in [.5,.7,.9]:
                for extra in [.25,1.]:
                    for H in [.2,.5,1.,2.]:
                        cost=rectangle_cost(a,c+extra,c,H)
                        for v in offsets:pool.append(dict(kind='rectangle',a=a,b=c+extra,c=c,H=H,v=v,cost=cost))
    return pool
