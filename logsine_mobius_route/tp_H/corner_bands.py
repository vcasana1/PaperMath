# Corner C(X) (d,j<=sqrt X, dj>sqrt X) split into dyadic Y-bands, Y = X/(dj) in [2^k, 2^{k+1})
import numpy as np, math
exec(open('bilinear_W.py').read().split('print("c_G')[0])
for X in [30000.5,120000.5,380000.5]:
    U=int(math.sqrt(X)); sq=np.array([d for d in range(1,U+1) if mu[d]!=0])
    nb=int(math.log2(math.sqrt(X)))+1; S=np.zeros(nb); A=np.zeros(nb)
    for d in sq:
        for j in sq[sq*d<=X]:
            if d*j<=math.sqrt(X): continue
            Y=X/(d*j); k=int(math.log2(Y)); v=mu[d]*mu[j]*d*j*(Gs(Y)-cG*Y*Y)
            S[k]+=v; A[k]+=abs(v)
    s=X**1.5
    print(f"X={X}: -C/X^1.5={-S.sum()/s:+.4f}")
    print("   band  [2^k,2^k+1):  " + "  ".join(f"k{k}:{-S[k]/s:+.3f}({A[k]/s:.1f})" for k in range(nb)))
