import numpy as np, math
exec(open('bilinear_W.py').read().split('print("c_G')[0])
for X in [30000.5,120000.5,480000.5]:
    U=int(math.sqrt(X)); sq=np.array([d for d in range(1,U+1) if mu[d]!=0])
    Smu=S1=0.0
    for d in sq:
        js=sq[sq*d<=X]
        for j in js:
            Y=X/(d*j)
            if Y>64: continue
            val=d*j*(Gs(Y)-cG*Y*Y); Smu+=mu[d]*mu[j]*val; S1+=val
    print(f"X={X}: corner mu-signed={Smu:.4e} ({Smu/X**1.5:.3f} X^1.5)   corner chi=1 ={S1:.4e} ({S1/X**1.5:.3f} X^1.5, {S1/X**2:.5f} X^2)")
