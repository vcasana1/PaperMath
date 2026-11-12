"""Checks for Proposition prop:fourier of Cg_Thermal_Contrast_v4.

B_0 = int_0^1 log V(u) du, B_m = 2 int_0^1 log V(u) cos(2 pi m u) du, computed with the
midpoint rule on Q points u_j = (j + 1/2)/Q (which is the discrete Fourier transform of
the samples). For a compound Poisson distribution B_0 = log p0 and B_m = b_m.
Displaced thermal state: q = B_1 - sqrt(B_1^2 - 2 B_2), |xi|^2 = (B_1 - q)/(1 - q)^2.
"""
import numpy as np, sys
sys.path.insert(0, '.')
from lst_common import coherence_damped

def coeffs(logV_samples, M):
    J = len(logV_samples)
    u = (np.arange(J) + 0.5)/J
    B0 = logV_samples.mean()
    B = [2*np.mean(logV_samples*np.cos(2*np.pi*m*u)) for m in range(1, M+1)]
    return B0, np.array(B)

def recover(B1, B2):
    disc = B1**2 - 2*B2
    q = B1 - np.sqrt(max(disc, 0.0))
    return q, (B1 - q)/(1 - q)**2, disc

def logV_dt(u, q, x2):
    z = np.exp(-2j*np.pi*u)
    D = (1-q)/(1-q*z)*np.exp(-x2*(1-q)*(1-z)/(1-q*z))
    return np.log(np.abs(D))

print('1. Displaced thermal, exact contrast, midpoint rule with Q points')
print('   q      |xi|^2   Q    B0 - log p0     B1 - b1        B2 - b2        q_rec - q      |xi|^2_rec - |xi|^2')
for q in [1/3, 0.8]:
    for x2 in [0.0, 0.25, 1.0, 2.0]:
        for J in [8, 16, 64]:
            u = (np.arange(J) + 0.5)/J
            B0, B = coeffs(logV_dt(u, q, x2), 2)
            b1 = q + x2*(1-q)**2
            b2 = q**2/2 + x2*(1-q)**2*q
            p0 = (1-q)*np.exp(-x2*(1-q))
            qr, xr, _ = recover(B[0], B[1])
            print('   %.4f %5.2f  %3d  % .3e     % .3e     % .3e     % .3e     % .3e'
                  % (q, x2, J, B0-np.log(p0), B[0]-b1, B[1]-b2, qr-q, xr-x2))

print()
print('2. Identity B2 - q B1 = -q^2/2 and B1^2 - 2 B2 = |xi|^4 (1-q)^4 (symbolic check with random values)')
rng = np.random.default_rng(1)
err = 0.0
for _ in range(1000):
    q = rng.uniform(0, 0.99); x2 = rng.uniform(0, 5)
    b1 = q + x2*(1-q)**2; b2 = q**2/2 + x2*(1-q)**2*q
    err = max(err, abs(b2 - q*b1 + q**2/2), abs(b1**2 - 2*b2 - x2**2*(1-q)**4))
print('   max error', err)

print()
print('3. Distribution p0 = 2/3, p1 = 1/3 (not compound Poisson): B_m = (-1)^(m+1) 2^(-m)/m')
J = 256
u = (np.arange(J) + 0.5)/J
lv = np.log(np.abs(2/3 + np.exp(-2j*np.pi*u)/3))
B0, B = coeffs(lv, 4)
print('   B0 =', B0, ' log(2/3) =', np.log(2/3))
for m in range(1, 5):
    print('   B_%d = % .10f   formula % .10f' % (m, B[m-1], (-1)**(m+1)*2.0**(-m)/m))

print()
print('4. Thermal mode with damping (closed form, rho = kappa/(2 chi)), window 0 < u < 1, Q = 64')
print('   nbar   rho      q_rec - q      B1^2-2B2       |xi|^2_rec     B0 - log p0    max_u |V_k - V| on (0,1)   bound pi*Lambda*(kappa/chi)')
J = 64
u = (np.arange(J) + 0.5)/J
for nb in [0.1, 0.5, 2.0]:
    q = nb/(nb+1)
    Lam = 4*nb*(nb+1)
    for rho in [1e-4, 1e-3, 1e-2]:
        D = coherence_damped(u, nb, rho)
        V0 = 1/np.sqrt(1 + Lam*np.sin(np.pi*u)**2)
        B0, B = coeffs(np.log(np.abs(D)), 2)
        qr, xr, disc = recover(B[0], B[1])
        print('   %.2f  %.0e   % .3e     % .3e     % .3e     % .3e     %.3e                  %.3e'
              % (nb, rho, qr-q, disc, xr, B0-np.log(1-q), np.abs(np.abs(D)-V0).max(), np.pi*Lam*2*rho))

print()
print('5. Static detuning delta between probe and analysis pulses: D -> exp(-i delta t) D, V unchanged.')
print('   Fourier inversion of the complex D over 0<u<1 with an unknown detuning delta = 0.1*(2 chi):')
nb = 0.5; q = nb/(nb+1)
J = 64; u = (np.arange(J) + 0.5)/J
D = (1-q)/(1-q*np.exp(-2j*np.pi*u))
Dd = D*np.exp(-1j*0.1*2*np.pi*u)
p_true = (1-q)*q**np.arange(4)
p_from_D = [np.mean(Dd*np.exp(2j*np.pi*n*u)).real for n in range(4)]
print('   true p_n      ', np.round(p_true, 5))
print('   from detuned D', np.round(p_from_D, 5))
B0, B = coeffs(np.log(np.abs(Dd)), 2)
qr, xr, disc = recover(B[0], B[1])
print('   from |D| (B0, B1, B2): p0 = %.15f, q_rec - 1/3 = %.2e, |xi|^2_rec = %.2e, B1^2-2B2 = %.2e' % (np.exp(B0), qr-1/3, xr, disc))
