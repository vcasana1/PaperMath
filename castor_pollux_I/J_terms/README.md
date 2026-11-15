# J_terms (v2)

Three terms of the regularized integral J(s) = int_0^inf Q(u) u^{-s-3} du, with
Q(u) = (1/2 pi^2) sum_{m>=1} sin^2(pi m u)/m^3 >= 0 and Q'' = -h, h(u) = log|2 sin pi u|:

* T1: 0 < u < 1, minus q0(u) = (u^2/2)(3/2 - log 2 pi u);
* T2: u > 1;
* T3: counterterm (1/2)(1/s^2 - (3/2 - log 2 pi)/s).

J = T1 + T2 + T3 = -(G - A)/((s+1)(s+2)), valid in -2 < sigma < 2.
Computed for sigma in [1/2, 1] at t = 14.1347, 20, 50 (`J_terms_v2_output.txt`, `J_terms_v2.csv`, `fig_J_terms_v2.png`).
Check of the sum against -(G-A)/((s+1)(s+2)): relative error <= 1e-6.
