import mpmath as mp
mp.mp.dps=25
def A(s): return mp.log(2*mp.pi)/s+1/s**2+mp.nsum(lambda k: mp.zeta(2*k)/(k*(2*k-s)),[1,mp.inf])
def Ad(s):  # digamma closed form
    return (mp.log(mp.pi)-mp.euler-mp.digamma(1-s/2)+1/s+2*mp.nsum(lambda k:(mp.zeta(2*k)-1)/(2*k-s),[1,mp.inf]))/s
for s in [mp.mpc(0.5,14.134725), mp.mpc(0.3,3), mp.mpc(0.9,40)]:
    print("closed-form check",mp.nstr(A(s)-Ad(s),3))
# argument principle for s*A(s) on box 0.01<=sigma<=0.99, 0.5<=t<=T
def f(s): return s*s*Ad(s)
def winding(T, n=1200):
    pts=[mp.mpc(0.01,0.5),mp.mpc(0.99,0.5),mp.mpc(0.99,T),mp.mpc(0.01,T),mp.mpc(0.01,0.5)]
    tot=0; prev=mp.arg(f(pts[0]))
    for a,b in zip(pts[:-1],pts[1:]):
        for j in range(1,n+1):
            z=a+(b-a)*j/n; cur=mp.arg(f(z)); dlt=cur-prev
            while dlt>mp.pi: dlt-=2*mp.pi
            while dlt<-mp.pi: dlt+=2*mp.pi
            tot+=dlt; prev=cur
    return tot/(2*mp.pi)
for T in [30,100]:
    print("zeros of s^2 A(s) in 0<sigma<1, 0.5<t<",T,":",mp.nstr(winding(T),4))
# also near real axis segment 0<t<0.5 small box
def wind_small():
    pts=[mp.mpc(0.01,-0.5),mp.mpc(0.99,-0.5),mp.mpc(0.99,0.5),mp.mpc(0.01,0.5),mp.mpc(0.01,-0.5)]
    tot=0; prev=mp.arg(f(pts[0])); n=800
    for a,b in zip(pts[:-1],pts[1:]):
        for j in range(1,n+1):
            z=a+(b-a)*j/n; cur=mp.arg(f(z)); dlt=cur-prev
            while dlt>mp.pi: dlt-=2*mp.pi
            while dlt<-mp.pi: dlt+=2*mp.pi
            tot+=dlt; prev=cur
    return tot/(2*mp.pi)
print("zeros in |t|<0.5 box:",mp.nstr(wind_small(),4))
