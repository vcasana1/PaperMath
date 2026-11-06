"""Finite interfaces of the piecewise harmonic Green-weighted majorant."""
import math
import numpy as np
def curves(geometries,T):
    out=[dict(kind='line',p=[0,-T],q=[0,T],name='b0'),dict(kind='line',p=[.5,-T],q=[.5,T],name='bhalf'),dict(kind='line',p=[0,0],q=[.5,0],name='t0')]
    for i,g in enumerate(geometries):
        if g['kind']=='circle':out.append(dict(kind='arc',c=g['c'],R=g['R'],v=g['v'],name=f'circle_{i}'))
        else:
            left=g['a']-.5
            if left>.5:continue
            out.append(dict(kind='line',p=[left,-g['v']-g['H']],q=[left,-g['v']+g['H']],name=f'rect_{i}_left'))
            for sign in [-1,1]:out.append(dict(kind='line',p=[max(0,left),-g['v']+sign*g['H']],q=[.5,-g['v']+sign*g['H']],name=f'rect_{i}_{sign}'))
    return out
def points(curve,u):
    u=np.atleast_1d(u)
    if curve['kind']=='line':
        p=np.array(curve['p']);q=np.array(curve['q']);a=(p+q)/2+u[:,None]*(q-p)/2;return a[:,0],a[:,1]
    theta=u*math.acos((curve['c']-1)/curve['R'])
    return curve['c']-.5-curve['R']*np.cos(theta),-curve['v']+curve['R']*np.sin(theta)
