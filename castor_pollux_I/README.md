# Castor and Pollux I — version 5 (11 November 2026)

V. Casaña-Giner. Manuscript `Castor_Pollux_I_v5.tex` (`.txt` is a literal copy, `.pdf` the compiled file, 37 pages),
its twelve figures, and all the code with its outputs. Everything is in this single directory.

SHA-256 of `Castor_Pollux_I_v5.tex`: `39d73e583d5e5fb016f6ea76bfa15a197f2a80359a9996457ba55d9f07ff5ea7`

## What changed

v5 (`make_v5_from_v4.py`, text of the new sections in `v5_new_sections.tex`, `diff_v4_to_v5.txt`):

- Section 15, the difference G - A without zeta: G - A = -∫ log(πu/|sin πu|) u^(-s-1) du on 0 < Re s < 2, the bound
  |G - A| <= A(σ) - G(σ), the decomposition through ψ(1 - s/2) - ψ(1 + s), and an analytic proof that A(s) != 0 for
  0 <= Re s <= 1, |Im s| >= 9 (Theorem 15.4). Remark 15.5 points to the ball-arithmetic check `A_nonvanishing_check.py`
  of 0 <= Re s <= 1, 0 <= Im s <= 102 (computer-assisted; nothing depends on it).
- Section 16, the positive convex kernel B (B'' = 4π² log(πu/|sin πu|)): G - A = -(s+1)(s+2)Ω(s)/(4π²), the inversion
  inequality B(u) > u^(2σ+4) B(1/u), the two positive weights, a region without solutions of G = A near the real axis,
  the decay Ω = O(t^-2), and a two-harmonic positive kernel whose G - A vanishes at 3/4 + i(2k+1)π/log 2.
- Section 17, with zeta (cited: Titchmarsh 1986 pp. 13, 15, 16, 45, 211, 214, 256; Titchmarsh 1939 p. 149):
  G - A = (π/s) cot(πs/2) ζ(s), and "every non-real solution of G = A has real part 1/2" is equivalent to RH.
  RvM points τ_k (numbers in `tauk_check.py`, output `tauk_check_output.txt`).
- Section 18, Conclusions: what is characterized without zeta, why introducing zeta does not lead further, and whether
  and where G and A intersect.
- Letters: p^a -> p^k in the Jordan totient paragraph and a_b -> θ_b in the proof of Corollary 11.3 (a is max(j,k));
  y added to the real variables; the twelve figures are unchanged.

v3 (`make_v3_from_v2.py`, `diff_v2_to_v3.txt`):

- Proposition 14.1 (continuation and real zeros of the auxiliary function A), with proof.
- Surfaces of G, A, G - A and zeta on a fine grid (253 x 889 points, refined near the zeros), and a new surface of A near
  the real axis, where its zeros are.
- Exponential sums over the 79 computed zeros of G and the 101 computed real zeros of A: three figures and their description.
  In the 3D figure the variable x is the vertical axis.

v4 (`make_v4_from_v3.py`, `diff_v3_to_v4.txt`): the surfaces show the modulus itself on a linear scale, with the vertical
axis inverted (0 at the top). A zero is a peak whose tip is at 0, where the red points are. No logarithm is plotted.

v2 (ball-arithmetic certificate of the six Rouche discs and the corrections of the review) is described in
`CONTINUACION_CASTOR_POLLUX_v5.md`.

## Files

| File | Content |
|---|---|
| `fig_kernel.png`, `fig_G_real.png` | written by `figures.py` (v1) |
| `fig_gram.png`, `gram_flat.csv`, `gram_weighted.csv` | written by `figure_gram.py` |
| `fig_G_surface.png`, `fig_A_surface.png`, `fig_A_real_surface.png`, `fig_GminusA_surface.png`, `fig_zeta_surface.png`, `fig_zero_map.png` | written by `figures_v4.py` (output `figures_v4_output.txt`); it also writes `grid_values_v4.npz`, not stored here (about 20 s to regenerate) |
| `fig_expsum_3d.png`, `fig_expsum_plane.png`, `fig_expsum_modulus.png` | written by `expsum_v3.py` (output `expsum_v3_output.txt`) |
| `cp_eval.py` | double precision evaluators of G (kernel K only) and of A (partial fractions); no zeta function |
| `zeros_G.txt`, `zeros_A.txt` | the 79 zeros of G with 0.2 <= Im s <= 200 and the 101 real zeros of A in [-60, 200]; computed by `find_zeros.py`, `find_zeros_A_real.py` (with `funcs.py`, `fast.py`; checks in `count_check.txt`, `zeros_A_check.txt`), taken from the branch `castor-pollux-zeros` |
| `castor_pollux_I_rouche_certificate_v1.py`, `..._output.txt`, `..._intervals.json` | Arb ball-arithmetic certificate of the six Rouche discs of Table 2 |
| `castor_numerics.py`, `pollux_gram_check.py` and outputs | the numbers of Sections 8, 10 and 13 (v1) |
| `make_v2_from_v1.py`, `make_v3_from_v2.py`, `make_v4_from_v3.py`, `make_v5_from_v4.py`, `diff_v*_to_v*.txt`, `allowed_labels_v*.txt` | the exact edits between versions |
| `build.py` | generator of the hover previews (v1); `make_v3_from_v2.py` and `make_v4_from_v3.py` use its `detex` function |
| `*.py.txt` | text copies of the scripts |

Order to regenerate the figures: `figures.py`, `figure_gram.py`, then `figures_v4.py` (it overwrites the four surfaces and
the zero map written by `figures.py`), then `expsum_v3.py`. Requires numpy, scipy, mpmath, matplotlib; python-flint for the certificate.

Compile: four passes of pdfLaTeX on `Castor_Pollux_I_v5.tex` in this directory. The CorrectVCG checker travels inside the
`.tex` after `\end{document}`.
