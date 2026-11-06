"""Positive numerical Gaussian quadrature for the actual prime-power measure.
SEARCH ONLY. Three nodes per short log panel reproduce six numerical moments.
The independent arithmetic certifiers never import this module.
"""
import math
import numpy as np
from opt_line import primes

def nodes(d,N,PP,width=.02):
    ps=primes(N);ps=ps[ps>PP];logs=np.log(ps);Ln=[];W=[];k=1
    while len(ps) and int(ps[0])**k<=N:
        if k==1:mask=np.ones(len(ps),bool)
        elif k==2:mask=ps<=math.isqrt(N)
        else:mask=np.array([int(p)**k<=N for p in ps])
        L=k*logs[mask];wt=logs[mask]*np.exp(-(d+.5)*L)
        if not len(L):break
        ids=np.floor(L/width).astype(np.int64);offset=int(ids.min());ids-=offset
        centers=(ids+offset+.5)*width;x=(L-centers)/(width/2)
        mu=np.array([np.bincount(ids,weights=wt*x**r) for r in range(6)])
        unique,start,count=np.unique(ids,return_index=True,return_counts=True)
        for group,i,cnt in zip(unique,start,count):
            mass=mu[0,group];mom=mu[:,group]/mass
            if cnt<3:
                Ln.extend(L[i:i+cnt]);W.extend(wt[i:i+cnt]);continue
            H=np.array([[mom[r+s] for s in range(3)] for r in range(3)])
            H1=np.array([[mom[r+s+1] for s in range(3)] for r in range(3)])
            try:
                ch=np.linalg.cholesky(H);ci=np.linalg.inv(ch);J=ci@H1@ci.T
                xx,V=np.linalg.eigh((J+J.T)/2)
                if np.any(np.abs(xx)>1.00001):raise ValueError('quadrature node outside panel')
                ww=mass*V[0]**2
                assert np.all(ww>=0)
                Ln.extend((group+offset+.5)*width+xx*width/2);W.extend(ww)
            except (np.linalg.LinAlgError,ValueError):Ln.extend(L[i:i+cnt]);W.extend(wt[i:i+cnt])
        k+=1
    # Numerical continuous approximation only above the much larger cutoff N.
    xx,ww=np.polynomial.legendre.leggauss(160)
    edges=sorted(set([np.log(N)]+[x for x in [20.,40.,80.,160.,320.,700.] if x>np.log(N)]))
    for l,r in zip(edges,edges[1:]):
        L=(l+r)/2+(r-l)*xx/2;Ln.extend(L);W.extend((r-l)*ww/2*np.exp((.5-d)*L))
    return np.array(Ln),np.array(W)
