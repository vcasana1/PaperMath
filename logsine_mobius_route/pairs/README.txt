Exploratory computations: log-sine products, Mobius twist, prime averages (8 Nov 2026)
Each script X.py has its output in X_output.txt (python3, numpy, sympy, mpmath, scipy).

check.py          S_k(h) shifted identity (direct vs divisor formula, k<80, h<60); E = -gamma + sum_p log p/(p-1)^2 (primes < 1e7)
conj_divisor.py   R(y) = sum_{k<=y} log|2 sin(pi y/k)| - (log2 - C) y at random real y, rms/y^{1/4}; Delta(y) for comparison
voronoi_fit.py    least squares fit of R(y) and Delta(y) on y^{1/4} sum d(n) n^{-3/4} {sin,cos}(4 pi sqrt(ny) - pi/4); sign law (-1)^floor(sqrt p) check
primes_fit.py     same fit for log|P(p)| + C p along primes near 1e5
H_explicit.py     H(x) = sum_{d<=x} mu(d) log|2 sin(pi x/d)| vs sum over first 150 zeros of A(rho) x^rho / zeta'(rho)
A_zeros.py        digamma closed form of A(s); argument principle for zeros of s^2 A(s) in 0.01<=sigma<=0.99, |t|<=100 (numerical, not interval-certified)
idcheck.py        sum mu(d) log(1-e(x/d)) = H(x) + i pi (x m(x) - 1 - M(x)/2); H(n+) = regular sum + Lambda(n)
left_sing.py      one-sided singularity of H at integers: coefficient -mu(n) from the left, 0 from the right
transition.py     mean over the 8392 primes in [1e5,2e5] of sum_{2<=k<=y} log|2 sin(pi p/k)| vs sum_{k<=y} Lambda(k)/phi(k).
                  NOTE: the column "cubic" is a fixed-p heuristic that turned out WRONG (sign); the edge-effect
                  prediction +zeta(3) y^3/(8 pi^2 X^2) discussed in chat is not in this script.
checkAD.py        checks of the other text's Theorems A-C: Euler product constant V, DFT identity, Parseval vs sampled variance (y=60)
parseval_scale.py Var(F_y) from the Fourier formula (8) for y up to 1e5, compared with V log^4 y
