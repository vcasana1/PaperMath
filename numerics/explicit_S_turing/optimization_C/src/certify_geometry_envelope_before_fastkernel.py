"""Assemble an unconditional uniform bound from executed Green--Jensen proofs.
For L>=L0>=10, the disc/rectangle cost per weight is at most
(J*L+G*log L+A+G*pi^2/(8*L^2)+400*exp(-L))/pi.
All constants below are evaluated with Arb and directed rounding.
"""
import sys,json,math,argparse
from pathlib import Path
from fractions import Fraction as Q
from flint import arb,ctx
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE.parent/'hybrid_asymptotic'))
from certutil import A,up_str,down_str,sha256
def certify(path,arithmetic,L0='100',low='inputs/low_L60.json',lowarith='inputs/low_L60_arithmetic_N1000000.json',lowelem='inputs/low_L60_elemS.json',PL=None):
    ctx.prec=512;s=json.loads(Path(path).read_text());ar=json.loads(Path(arithmetic).read_text());cp=Path(path).with_name(Path(path).stem+'_geometry_costs.json');kp=Path(path).with_name(Path(path).stem+'_geometry_kernel.json')
    co=json.loads(cp.read_text());ke=json.loads(kp.read_text());pl=Path(PL) if PL else BASE/'certificates/geometry_PL_inputs.json';pr=json.loads(pl.read_text())
    assert ar['certified'] and co['certified'] and ke['certified'] and pr['certified']
    assert ar['input_sha256']==co['input_sha256']==ke['input_sha256']==sha256(path)
    assert ke['interface_coordinates']=='constructed independently in exact rational arithmetic'
    assert co['PL_certificate_sha256']==sha256(pl) and pr['code_sha256']==sha256(BASE/'src/certify_pl_inputs.py')
    assert co['code_sha256']==sha256(BASE/'src/certify_geometry_costs.py') and ke['code_sha256']==sha256(BASE/'src/certify_geometry_kernel.py')
    pi=arb.pi();d=A(Q(s['d']));c=[A(Q(x)) for x in s['c']];B=s['B'];kap=[A(Q(x)) for x in s['geometry_weights']];assert all(k>=0 for k in kap)
    assert len(co['geometries'])==len(kap)==len(s['geometries'])
    for g,r in zip(s['geometries'],co['geometries']):
        assert {k:v for k,v in g.items() if k!='cost'}==r['geometry']
        extent=Q(str(g['H'] if g['kind']=='rectangle' else g['R']));right=Q(str(g['b'])) if g['kind']=='rectangle' else Q(str(g['c']))+Q(str(g['R']))
        assert extent+abs(Q(str(g['v'])))<=10 and right+3<=10
    Ak=c[0]/(2*pi);At=Ak+sum((k*arb(r['J_upper'])/pi for k,r in zip(kap,co['geometries'])),arb(0));Bc=sum((k*arb(r['G_upper'])/pi for k,r in zip(kap,co['geometries'])),arb(0));fee=sum((k*arb(r['A_upper'])/pi for k,r in zip(kap,co['geometries'])),arb(0))
    coupled=ar.get('centre_mode')=='joint_prime_phase'
    arithprog='certify_arithmetic_binned.py'
    if coupled:
        approved={sha256(BASE/'src'/q):q for q in ['certify_arithmetic_coupled.py','certify_arithmetic_coupled_fast.py']}
        assert ar['code_sha256'] in approved
        arithprog=approved[ar['code_sha256']]
        # A_upper includes the separately bounded centre term. The exact
        # centre Euler series is now part of the coupled prime polynomial.
        # Subtract a LOWER endpoint, keeping a rigorous upper boundary fee.
        for g,k in zip(s['geometries'],kap):
            cc=A(Q(str(g['c'])));centre=cc.zeta().log()-(2*cc).zeta().log();fee-=k*centre.lower()/pi
    delta=arb('.08382')-At;assert delta>0 and Bc>0;peak=Bc/delta
    lp,la,le=[Path(x) for x in [low,lowarith,lowelem]];ls,lac,lec=[json.loads(p.read_text()) for p in [lp,la,le]]
    if L0=='auto':
        rough=arb(ar['Czeta_upper'])-Ak*(2*pi).log()+fee+Bc*(peak.log()-1)
        trial=(rough-arb(lac['Czeta_upper'])-arb(lec['Fsup_upper']))/(arb(lec['A1'])-arb('.08382'))
        choice=max(10.,min(float(trial),float(peak)))
        L0=format(math.floor(choice*10**6)/10**6,'.6f')
    L=A(Q(L0));assert L>=10;T=L.exp();assert T>20 and 110/(T*L)<1
    height=Bc*(peak.log()-1)
    if peak<L:height=-delta*L+Bc*L.log()
    s1=arb(1)/2+d;s2=arb(1)/2+2*d
    K=(4*d+s1*s1/2+s2*(s2-1)/2+1+s2*s2/2+s1*(s1-1))/pi
    K+=abs(c[0])/pi*((2*s1-1)+s1*s1/4+arb(8)/3)/T
    for (kind,j),cc in zip(B,c):
        if j==1:continue
        kk=j-1;ps=arb(math.factorial(kk-1))*(2/T)**kk+arb(math.factorial(kk))*(2/T)**(kk+1)/2+arb(math.factorial(kk+1))*(4/(3*T))*(4/T)**(kk+1)
        K+=abs(cc)/pi*(2/T**j+ps/(math.factorial(j-1)*2**j))*T
    K+=(arb(1)/16+arb(1)/8+arb(1)/3)/pi
    correction=Bc*pi*pi/(8*L*L)+(K+400*sum(kap,arb(0))/pi)/T
    high=arb(ar['Czeta_upper'])-Ak*(2*pi).log()+fee+height+correction
    lk=lp.with_name(lp.stem+'_kernel.json');lkr=json.loads(lk.read_text())
    assert lkr['certified'] and lac['certified'] and lkr['input_sha256']==lac['input_sha256']==sha256(lp)
    assert lec['mode']=='S' and lec['certified'] and lec['input_sha256']==sha256(lp)
    lowbound=arb(lac['Czeta_upper'])+arb(lec['Fsup_upper'])+(arb(lec['A1'])-arb('.08382'))*L
    value=max(high.upper(),lowbound.upper());paths=[Path(path),Path(arithmetic),cp,kp,pl,lp,la,le,lk,Path(__file__),BASE/'src'/arithprog]
    out=dict(certified=True,bound_type='Green_Jensen_uniform',A='0.08382',C_upper=up_str(value,10),domain='T>1',Lswitch=L0,
        high_upper=up_str(high,25),low_upper=up_str(lowbound,25),kernel_A_upper=up_str(Ak,25),A_total_upper=up_str(At,25),slope_slack_lower=down_str(delta,25),
        B_loglog_upper=up_str(Bc,25),constant_geometry_fee_upper=up_str(fee,25),peak_logT_lower=down_str(peak,25),peak_logT_upper=up_str(peak,25),
        elementary_and_height_correction_upper=up_str(correction,25),geometries=len(kap),rectangles=sum(g['kind']=='rectangle' for g in s['geometries']),
        coupled_centres=coupled,arithmetic_verifier=arithprog,convention='right continuous S at zeros; also valid at midpoint and left limit',
        proof='v11 exact identity plus piecewise-harmonic Green majorant; explicit Phragmen-Lindelof and Euler-product boundary costs; analytic supremum in log T; low kernel covers the complete finite interval',
        hashes={str(p):sha256(p) for p in paths})
    dest=Path(path).with_name(Path(path).stem+('_joint_geometry_envelope.json' if coupled else '_geometry_envelope.json'));dest.write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('candidate');p.add_argument('arithmetic');p.add_argument('--Lswitch',default='100');p.add_argument('--low',default='inputs/low_L60.json');p.add_argument('--low-arithmetic',default='inputs/low_L60_arithmetic_N1000000.json');p.add_argument('--low-elementary',default='inputs/low_L60_elemS.json');p.add_argument('--PL');a=p.parse_args();certify(a.candidate,a.arithmetic,a.Lswitch,a.low,a.low_arithmetic,a.low_elementary,a.PL)
