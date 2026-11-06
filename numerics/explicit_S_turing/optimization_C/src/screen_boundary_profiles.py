"""Numerical cost-only comparison of primary-source critical-line inputs.
Not a certificate; threshold for deciding whether a new proof is worth doing.
"""
import sys,json,math
from pathlib import Path
import numpy as np
from scipy.special import zeta
import geometry_jensen as geom
BASE=Path(__file__).resolve().parents[1];f=json.loads((BASE/'certificates/FINAL_RESULT.json').read_text());s=json.loads((BASE/f['solution']).read_text());env=json.loads((BASE/f['envelope_certificate']).read_text());ar=json.loads((BASE/f['arithmetic_certificate']).read_text());kap=np.array(s['geometry_weights'],float);Ak=float(env['kernel_A_upper']);R0=float(ar['Czeta_upper'])-Ak*math.log(2*math.pi)
X=geom.X;E0=geom.E.copy();AA0=geom.A.copy();rows=[]
profiles=[('HPY_0618',1/6,1,.618,'https://arxiv.org/html/2207.02366v1'),('Revers_0611',1/6,1,.611,'https://arxiv.org/html/2602.05614v1'),('Patel_Yang_subWeyl',27/164,0,66.7,'https://arxiv.org/html/2302.13444v1')]
for name,exponent,gamma,constant,url in profiles:
 E=E0.copy();E[0]=exponent;G=np.ones(len(X));G[0]=gamma;AA=AA0.copy();AA[0]=math.log(constant)
 def profile(x,which):
  x=np.asarray(x);inside=x<=1;out=np.zeros_like(x);ys=E if which=='J' else G if which=='G' else AA;out[inside]=np.interp(x[inside],X,ys)
  if which=='A':out[~inside]=np.log(zeta(x[~inside],1))
  return out
 geom.profile=profile;cost=[]
 for g in s['geometries']:
  cost.append(geom.rectangle_cost(g['a'],g['b'],g['c'],g['H'],n=8192) if g['kind']=='rectangle' else geom.circle_cost(g['c'],g['R'],n=512))
 J,G,A=np.array(cost).T;A-=np.array([math.log(zeta(g['c'],1)/zeta(2*g['c'],1)) for g in s['geometries']]);At=Ak+kap@J/math.pi;Bc=kap@G/math.pi;R=R0+kap@A/math.pi;delta=.08382-At;peak=Bc/delta;rough=R+Bc*(math.log(peak)-1);L0=max(10.,min((rough-(2.10221996-.15847575899))/(.09473-.08382),peak));C=rough+Bc*math.pi**2/(8*L0**2)
 rows.append(dict(profile=name,C_numerical=C,A_total=At,B_loglog=Bc,Lswitch_numerical=L0,source=url))
for r in rows:r['gain_numerical']=rows[0]['C_numerical']-r['C_numerical']
out=dict(certified=False,solution=f['solution'],results=rows,warning='Numerical screening only; changing PL exponents requires separate verification and harmonic cost certification.')
(BASE/'certificates/boundary_profile_screen.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
