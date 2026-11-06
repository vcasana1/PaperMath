"""Numerical boundary profiles for search only; independent Arb counterparts exist."""
import numpy as np
from scipy.special import zeta
import geometry_jensen as geom

def configure(name):
    if name=='baseline':return
    assert name in ['subweyl','pruned_subweyl']
    stop=8 if name=='pruned_subweyl' else 10
    X=np.array([.5]+[1-k/(2**k-2) for k in range(4,stop)]+[1.])
    E=np.array([27/164]+[1/(2**k-2) for k in range(4,stop)]+[0.]);G=np.r_[0.,np.ones(len(X)-1)];AA=np.log([66.7]+[1.546]*(len(X)-2)+[1.])
    def profile(x,which):
        x=np.asarray(x);inside=x<=1;out=np.zeros_like(x);ys=E if which=='J' else G if which=='G' else AA;out[inside]=np.interp(x[inside],X,ys)
        if which=='A':out[~inside]=np.log(zeta(x[~inside],1))
        return out
    geom.X=X;geom.E=E;geom.A=AA;geom.profile=profile
