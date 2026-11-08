# One-sided (positive-part) test of the corner after Abel summation in n = dj:
#   C(X) = A_U(N_X) g(N_X) - sum_{U<n<N_X} A_U(n) b_X(n),  g(n) = n E_G(X/n),  b_X(n) = g(n+1) - g(n),
#   A_U(t) = sum_{U<n<=t} a_U(n),  a_U(n) = sum_{dj=n, d,j<=U} mu(d) mu(j),  U = sqrt X.
# Compares sum [A_U b_X]_+ , sum |A_U b_X| and sum |a_U(n) n E_G(X/n)| (termwise), in units of X^{3/2}.
import numpy as np, math
exec(open('bilinear_W.py').read().split('print("c_G')[0])
for X in [30000.5, 120000.5, 380000.5]:
    U=int(math.sqrt(X)); NX=int(X)
    sq=np.array([d for d in range(1,U+1) if mu[d]!=0])
    aU=np.zeros(NX+2)
    for d in sq:
        js=sq[sq*d<=X]
        np.add.at(aU, d*js, mu[d]*mu[js])
    n=np.arange(U+1,NX+1)
    g=np.array([k*(Gs(X/k)-cG*(X/k)**2) for k in n])
    C_direct=np.sum(aU[n]*g)
    A=np.cumsum(aU[n])                      # A_U(n) for n=U+1..NX
    b=g[1:]-g[:-1]                          # b_X(n), n=U+1..NX-1
    prod=A[:-1]*b
    C_abel=A[-1]*g[-1]-np.sum(prod)
    s=X**1.5
    print(f"X={X}: C={C_direct/s:+.4f} (Abel {C_abel/s:+.4f})  border={A[-1]*g[-1]/s:+.4f}  "
          f"sum[A b]_+={np.sum(prod[prod>0])/s:.2f}  sum|A b|={np.sum(np.abs(prod))/s:.2f}  "
          f"termwise sum|a_U n E_G|={np.sum(np.abs(aU[n]*g))/s:.2f}  max|A_U|/X^0.5={np.max(np.abs(A))/X**0.5:.3f}  [X^1.5 units]")
