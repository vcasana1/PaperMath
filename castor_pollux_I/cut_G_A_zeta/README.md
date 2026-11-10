# Where G, A and zeta meet (HTML chart, v1)

`G_A_zeta_cut_v1.html` is self-contained (Plotly inlined); open it in any browser.
Data: `cut_data.py` (moduli on Re s = sigma, complex-plane curves, map of |G - A|; output `cut_data_output.txt`)
and `cut_curve3d.py` (surfaces |G|, |A|, |zeta| and the curve |G| = |A|; output `cut_curve3d_output.txt`).
`template.html` + the two JSON files rebuild the page. G and A come from `../cp_eval.py` (no zeta); zeta from mpmath.
On the line grid, max |G - A - (pi/s) cot(pi s/2) zeta(s)| = 2.7e-11 (Proposition 17.1 of v5).
