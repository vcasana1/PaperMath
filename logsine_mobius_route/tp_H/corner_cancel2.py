# Profile per dyadic band Y=X/n in [2^k,2^{k+1}): rms A_U / sqrt X, mean |b_X|, sum|T| ; and growth of sum|T| in X.
import numpy as np, math
exec(open('bilinear_W.py').read().split('print("c_G')[0])
for X in [30000.5, 120000.5, 380000.5]:
    U=int(math.sqrt(X)); NX=int(X)
    sq=np.array([d for d in range(1,U+1) if mu[d]!=0])
    aU=np.zeros(NX+2)
    for d in sq:
        js=sq[sq*d<=X]; np.add.at(aU, d*js, mu[d]*mu[js])
    n=np.arange(U+1,NX+1); g=np.array([k*(Gs(X/k)-cG*(X/k)**2) for k in n])
    A=np.cumsum(aU[n]); b=g[1:]-g[:-1]; T=A[:-1]*b; s=X**1.5
    Y=X/n[:-1]; kb=np.floor(np.log2(Y)).astype(int)
    print(f"X={X}: TV(g)/X={np.abs(b).sum()/X:.1f}  sum|T|/X^1.5={np.abs(T).sum()/s:.2f}  max|A_U|/sqrtX={np.abs(A).max()/X**.5:.3f}")
    print("   k: rmsA/sqrtX  mean|b|/sqrtX  sum|T|/X^1.5")
    for k in range(0,kb.max()+1):
        m=kb==k
        print(f"   {k}: {np.sqrt(np.mean(A[:-1][m]**2))/X**.5:.3f}  {np.mean(np.abs(b[m]))/X**.5:.3f}  {np.abs(T[m]).sum()/s:.2f}")
