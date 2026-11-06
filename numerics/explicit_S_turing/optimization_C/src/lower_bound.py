"""Rigorous lower bound on a FIXED-family high-height surrogate.

J(c)=C_zeta(c)+(L0-log(2*pi))*c_R1/(2*pi)-.08382*L0,
with (K) and c_R1/(2*pi)<=.08382. This is not a lower bound on
the optimum of arbitrary multi-kernel envelopes. Supports use COMPLETE
prime series at rational phases, not truncated Fourier polynomials.
An LP finds dual multipliers; Arb then solves the exact active linear
system and proves their positivity. Only the latter result is certified.
"""
import sys,json,math,argparse,time
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
from scipy.optimize import linprog
from scipy.special import eval_laguerre,eval_genlaguerre
from flint import arb,acb,arb_mat,acb_poly
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'family'));sys.path.insert(0,str(ROOT/'hybrid_asymptotic'))
from opt_line import basis,primes
from certutil import A,box,up_str,down_str,sha256,provenance

def conversion(d,B,exact=False):
    n=len(B);out=[[Q(0) for _ in B] for _ in B];lam=2*(Q(str(d))-Q(1,2))
    for col,(kind,j) in enumerate(B):
        off=1 if kind=='R' else 2
        for k in range(j-off+1):out[B.index((kind,k+off))][col]=math.comb(j-off,k)*(-lam)**k
    return out if exact else np.array(out,dtype=float)

def run(candidate,N=10**5,iterations=25):
    start=time.time();sol=json.loads(Path(candidate).read_text());d=float(sol['d']);m=sol['m'];B=basis(m,m);n=len(B);lam=2*(d-.5)
    conv=conversion(d,B);p=primes(N);lp=np.log(p);sig=d+.5;cap=.08382;L0=100.
    old=np.array(sol['c'],float);params=np.linalg.solve(conv,old)
    tp=np.unique(np.r_[0.,np.linspace(0,5,500),np.geomspace(1e-7,2000,1200)])
    tv=np.r_[-tp[:0:-1],tp];tv[tv==0]=1e-100
    points=[('t',repr(float(t))) for t in tv]+[('b',repr(float(b))) for b in np.linspace(0,.5,101)]
    def krow(kind,x):
        b=.5 if kind=='t' else x;t=x if kind=='t' else 0.
        z1=d+b+1j*t;z2=d-b+1j*t;row=[]
        for kind_,j in B:
            off=1 if kind_=='R' else 2;v=z1**(-off)*(1-lam/z1)**(j-off)+z2**(-off)*(1-lam/z2)**(j-off)
            row.append(v.real if kind_=='R' else -v.imag)
        f=(np.sign(t)*np.pi-2*np.arctan(t/(d+b))-2*np.arctan(t/(d-b))+np.arctan(t/(2*d+b))+np.arctan(t/(2*d-b))) if t else np.pi
        scale=1+t*t
        return np.r_[np.array(row)*scale,0.],f*scale
    rows=[];rhs=[];meta=[]
    for kind,x in points:
        rr,ff=krow(kind,float(x));rows.append(rr);rhs.append(ff);meta.append((kind,x))
    rows.append(np.r_[-conv[0],0.]);rhs.append(-2*np.pi*cap);meta.append(('cap','0'))
    rows.append(np.r_[2*d*conv[0]-2*conv[1],0.]);rhs.append(0.);meta.append(('tail','0'))
    # Boxes only make the numerical support-generation LP bounded. They are
    # not admissible in a final certificate; active boxes are rejected.
    bound=10000.
    for j in range(n):
        row=np.zeros(n+1);row[j]=1;rows.extend([row,-row]);rhs.extend([-bound,-bound]);meta.extend([('box',str(j)),('box',str(j))])
    planes=[];qden=2**32
    def support(v):
        # Choose phases from the first harmonic, refining small primes using
        # a numerical phase scan. The certifier evaluates the full series.
        aa=np.zeros(len(p));bb=np.zeros(len(p))
        for j in range(m):
            aa-=v[j]*eval_laguerre(j,lam*lp)/np.pi
        for j in range(2,m+1):bb-=v[m+j-2]*lp*eval_genlaguerre(j-2,1,lam*lp)/((j-1)*np.pi)
        bb+=(np.exp(-d*lp)-2)/(lp*np.pi)
        phase=np.mod(np.arctan2(bb,aa),2*np.pi)
        small=np.where(p<=1000)[0]
        for ii in small:
            xx=np.linspace(phase[ii]-.8,phase[ii]+.8,96)
            value=np.zeros(len(xx))
            for k in range(1,60):
                LL=k*lp[ii];weight=lp[ii]*np.exp(-sig*LL)
                ar=-sum(v[j]*eval_laguerre(j,lam*LL) for j in range(m))/np.pi
                bi=(np.exp(-d*LL)-2)/(LL*np.pi)-sum(v[m+j-2]*LL*eval_genlaguerre(j-2,1,lam*LL)/(j-1) for j in range(2,m+1))/np.pi
                value+=weight*(ar*np.cos(k*xx)+bi*np.sin(k*xx))
            phase[ii]=xx[np.argmax(value)]
        qs=np.rint(np.mod(phase,2*np.pi)/(2*np.pi)*qden).astype(np.int64);phase=2*np.pi*qs/qden
        ar=np.zeros(n);base=0.
        # Direct convergent series for numerical support. The Arb stage below
        # uses rational polylogarithms and exact logarithms instead.
        for k in range(1,100):
            LL=k*lp;weight=lp*np.exp(-sig*LL);co=np.cos(k*phase);si=np.sin(k*phase)
            for col,(kind,j) in enumerate(B):
                value=eval_laguerre(j-1,lam*LL) if kind=='R' else LL*eval_genlaguerre(j-2,1,lam*LL)/(j-1)
                ar[col]-=np.dot(weight*(co if kind=='R' else si),value)/np.pi
            base+=np.sum(weight*(np.exp(-d*LL)-2)/(LL*np.pi)*si)
            if k>=5 and np.max(weight)*max(1,float(np.max(LL))**(m-1)/math.factorial(m-1))<1e-30:break
        return ar,base,qs.tolist()
    obj=np.r_[conv[0]*(L0-np.log(2*np.pi))/(2*np.pi),1.]
    for it in range(iterations):
        row,constant,qs=support(params);planes.append(qs)
        rows.append(np.r_[-row,1.]);rhs.append(constant);meta.append(('phase',str(len(planes)-1)))
        rr=np.array(rows);ff=np.array(rhs)
        res=linprog(obj,A_ub=-rr,b_ub=-ff,bounds=[(None,None)]*(n+1),method='highs')
        if not res.success:raise RuntimeError(res.message)
        params=res.x[:n];dual=-res.ineqlin.marginals
        active=np.where(dual>1e-7)[0]
        print('LP',it,'lower numerically',res.fun-cap*L0,'active',len(active),'boxes',sum(meta[i][0]=='box' for i in active),flush=True)
        if it>=4 and all(meta[i][0]!='box' for i in active) and len(active)==n+1:
            # A feasible, positive dual is useful at any iteration; keep improving.
            pass
    data=dict(candidate=str(candidate),d=str(d),m=m,N=N,L0='100',qden=qden,planes=planes,
              active=[meta[i] for i in active],numerical_lower=res.fun-cap*L0,certified=False)
    out=Path(candidate).with_name(Path(candidate).stem+'_dual_input.json');out.write_text(json.dumps(data))
    print('numerical input saved',out,flush=True)
    verify(out)

def verify(path):
    start=time.time();data=json.loads(Path(path).read_text());d=Q(data['d']);m=data['m'];B=basis(m,m);n=len(B);pi=arb.pi();da=A(d);lam=2*da-1
    conv=conversion(float(d),B,True);P=primes(data['N']);cap=arb('0.08382');L0=A(Q(data['L0']))
    def transform(row):return [sum((row[i]*A(conv[i][j]) for i in range(n)),arb(0)) for j in range(n)]
    # Li_0,...,Li_{-(m-1)} as exact rational functions.
    polys=[];coeff=[0,1]
    for r in range(m):
        polys.append(acb_poly(coeff))
        derivative=[(i+1)*coeff[i+1] for i in range(len(coeff)-1)]
        new=[0]*(len(coeff)+1)
        for i,z in enumerate(derivative):new[i+1]+=z;new[i+2]-=z
        for i,z in enumerate(coeff):new[i+1]+=(r+1)*z
        coeff=new
    phase_cache={}
    def phaseplane(idx):
        if idx in phase_cache:return phase_cache[idx]
        qs=data['planes'][idx];assert len(qs)==len(P)
        moments=[acb(0) for _ in range(m)];constant=arb(0)
        for p,q in zip(P,qs):
            pp=arb(int(p));lp=pp.log();xx=2*pi*A(Q(q,data['qden']));unit=acb(xx.cos(),xx.sin())
            z=(-A(d+Q(1,2))*lp).exp()*unit;zd=(-A(2*d+Q(1,2))*lp).exp()*unit
            constant+=(-(1-zd).log().imag+2*(1-z).log().imag)/pi
            den=1-z;dpow=acb(1);lpow=arb(1)
            for r in range(m):
                dpow*=den;lpow*=lp
                moments[r]+=lpow/math.factorial(r)*polys[r](z)/dpow
        row=[]
        for kind,j in B:row.append(-(moments[j-1].real if kind=='R' else moments[j-1].imag)/pi)
        result=([-x for x in transform(row)]+[arb(1)],constant);phase_cache[idx]=result;return result
    rows=[];rhs=[]
    for kind,x in data['active']:
        if kind=='phase':row,r=phaseplane(int(x))
        elif kind=='cap':row=[-A(v) for v in conv[0]]+[arb(0)];r=-2*pi*cap
        elif kind=='tail':row=[2*da*A(conv[0][j])-2*A(conv[1][j]) for j in range(n)]+[arb(0)];r=arb(0)
        elif kind=='box':raise RuntimeError('artificial box active: no certificate')
        else:
            xx=A(Q(x));b=arb(1)/2 if kind=='t' else xx;t=xx if kind=='t' else arb(0)
            row=[]
            for kk,j in B:
                off=1 if kk=='R' else 2;v=sum((z**(-off)*(1-lam/z)**(j-off) for z in [acb(da+b,t),acb(da-b,t)]),acb(0))
                row.append(v.real if kk=='R' else -v.imag)
            scale=1+t*t;row=[v*scale for v in row]+[arb(0)]
            r=(pi if kind=='b' else (pi if Q(x)>0 else -pi)-2*(t/(da+b)).atan()-2*(t/(da-b)).atan()+(t/(2*da+b)).atan()+(t/(2*da-b)).atan())*scale
        rows.append(row);rhs.append(r)
    assert len(rows)==n+1
    # Exact elementary upper side evaluated at T=exp(L0). This makes the
    # certificate a lower bound on the true single-kernel uniform objective,
    # without claiming a lower bound for arbitrary envelopes.
    T=L0.exp();s1=acb(da+arb(1)/2,T);s2=acb(2*da+arb(1)/2,T)
    def ael(s):return s.log().imag+(s-1).log().imag-T*pi.log()/2+(s/2).lgamma().imag
    theta=acb(arb(1)/4,T/2).lgamma().imag-T*pi.log()/2
    constant=(2*ael(s1)-ael(s2)-theta)/pi-1-cap*L0
    elementary=[]
    for kind,j in B:
        if j==1:D=1/s1+1/(s1-1)-pi.log()/2+(s1/2).polygamma(0)/2
        else:D=s1**(-j)+(s1-1)**(-j)+arb((-1)**(j-1))/math.factorial(j-1)/2**j*(s1/2).polygamma(j-1)
        elementary.append((D.real if kind=='R' else -D.imag)/pi)
    mat=arb_mat(rows).transpose();obj=arb_mat([[x] for x in transform(elementary)]+[[arb(1)]])
    multipliers=mat.solve(obj)
    assert all(multipliers[j,0]>0 for j in range(n+1)), 'dual multiplier positivity failed'
    lower=sum((multipliers[j,0]*rhs[j] for j in range(n+1)),arb(0))+constant
    result=dict(certified=True,C_lower=down_str(lower,22),family=dict(d=data['d'],m=m,L0=data['L0']),
                objective='true single-kernel uniform objective, relaxed at T=exp(L0); not arbitrary envelope optimum',N=data['N'],
                input_sha256=sha256(path),code_sha256=sha256(__file__),seconds=time.time()-start,
                dual_multipliers=[dict(lower=down_str(multipliers[j,0],22),upper=up_str(multipliers[j,0],22)) for j in range(n+1)])
    Path(path).with_name(Path(path).stem.replace('_input','')+'_certificate.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('candidate');ap.add_argument('--N',type=int,default=10000);ap.add_argument('--iterations',type=int,default=12);ap.add_argument('--verify',action='store_true');a=ap.parse_args()
    if a.verify:verify(a.candidate)
    else:run(a.candidate,a.N,a.iterations)
