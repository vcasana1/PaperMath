# Explicit and asymptotic bounds for S(T) by the Turing–Amberger–Bellotti–Wong method

V. Casaña-Giner. Numerical certificates (Arb ball arithmetic, python-flint 0.9.0, 256 bits).
These are not Lean files; they are not imported by the Lake project.

Notation: `N(T)` counts zeros with `0 < γ ≤ T`; `main(T) = (T/2π) log(T/2πe)`; `a = limsup |S(T)|/log T`.

## 1. `hybrid_asymptotic/` — asymptotic bound below the Lindelöf limit of Backlund's method

Turing–Amberger identity + kernel majorant + Jensen discs controlled by Bourgain's exponent profile.

| file | result |
|---|---|
| `sol_m10_B_eta0.001.json`, `cert_m10B.txt` | `a < 0.0775422804104` (d = 9/10, kernel of order m = 10, 39 discs) |
| `sol_m4_B_eta0.002.json`, `cert_m4B.txt` | `a < 0.0820487876897` (d = 7/10, m = 4, 33 discs) |

`certify_hybrid.py` certifies `f(b,t) ≤ U(b,t) + Σ κ_k W_k(b,t)` on `0 ≤ b ≤ 1/2`, `t ≠ 0` (bounded region by
centred-form bisection, tail `|t| ≥ 100` in the variable `u = 1/t`) and computes `C_H` in closed form.
`lpm.py` is the linear program (cutting planes) that produced the coefficients.
Asymptotic only: no bound at any finite height.

## 2. `explicit_allT_BWkernels/` — explicit bound for all T ≥ 1 with the kernels of Bellotti–Wong

With the kernels (2.43) and (2.44) of Bellotti–Wong (arXiv:2606.31441), rounded to binary:

    |N(T) − main(T)| ≤ min(0.0946 log T + 5.138, 0.097 log T + 4.507)   (T ≥ 1)

(their constants: 5.746 and 4.954). No numerical data on zeros (no Platt) are used.

| step | file | value |
|---|---|---|
| kernel inequality | `cert_bw243.txt`, `cert_bw244.txt` | certified |
| Euler-product constant `C_ζ = Σ Λ(n) n^{-σ1} hypot(A0, B0)` | `cz_bw243.txt`, `cz_bw244.txt` | `< 4.40866580476`, `< 3.78925591739` |
| elementary part, sup over T ≥ 1 | `elem_bw243.txt`, `elem_bw244.txt` | `≤ 0.7283361433`, `≤ 0.7174847556` |

`cz_arb.py`: exact Arb sum over all prime powers ≤ 10^8, tail by partial summation with
`ψ(x) < 1.03883 x` (Rosser–Schoenfeld 1962, Thm 12) and certified monotonicity.
`elem_arb.py`: centred form on 9215 intervals of [1, 10^4]; for T ≥ 10^4 Stirling with Olver's remainder
(DLMF 5.11(ii)) and Cauchy estimates for the derivatives.

## 3. `family/` — optimized kernels, one per range of log T (in progress)

See `family/STATUS.md`.
