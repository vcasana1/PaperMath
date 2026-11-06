"""Numerical screening of VALID PL node subsets and shifted logarithms.
Profiles use published vertical-line inputs. Shifted-log cases are
numerical screens and have not passed compact PL verification. Costs are
NOT certificates. The chosen subset must be integrated again with Arb.
"""
import json,sys,math,itertools,time
from pathlib import Path
import numpy as np
from scipy.special import zeta
from scipy.optimize import brentq
import geometry_jensen as geom
BASE=Path(__file__).resolve().parents[1];start=time.time();final_path=Path(sys.argv[1]) if len(sys.argv)>1 else BASE/'certificates/FINAL_RESULT.json';f=json.loads(final_path.read_text());s=json.loads((BASE/f['solution']).read_text());e=json.loads((BASE/f['envelope_certificate']).read_text());ar=json.loads((BASE/f['arithmetic_certificate']).read_text());kap=np.array(s['geometry_weights'],float);Ak=float(e['kernel_A_upper']);R0=float(ar['Czeta_upper'])-Ak*math.log(2*math.pi)
XX=np.array([.5]+[1-k/(2**k-2) for k in range(4,10)]+[1.]);EE=np.array([27/164]+[1/(2**k-2) for k in range(4,10)]+[0.]);GG=np.r_[0,np.ones(7)];rows=[]
# Cache quadrature nodes; these data are for numerical ranking only.
leg=geom.np.polynomial.legendre.leggauss;cache={}
def cached(n):
 if n not in cache:cache[n]=leg(n)
 return cache[n]
geom.np.polynomial.legendre.leggauss=cached
for aa,q in [(1.,0.),(.5,3.86),(.2,220.1)]:
 for mask in range(64):
  ids=[0]+[i+1 for i in range(6) if mask>>i&1]+[7];X=XX[ids];E=EE[ids];G=GG[ids];A=np.log(np.array([66.7]+[1.546]*6+[aa]))[ids]
  def profile(x,which):
   x=np.asarray(x);inside=x<=1;out=np.zeros_like(x);ys=E if which=='J' else G if which=='G' else A;out[inside]=np.interp(x[inside],X,ys)
   if which=='A':out[~inside]=np.log(zeta(x[~inside],1))
   return out
  geom.profile=profile;cost=[]
  for g in s['geometries']:
   cost.append(geom.rectangle_cost(g['a'],g['b'],g['c'],g['H'],n=8192) if g['kind']=='rectangle' else geom.circle_cost(g['c'],g['R'],n=512))
  J,G,A=np.array(cost).T;A-=np.array([math.log(zeta(g['c'],1)/zeta(2*g['c'],1)) for g in s['geometries']]);At=Ak+kap@J/math.pi;B=kap@G/math.pi;R=R0+kap@A/math.pi;delta=.08382-At
  if delta<=0:continue
  peak=B/delta-q
  def high(L):
   h=max(L,peak);return R-delta*h+B*math.log(h+q)+B*math.pi**2/(8*(L+q)**2)
  def low(L):return 2.10221996-.15847575899+(.09473-.08382)*L
  if low(10)>high(10):L0=10.
  else:
   hi=300.
   while low(hi)<high(hi):hi*=2
   L0=brentq(lambda L:low(L)-high(L),10.,hi)
  rows.append(dict(C_numerical=max(low(L0),high(L0)),one_line_factor=aa,log_shift=q,node_indices=ids,A_total=At,B_loglog=B,Lswitch=L0,peak_logT=peak))
rows.sort(key=lambda r:r['C_numerical']);out=dict(certified=False,solution=f['solution'],profiles_tested=len(rows),seconds=time.time()-start,ranked_profiles=rows)
(BASE/'certificates/profile_subset_screen.json').write_text(json.dumps(out,indent=2));(BASE/'certificates'/('profile_subset_screen_C'+f['C_new'].replace('.','_')+'.json')).write_text(json.dumps(out,indent=2));print(json.dumps(dict(solution=f['solution'],seconds=out['seconds'],top=rows[:10]),indent=2))
