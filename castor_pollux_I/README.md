# Castor and Pollux I — version 3 (10 November 2026)

V. Casaña-Giner. Manuscript `Castor_Pollux_I_v3.tex` (`.txt` is a literal copy, `.pdf` the compiled file, 25 pages),
its twelve figures, and all the code with its outputs. Everything is in this single directory.

SHA-256 of `Castor_Pollux_I_v3.tex`: `1465a2c038a3e88ba45c4ea62c11ee4a1e3cc567ce9d75b45ad82c8f1d487f87`

## What changed from v2

`make_v3_from_v2.py` produces v3 from v2 by 14 exact replacements (`diff_v2_to_v3.txt`):

- Proposition 14.1 (continuation and real zeros of the auxiliary function A), with proof.
- Surfaces of G, A, G - A and zeta on a fine grid (253 x 889 points, refined near the zeros). They show -log10 of the
  modulus, so a zero is a peak. New surface of A near the real axis, where its zeros are.
- Exponential sums over the 79 computed zeros of G and the 101 computed real zeros of A: three figures and their description.
  In the 3D figure the variable x is the vertical axis.

v2 itself (ball-arithmetic certificate of the six Rouche discs and the corrections of the review) is described in
`CONTINUACION_CASTOR_POLLUX_v3.md`.

## Files

| File | Content |
|---|---|
| `fig_kernel.png`, `fig_G_real.png` | written by `figures.py` (v1) |
| `fig_gram.png`, `gram_flat.csv`, `gram_weighted.csv` | written by `figure_gram.py` |
| `fig_G_surface.png`, `fig_A_surface.png`, `fig_A_real_surface.png`, `fig_GminusA_surface.png`, `fig_zeta_surface.png`, `fig_zero_map.png` | written by `figures_v3.py` (output `figures_v3_output.txt`); it also writes `grid_values_v3.npz`, not stored here (about 20 s to regenerate) |
| `fig_expsum_3d.png`, `fig_expsum_plane.png`, `fig_expsum_modulus.png` | written by `expsum_v3.py` (output `expsum_v3_output.txt`) |
| `cp_eval.py` | double precision evaluators of G (kernel K only) and of A (partial fractions); no zeta function |
| `zeros_G.txt`, `zeros_A.txt` | the 79 zeros of G with 0.2 <= Im s <= 200 and the 101 real zeros of A in [-60, 200]; computed by `find_zeros.py`, `find_zeros_A_real.py` (with `funcs.py`, `fast.py`; checks in `count_check.txt`, `zeros_A_check.txt`), taken from the branch `castor-pollux-zeros` |
| `castor_pollux_I_rouche_certificate_v1.py`, `..._output.txt`, `..._intervals.json` | Arb ball-arithmetic certificate of the six Rouche discs of Table 2 |
| `castor_numerics.py`, `pollux_gram_check.py` and outputs | the numbers of Sections 8, 10 and 13 (v1) |
| `make_v2_from_v1.py`, `diff_v1_to_v2.txt`, `make_v3_from_v2.py`, `diff_v2_to_v3.txt`, `allowed_labels_v*.txt` | the exact edits between versions |
| `build.py` | generator of the hover previews (v1); `make_v3_from_v2.py` uses its `detex` function |
| `*.py.txt` | text copies of the scripts |

Order to regenerate the figures: `figures.py`, `figure_gram.py`, then `figures_v3.py` (it overwrites the four surfaces and
the zero map written by `figures.py`), then `expsum_v3.py`. Requires numpy, scipy, mpmath, matplotlib; python-flint for the certificate.

Compile: four passes of pdfLaTeX on `Castor_Pollux_I_v3.tex` in this directory. The CorrectVCG checker travels inside the
`.tex` after `\end{document}`.
