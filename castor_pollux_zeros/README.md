# Zeros of G and of A, exponential series over them, centroids (v1, 10-11-2026)

Castor–Pollux line (V. Casaña-Giner). Objects as in `Castor_Pollux_I_v1.tex`:

- `h(u) = log|2 sin(pi u)|`, `G(s) = int_1^inf h(u) u^{-s-1} du`, continued as `G = -(s+1)(s+2) H(s)/(4 pi^2)`,
  `H(s) = int_1^inf K(u) u^{-s-3} du`, `K(x) = sum_m (1 - cos 2 pi m x)/m^3 >= 0`.
- `A(s) = log(2 pi)/s + 1/s^2 - int_0^1 log(sin(pi u)/(pi u)) u^{-s-1} du`, continued by its partial fractions
  `A(s) = log(2 pi)/s + 1/s^2 + sum_k a_k/(k(2k - s))`, `a_k = sum_n n^{-2k}`; numerically
  `A = log(2 pi)/s + 1/s^2 - (psi(1 - s/2) + gamma)/s + sum_k (a_k - 1)/(k(2k - s))` (`psi` = digamma).

No zeta function is used to evaluate G or A.

## Files

| File | What it is |
|---|---|
| `funcs.py` | mpmath evaluators of `A` and `G` (20 digits), plus checks against the integral definitions |
| `fast.py` | vectorised double-precision evaluators (Gauss–Legendre in x, Euler–Maclaurin tail in n) |
| `find_zeros.py` | grid scan of `log|F|`, Newton, mpmath polish, argument-principle count, for F = G and F = A |
| `find_zeros_output.txt`, `count_check.txt` | its output: G has 79 zeros in `-1.5 <= Re s <= 3, 0.2 <= Im s <= 200`, argument principle gives 79.0000; A has none in `-6 <= Re s <= 8, 0.2 <= Im s <= 200` |
| `zeros_G.txt` | the 79 zeros of G: Re, Im, residual |
| `find_zeros_A_real.py` | the zeros of A in `-60 <= Re s <= 200`, `0 <= Im s <= 200`: all real (argument principle on two rectangles) |
| `zeros_A.txt`, `zeros_A_check.txt` | the 101 real zeros of A (`-2, -1`, then one in each interval `(2k, 2k+2)`, `k = 1..99`) and the check |
| `series_centroid.py`, `series_centroid_output.txt` | `S(x) = (1/N) sum_k exp(i o_k x)` on `[0, 2 pi]`, with `o_k = Im rho_k` for G and `o_k = rho_k` (real) for A; centroid of the zeros and centroid of the curve `S` |
| `peaks_logp.py`, `peaks_logp_output.txt` | peaks of `|S_G|` and the values `S_G(log n)` |
| `fig_series_3d.png` | 3D: `(x, Re S, Im S)` for G and A together, with the two centroids |
| `fig_centroids.png` | the curves `S` in the complex plane, and the zeros with their centroids |
| `fig_series_modulus.png` | `|S_G(x)|` and `|S_A(x)|` |
| `*.py.txt` | text copies of the scripts |

Run order: `python3 find_zeros.py` (about 25 min), `python3 find_zeros_A_real.py` (overwrites the empty
`zeros_A.txt` left by the first script), `python3 series_centroid.py`, `python3 peaks_logp.py`.
Requires numpy, scipy, mpmath, matplotlib.

## Results (measured)

- Zeros of G with `0.2 <= Im s <= 200`: 79, all with `0.1037 <= Re s <= 1.1274`; centroid `0.45923 + 119.21486 i`.
- Zeros of A in the window: all real; centroid `99.44250`.
- Centroid of `S_G` on `[0, 2pi]`: `-0.00029 + 0.00188 i`; of `S_A`: `0.00151 + 0.00423 i`.
- `|S_G(x)|` has its peaks at `x = log n` for prime powers n (2, 3, 4, 5, 7, 9, 11, 13, 17, 19, 23, 25, 27, 29, 31, ...);
  at `log 6, log 10, log 12, log 15, log 30` it is small. `|S_A|` peaks only at `x = pi, 2 pi` (spacing 2 of the real zeros).
