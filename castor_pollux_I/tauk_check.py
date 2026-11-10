#!/usr/bin/env python3
# Castor and Pollux I v5, Section 17: the points tau_k of (17.7), the first six ordinates of zeta, and |G-A| at 1/2+i tau_k.
# Numerical observations only (the paper says so). G from cp_eval (Gauss-Legendre + Euler-Maclaurin), A from (14.2)-type series.
import sys; sys.path.insert(0, '.')
import numpy as np, mpmath as mp
from cp_eval import G, A
out = open('tauk_check_output.txt', 'w')
def log(s): print(s); out.write(s + '\n')
ts = [float(2*mp.pi*(k-mp.mpf(11)/8)/mp.lambertw((k-mp.mpf(11)/8)/mp.e)) for k in range(1, 7)]
g = G(np.array([0.5+1j*t for t in ts]))
log(' k   tau_k     gamma_k   gamma_k-tau_k  |G-A|(1/2+i tau_k)')
for k, (t, gv) in enumerate(zip(ts, g), 1):
    z = float(mp.im(mp.zetazero(k)))
    log('%2d %9.4f %9.4f %9.4f %12.4f' % (k, t, z, z-t, abs(gv-A(0.5+1j*t))))
for s in [3.0, 5.0, -1.0, -3.0]:
    log('G(s)-A(s) at s=%g: %.3e' % (s, abs(G(np.array([s+0j]))[0]-A(complex(s)))))
log('Q(9) = %s' % mp.nstr(mp.log(8*mp.pi)-mp.log(82)/2-mp.mpf(81)/170+mp.mpf(1)/81-mp.mpf('0.64')*80/85+mp.mpf('1e-27'), 10))
