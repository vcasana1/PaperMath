# Castor-Pollux I: numerics for the kernel transform H(s) = int_1^inf K({u}) u^{-s-3} du,
# K(x) = sum_m (1 - cos(2 pi m x))/m^3,  G(s) = -(s+1)(s+2) H(s)/(4 pi^2).  No external special function is used.
import numpy as np, math
M, N, L = 4000, 200, 65536
x = (np.arange(L) + 0.5)/L
KM = np.zeros(L)
for m0 in range(1, M+1, 200):                      # K_M at the midpoints, in chunks
    m = np.arange(m0, min(m0+200, M+1))[:, None]
    KM += ((1 - np.cos(2*np.pi*m*x[None, :]))/m**3).sum(axis=0)
print("min K_M =", KM.min(), " max K_M =", KM.max(), " mean K_M =", KM.mean())
def HMNL(s, deriv=0):
    tot = 0j
    for n in range(1, N+1):
        u = n + x
        tot += (KM*(-np.log(u))**deriv*u**(-s-3)).sum()/L
    return tot
B0, B1 = 2.5, math.pi**3/3; B2 = 4*math.pi**2*(1+math.log(M))
Z = lambda th: 1 + 1/(th-1)
def E0(s):
    sg = s.real
    return 1/((sg+2)*M**2) + B0/((sg+2)*(N+1)**(sg+2)) + (B2*Z(sg+3) + 2*abs(s+3)*B1*Z(sg+4) + abs((s+3)*(s+4))*B0*Z(sg+5))/(24*L**2)
def E1(s):
    sg = s.real; a = s+3
    return (1/(M**2*(sg+2)**2) + B0*(N+1)**(-sg-2)*(math.log(N+1)/(sg+2) + 1/(sg+2)**2)
            + (B2*Z(sg+2) + 2*B1*(Z(sg+4) + abs(a)*Z(sg+3)) + B0*(abs(a*(a+1))*Z(sg+4) + abs(2*a+1)*Z(sg+5)))/(24*L**2))
roots = [1.12731287366+15.0012634323j, 0.533572289782+21.763254707j, 0.89473080986+25.6248369206j,
         0.227688020607+30.9759627227j, 0.950506780068+33.5990875454j, 0.430899873563+38.0548862104j]
for rho in (1e-4, 1e-2):
  print("\nRouche test, radius rho =", rho, " (M,N,L) =", (M,N,L))
  for i, s0 in enumerate(roots, 1):
    e0, e1 = HMNL(s0), HMNL(s0, 1)
    lhs = abs(e0) + E0(s0) + rho*E1(s0) + rho**2*B0/(s0.real - rho + 2)**3
    print(f" {i}: s0 = {s0:.9f}  |eta0| = {abs(e0):.3e}  |eta1| = {abs(e1):.8f}  E0 = {E0(s0):.3e}  E1 = {E1(s0):.3e}"
          f"  left = {lhs:.3e}  right = {rho*abs(e1):.3e}  holds: {lhs < rho*abs(e1)}")
# variance V(1/2): moments with the tail u > N+1 replaced by the mean of K (Sigma_3)
S3 = sum(1/m**3 for m in range(1, 200000)) + 1/(2*200000.0**2)
def moment(sg, j):
    b = N+1.0; c = sg+2
    tail = {0: b**-c/c, 1: b**-c*(math.log(b)/c + 1/c**2), 2: b**-c*(math.log(b)**2/c + 2*math.log(b)/c**2 + 2/c**3)}[j]
    return (HMNL(sg+0j, j).real)*(-1)**j + S3*tail
h0, h1, h2 = moment(0.5, 0), moment(0.5, 1), moment(0.5, 2)
V = h2/h0 - (h1/h0)**2
print(f"\nSigma_3 = {S3:.12f}\nH(1/2) = {h0:.10f}  -H'(1/2) = {h1:.10f}  H''(1/2) = {h2:.10f}\nV(1/2) = {V:.7f}  sqrt(2/V) = {math.sqrt(2/V):.4f}")
print("G(1) = -(2)(3) H(1)/(4 pi^2) =", -6*moment(1.0, 0)/(4*math.pi**2), "  (log 2 - C = -0.0506476813)")
