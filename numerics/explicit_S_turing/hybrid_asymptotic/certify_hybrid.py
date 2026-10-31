# Certification (Arb ball arithmetic, python-flint) of the kernel inequality
#   f(b,t,d) <= sum_j c_j [F_j(d+b,t)+F_j(d-b,t)] + sum_k kappa_k W_k(b,t)    for 0<=b<=1/2, t != 0,
# with f(b,t,d)=2atan((b+d)/t)+2atan((d-b)/t)-atan((b+2d)/t)-atan((2d-b)/t),
# F_Rj=Re (x+it)^(-j), F_Ij=-Im (x+it)^(-j), W_k=log^+(R_k/sqrt((c_k-1/2-b)^2+(t+v_k)^2)),
# and of the value C = c_R1/(2pi) + sum_k kappa_k J_k/pi, J_k=(1/pi) int_0^pi e(c_k+R_k cos th) dth.
import sys, json, time
from fractions import Fraction as Fr
from flint import arb, acb, ctx
ctx.prec = 256
def A(q): return arb(q.numerator)/q.denominator if isinstance(q,Fr) else arb(q)
def box(lo,hi): return A(lo).union(A(hi))           # lo,hi Fractions (dyadic) -> ball containing [lo,hi]

sol=json.load(open(sys.argv[1])); T1=Fr(sys.argv[2]) if len(sys.argv)>2 else Fr(40)
d=Fr(sol['d']).limit_denominator(10**6); B=[tuple(x) for x in sol['B']]
c=[Fr(x) for x in sol['c']]                                    # exact binary values of the LP coefficients
discs=[(Fr(cc).limit_denominator(10**4),Fr(R).limit_denominator(10**4),Fr(v).limit_denominator(10**4)) for cc,R,v in sol['discs']]
discs=[(cc,min(R,cc-Fr(1,2)),v) for cc,R,v in discs]   # rational rounding must keep c-R >= 1/2 (shrinking R only lowers W)
kap=[Fr(x) for x in sol['kappa']]
assert all(k>=0 for k in kap) and all(cc-R>=Fr(1,2) and cc>1 for cc,R,v in discs)
dA=A(d); half=A(Fr(1,2)); PI=arb.pi()
cA=[A(x) for x in c]; kA=[A(x) for x in kap]; dsA=[(A(cc),A(R).log(),A(v)) for cc,R,v in discs]

def kernel(b,t):
    U=arb(0)
    for x in (dA+b, dA-b):
        w=acb(1)/acb(x,t); p=acb(1)
        for i,(k,j) in enumerate(B):
            pass
        pw=[acb(1)]
        for j in range(1,max(jj for _,jj in B)+1): pw.append(pw[-1]*w)
        for i,(k,j) in enumerate(B):
            U+= cA[i]*(pw[j].real if k=='R' else -pw[j].imag)
    return U
def fbox(b,t,sgn):
    # valid on the closure of t>0 (sgn=+1) or t<0 (sgn=-1)
    return sgn*PI-2*(t/(dA+b)).atan()-2*(t/(dA-b)).atan()+(t/(2*dA+b)).atan()+(t/(2*dA-b)).atan()
def Wlow(b,t):
    s=arb(0)
    for (cc,lR,v),k in zip(dsA,kA):
        if k==0: continue
        val=lR-((cc-half-b)**2+(t+v)**2).log()/2
        lo=val.lower()
        if lo>0: s+=k*lo
    return s

JMAX=max(jj for _,jj in B)
def grad(b,t):
    # partial derivatives of U-f in b and t, evaluated on a box (balls b,t)
    gb=arb(0); gt=arb(0)
    for x,sg in ((dA+b,1),(dA-b,-1)):
        w=acb(1)/acb(x,t); pw=[acb(1)]
        for j in range(1,JMAX+2): pw.append(pw[-1]*w)
        for i,(k,j) in enumerate(B):
            dx=-j*pw[j+1]; dt=acb(0,-j)*pw[j+1]
            if k=='R': gb+=cA[i]*sg*dx.real; gt+=cA[i]*dt.real
            else: gb-=cA[i]*sg*dx.imag; gt-=cA[i]*dt.imag
    y1=dA+b; y2=dA-b; y3=2*dA+b; y4=2*dA-b; t2=t*t
    ft=-2*y1/(y1*y1+t2)-2*y2/(y2*y2+t2)+y3/(y3*y3+t2)+y4/(y4*y4+t2)
    fb=2*t/(y1*y1+t2)-2*t/(y2*y2+t2)-t/(y3*y3+t2)+t/(y4*y4+t2)
    return gb-fb, gt-ft
def Hcentered(b0,b1,t0,t1,sgn):
    bm=(b0+b1)/2; tm=(t0+t1)/2; b=box(b0,b1); t=box(t0,t1)
    H0=kernel(A(bm),A(tm))-fbox(A(bm),A(tm),sgn)
    gb,gt=grad(b,t)
    H=H0+gb*box(-(b1-b0)/2,(b1-b0)/2)+gt*box(-(t1-t0)/2,(t1-t0)/2)
    return H+Wlow(b,t)
def cert_main(blo,bhi,tlo,thi,sgn,maxdepth=60):
    stack=[(blo,bhi,tlo,thi,0)]; n=0; worst=None
    while stack:
        b0,b1,t0,t1,dep=stack.pop(); n+=1
        b=box(b0,b1); t=box(t0,t1)
        H=Hcentered(b0,b1,t0,t1,sgn)
        if H>0: continue
        if dep>=maxdepth: raise RuntimeError('fail at b=[%s,%s] t=[%s,%s] H=%s'%(float(b0),float(b1),float(t0),float(t1),H))
        wb=(b1-b0)/Fr(1,20); tm=max(abs(t0),abs(t1)); wt=(t1-t0)/max(Fr(1,20),tm*Fr(3,10))
        if wb>=wt: m_=(b0+b1)/2; stack+= [(b0,m_,t0,t1,dep+1),(m_,b1,t0,t1,dep+1)]
        else: m_=(t0+t1)/2; stack+= [(b0,b1,t0,m_,dep+1),(b0,b1,m_,t1,dep+1)]
    return n

# tail |t|>=T1, u=1/t: t^2 (U - f) >= t^2 U - 4d^3 u - K|u|^3, with t^2 U = sum c_j [Phi_j(d+b,u)+Phi_j(d-b,u)],
# Phi_R1 = x/(1+x^2u^2), Phi_j = Re/-Im of u^(j-2) (xu+i)^(-j) for j>=2;  K = (1/5) sum |alpha_i| y_i^5 with y_i<=2d+1/2.
def tailval(b,u):
    V=arb(0)
    for x in (dA+b, dA-b):
        for i,(k,j) in enumerate(B):
            if j==1:
                assert k=='R'; V+=cA[i]*x/(1+x*x*u*u)
            else:
                z=acb(u)**(j-2)*(acb(1)/acb(x*u,1))**j
                V+=cA[i]*(z.real if k=='R' else -z.imag)
    return V
ymax=2*dA+half; K=(2*(dA+half)**5+2*dA**5+ymax**5+(2*dA)**5)/5   # sum |alpha_i| y_i^5 /5, y_i in {b+d,d-b,b+2d,2d-b}, |b|<=1/2 (crude upper bound)
def cert_tail(u0,u1,maxdepth=40):
    assert u1*(2*d+Fr(1,2))<=1
    stack=[(Fr(0),Fr(1,2),u0,u1,0)]; n=0
    while stack:
        b0,b1,a0,a1,dep=stack.pop(); n+=1
        b=box(b0,b1); u=box(a0,a1)
        H=tailval(b,u)-4*dA**3*u-K*abs(u)**3
        if H>0: continue
        if dep>=maxdepth: raise RuntimeError('tail fail b=[%s,%s] u=[%s,%s] H=%s'%(float(b0),float(b1),float(a0),float(a1),H))
        if (b1-b0)*8>=(a1-a0)*T1: m_=(b0+b1)/2; stack+=[(b0,m_,a0,a1,dep+1),(m_,b1,a0,a1,dep+1)]
        else: m_=(a0+a1)/2; stack+=[(b0,b1,a0,m_,dep+1),(b0,b1,m_,a1,dep+1)]
    return n

def Jexact(nodes,cc,R):
    # (1/pi) int_0^pi e(cc+R cos th) dth for e piecewise linear through nodes, e=0 for sigma>=1, cc-R>=1/2
    tot=arb(0); ccA=A(cc); RA=A(R)
    lo,hi=cc-R,min(cc+R,Fr(1))
    for (p,ep),(q,eq) in zip(nodes,nodes[1:]):
        a,bq=max(p,lo),min(q,hi)
        if a>=bq: continue
        Bs=(eq-ep)/(q-p); As=ep-Bs*p
        tha=A((a-cc)/R).acos(); thb=A((bq-cc)/R).acos()      # tha>=thb
        tot+= (A(As)+A(Bs)*ccA)*(tha-thb)+A(Bs)*RA*(tha.sin()-thb.sin())
    return tot/PI
def nodes_of(p):
    k,l=Fr(13,84),Fr(55,84); nodes=[]
    if p=='T':   # ANTEDB Table 6.2 (Tao-Trudgian-Yang) + Heath-Brown nodes, see profile_tty.py
        from profile_tty import nodes_tty
        return nodes_tty()
    if p=='P':   # published-source nodes only (lower convex hull), see profile_published.py
        from profile_published import nodes_published
        return nodes_published()
    if p=='B':
        for _ in range(8):
            nodes.append((l-k,k)); k,l=k/(2*k+2),Fr(1,2)+l/(2*k+2)
        nodes.append((Fr(1),Fr(0)))
    else:
        nodes=[(Fr(1,2),Fr(27,164))]+[(1-Fr(m,2**m-2),Fr(1,2**m-2)) for m in range(4,10)]+[(Fr(1),Fr(0))]
    return nodes

if __name__=='__main__':
    t_=time.time()
    nodes=nodes_of(sol['prof'])
    J=[Jexact(nodes,cc,R) for cc,R,v in discs]
    C=cA[0]/(2*PI)+sum((k*j for k,j in zip(kA,J)),arb(0))/PI
    print('d =',d,' m =',max(j for _,j in B),' profile',sol['prof'],' discs used:',len(discs))
    print('C = c_R1/(2pi) + sum kappa_k J_k/pi =',C.str(20,radius=False),' (ball',C.str(5),')')
    print('kernel part c_R1/(2pi) =',(cA[0]/(2*PI)).str(12,radius=False))
    lim=2*dA*cA[B.index(('R',1))]-2*cA[B.index(('R',2))]; print('limit t^2 U at |t|->inf =',lim.str(10), lim>0)
    n1=cert_main(Fr(0),Fr(1,2),Fr(0),T1,+1); print('t in (0,T1]: certified, boxes',n1,flush=True)
    n2=cert_main(Fr(0),Fr(1,2),-T1,Fr(0),-1); print('t in [-T1,0): certified, boxes',n2,flush=True)
    assert all(abs(v)+R<=T1 for cc,R,v in discs)    # W_k = 0 for |t|>=T1
    n3=cert_tail(Fr(0),1/T1); n4=cert_tail(-1/T1,Fr(0)); print('|t|>=T1: certified, boxes',n3+n4)
    print('all certified;  C <',C.upper().str(12,radius=False),'  time %.0fs'%(time.time()-t_))
