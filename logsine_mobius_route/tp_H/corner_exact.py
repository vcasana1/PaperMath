# Exact reduction (unconditional):  W = 2W_u - a X^2 m(u)^2 - Corner - Rest,  u = sqrt X, a = pi(C - log 2)
#   Corner: d,j <= sqrt X, dj > sqrt X   (Y = X/(dj) < sqrt X)
#   Rest:   dj <= sqrt X, bounded by sum dj |E_G(X/dj)| << X^{3/2+eps} since E_G(Y) << Y^{1+eps} (Perron, abs. conv.)
import numpy as np, math
exec(open('bilinear_W.py').read().split('print("c_G')[0])
rng=np.random.default_rng(3)
Ys=np.concatenate([10**rng.uniform(1,5.3,4000)])
r=np.array([abs(Gs(Y)-cG*Y*Y)/Y**0.75 for Y in Ys])
print(f"E_G sup check: max|E_G(Y)|/Y^(3/4) over 4000 random Y in [10, 2e5] = {r.max():.3f}; max|E_G|/Y = {np.max([abs(Gs(Y)-cG*Y*Y)/Y for Y in Ys[:400]]):.3f}")
for X in [30000.5,120000.5,380000.5]:
    U=int(math.sqrt(X)); sq=np.array([d for d in range(1,U+1) if mu[d]!=0])
    Cor=Rest=RestAbs=CorAbs=0.0
    for d in sq:
        for j in sq[sq*d<=X]:
            Y=X/(d*j); v=mu[d]*mu[j]*d*j*(Gs(Y)-cG*Y*Y)
            if d*j>math.sqrt(X): Cor+=v; CorAbs+=abs(v)
            else: Rest+=v; RestAbs+=abs(v)
    mu_u=np.sum(mu[1:U+1]/np.arange(1,U+1)); W2u=2*Wfull(X,math.sqrt(X)); sqt=cG*X*X*mu_u**2; W=Wfull(X)
    s=X**1.5
    print(f"X={X}: W={W/s:+.4f} | 2W_u={W2u/s:+.4f}  -aX^2m^2={-sqt/s:+.4f}  -Rest={-Rest/s:+.4f} (sum|Rest|={RestAbs/s:.3f})  -Corner={-Cor/s:+.4f} (sum|Corner|={CorAbs/s:.1f})  [X^1.5 units] check={W2u-sqt-Cor-Rest-W:.1e}")
