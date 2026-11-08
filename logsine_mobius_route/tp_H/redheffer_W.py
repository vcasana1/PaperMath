# K mu = W(X) e_1 exactly (lcm-Moebius), hence W(X) = 1/(K^{-1})_{11} = det K / det K^{(1)}
import numpy as np, math
exec(open('lcm_form.py').read().split('for X in [300.5')[0])
for X in [300.5, 1000.5, 2500.5]:
    N=int(X); mu=mobius_upto(N)
    D=np.array([d for d in range(1,N+1) if mu[d]!=0]); v=mu[D].astype(float)
    g=np.gcd.outer(D,D); L=(D[:,None]*D[None,:])//g
    K=np.where(L<=X, L*Cl2(2*np.pi*np.mod(X/np.maximum(L,1),1.0)), 0.0)
    Kv=K@v; W=Kv[0]
    s1,ld=np.linalg.slogdet(K); s2,ld1=np.linalg.slogdet(K[1:,1:])
    inv11=np.linalg.solve(K,np.eye(len(D))[:,0])[0]
    print(f"X={X}: W={W:.6f}  max|(K mu)_d|, d>1 = {np.max(np.abs(Kv[1:])):.2e}  1/(K^-1)_11={1/inv11:.6f}  detK/detK1={s1*s2*math.exp(ld-ld1):.6f}  cond={np.linalg.cond(K):.2e}")
print("--- Schur form W = k(1) - b^T (K1)^{-1} b, inertia of K1 ---")
for X in [300.5, 1000.5, 2500.5]:
    N=int(X); mu=mobius_upto(N)
    D=np.array([d for d in range(1,N+1) if mu[d]!=0])
    g=np.gcd.outer(D,D); L=(D[:,None]*D[None,:])//g
    K=np.where(L<=X, L*Cl2(2*np.pi*np.mod(X/np.maximum(L,1),1.0)), 0.0)
    K1=K[1:,1:]; b=K[1:,0]; lam,U=np.linalg.eigh(K1); c=U.T@b
    q=c**2/lam; Pos=np.sum(q[lam>0]); Neg=np.sum(q[lam<0])
    print(f"X={X}: k(1)={K[0,0]:.4f}  W={K[0,0]-np.sum(q):.4f}  #pos={np.sum(lam>0)} #neg={np.sum(lam<0)}  sum_pos={Pos:.4e} sum_neg={Neg:.4e}")
