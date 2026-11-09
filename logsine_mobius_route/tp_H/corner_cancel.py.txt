# Where does the cancellation in sum_n A_U(n) b_X(n) live?  T(n) = A_U(n) b_X(n), n in (U, X).
# (a) block sums of T over consecutive n of length L: sum_i |sum_{n in block i} T(n)| vs sum |T|;
# (b) coarse/fine split: sum_i A_U(n_i)[g(end_i)-g(n_i)]  +  sum_i sum_{n in i} (A_U(n)-A_U(n_i)) b_X(n);
# (c) dyadic bands in Y = X/n; (d) sign agreement of A_U and b_X.
import numpy as np, math
exec(open('bilinear_W.py').read().split('print("c_G')[0])
for X in [30000.5, 120000.5, 380000.5]:
    U=int(math.sqrt(X)); NX=int(X)
    sq=np.array([d for d in range(1,U+1) if mu[d]!=0])
    aU=np.zeros(NX+2)
    for d in sq:
        js=sq[sq*d<=X]; np.add.at(aU, d*js, mu[d]*mu[js])
    n=np.arange(U+1,NX+1); g=np.array([k*(Gs(X/k)-cG*(X/k)**2) for k in n])
    A=np.cumsum(aU[n]); b=g[1:]-g[:-1]; T=A[:-1]*b; s=X**1.5; m=len(T)
    print(f"X={X}: sum T={T.sum()/s:+.4f}  sum|T|={np.abs(T).sum()/s:.2f}  [X^1.5]  #n={m}")
    print("   (a) block length L -> sum_i |block sum| :", end="")
    for L in [1,4,16,64,256,1024,4096]:
        k=m//L; B=T[:k*L].reshape(k,L).sum(1); print(f" L={L}:{np.abs(B).sum()/s:.2f}", end="")
    print()
    print("   (b) coarse/fine, L -> (sum|coarse_i|, sum coarse, sum|fine_i|, sum fine):", end="")
    for L in [16,256,4096]:
        k=m//L; idx=np.arange(k)*L
        coarse=A[idx]*(g[idx+L]-g[idx])
        fine=np.array([np.sum((A[i:i+L]-A[i])*b[i:i+L]) for i in idx])
        print(f" L={L}:({np.abs(coarse).sum()/s:.2f},{coarse.sum()/s:+.3f},{np.abs(fine).sum()/s:.2f},{fine.sum()/s:+.3f})", end="")
    print()
    Y=X/n[:-1]; kb=np.floor(np.log2(Y)).astype(int)
    print("   (c) bands Y in [2^k,2^k+1): k -> (sum T, sum|T|, #n):", end="")
    for k in range(0,kb.max()+1):
        mk=kb==k; print(f" k{k}:({T[mk].sum()/s:+.3f},{np.abs(T[mk]).sum()/s:.2f},{mk.sum()})", end="")
    print()
    sA=np.sign(A[:-1]); sb=np.sign(b); same=np.mean(sA*sb>0)
    print(f"   (d) P(sign A_U = sign b_X)={same:.4f}   corr(A_U,b_X)={np.corrcoef(A[:-1],b)[0,1]:+.4f}   rms A_U/sqrt X={np.sqrt(np.mean(A**2))/X**0.5:.3f}   mean|b_X|/X={np.mean(np.abs(b))/X:.4f}")
