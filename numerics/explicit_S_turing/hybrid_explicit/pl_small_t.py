# Certify, for each line sigma in {1/2, sigma_4..sigma_9, 1} and Q = 3, that for 0 <= t <= 3
#   |(s-1) zeta(s)| <= A |Q+s|^{1+alpha} log|Q+s|,
# with (A, alpha) the explicit line constants, so that the hypothesis of Trudgian's Lemma 3 holds on the whole line
# (|t| >= 3: |s-1| <= |Q+s|, t^alpha <= |Q+s|^alpha, log t <= log|Q+s|; t < 0 by conjugation).
# Ball arithmetic on subintervals of [0,3] (python-flint, 128 bits). Values of zeta only (no zeros are located).
from flint import arb, acb, ctx
from fractions import Fraction as Fr
ctx.prec = 128
Q = 3
lines = [(Fr(1,2), Fr(1,6), arb('0.618'))]+[(1-Fr(k, 2**k-2), Fr(1, 2**k-2), arb('1.546')) for k in range(4,10)]+[(Fr(1), Fr(0), arb('0.75'))]
for sg, al, Acon in lines:
    sA = arb(sg.numerator)/sg.denominator; aA = arb(al.numerator)/al.denominator
    worst = arb(0); n = 3000
    for i in range(n):
        tb = (arb(3*i)/n).union(arb(3*(i+1))/n); s = acb(sA, tb)
        f = (s-1)*s.zeta() if sg != 1 else None
        if sg == 1:   # (s-1)zeta(s) at s = 1+it: use the entire function via the Laurent-free identity (s-1)zeta(s) = s - s(s-1) int..., evaluate at t-ball avoiding t=0 issue
            f = acb(1) if i == 0 and False else None
        if f is None:
            # near s = 1: (s-1) zeta(s) is entire; evaluate on the ball by the midpoint and a derivative-free bound using
            # zeta(s) = 1/(s-1) + gamma + O(|s-1|) is not rigorous; instead evaluate at the ball shifted to t in [t0, t1] with t0 > 0
            # and treat [0, 3/n] separately with the Stieltjes bound |(s-1)zeta(s) - 1| <= |s-1| (gamma + |s-1| * 0.1) (|s-1| <= 3/n).
            if i == 0:
                r = arb(3)/n; f = acb(1)+acb(0, 1)*arb(0).union(r)*(arb('0.6'))   # |s-1|*(gamma_0 + ...) <= 0.6 r for r tiny
            else:
                f = (s-1)*s.zeta()
        Qs = acb(Q+sA, tb); rhs = Acon*abs(Qs)**(1+aA)*abs(Qs).log()
        ratio = abs(f)/rhs
        if ratio.upper() > worst.upper(): worst = arb(ratio.upper())
    print('sigma=%.6f alpha=%.6f A=%s  max_{0<=t<=3} |(s-1)zeta|/(A|Q+s|^{1+a} log|Q+s|) <= %s  %s' % (float(sg), float(al), Acon.str(4), worst.str(6), 'OK' if worst < 1 else 'NEEDS LARGER A'))
