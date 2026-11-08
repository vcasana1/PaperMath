import numpy as np, math
exec(open('bilinear_W.py').read().split('print("c_G')[0])
# (i) E_G'(Y) = -2 pi R(Y),  R(Y) = sum_{l<=Y} log|2 sin(pi Y/l)| - (log2 - C) Y
def R(Y):
    l=np.arange(1,int(Y)+1,dtype=float); return np.sum(np.log(np.abs(2*np.sin(np.pi*Y/l))))-(math.log(2)-C)*Y
for Y in [37.3, 512.77, 4096.41]:
    h=1e-5; dE=((Gs(Y+h)-cG*(Y+h)**2)-(Gs(Y-h)-cG*(Y-h)**2))/(2*h)
    print(f"Y={Y}: E_G'(Y) numeric={dE:.6f}   -2 pi R(Y)={-2*math.pi*R(Y):.6f}")
# (ii) parity split of the corner (Y=X/(dj)<=64), d,j<=sqrt X squarefree; sign = (-1)^{omega(d)+omega(j)}
X=120000.5; u=math.sqrt(X); U=int(u)
om=np.zeros(U+1,dtype=int)
for p in range(2,U+1):
    if all(p%q for q in range(2,int(p**0.5)+1)): om[p::p]+=1
sq=np.array([d for d in range(1,U+1) if mu[d]!=0])
Se=So=0.0; Ae=Ao=0.0
for d in sq:
    js=sq[sq*d<=X]
    for j in js:
        Y=X/(d*j)
        if Y>64: continue
        val=d*j*(Gs(Y)-cG*Y*Y)
        if (om[d]+om[j])%2==0: Se+=val; Ae+=abs(val)
        else: So+=val; Ao+=abs(val)
print(f"X={X}: corner (Y<=64): S_even={Se:.4e}  S_odd={So:.4e}  S_even-S_odd={Se-So:.4e}   sum|.| even={Ae:.3e} odd={Ao:.3e}   X^1.5={X**1.5:.3e} X^2={X**2:.3e}")
