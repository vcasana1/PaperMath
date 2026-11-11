# Where G, A and zeta meet (HTML chart, v1)

`G_A_zeta_cut_v1.html` is self-contained (Plotly inlined); open it in any browser.
Data: `cut_data.py` (moduli on Re s = sigma, complex-plane curves, map of |G - A|; output `cut_data_output.txt`)
and `cut_curve3d.py` (surfaces |G|, |A|, |zeta| and the curve |G| = |A|; output `cut_curve3d_output.txt`).
`template.html` + the two JSON files rebuild the page. G and A come from `../cp_eval.py` (no zeta); zeta from mpmath.
On the line grid, max |G - A - (pi/s) cot(pi s/2) zeta(s)| = 2.7e-11 (Proposition 17.1 of v5).

## v2 (11 November 2026)

`G_A_zeta_cut_v2.html` adds the vertical cut at Re s = 1/2: the curves t -> G(1/2+it) and t -> A(1/2+it) in
(Re, Im, t) with t vertical, the curve G - A in the plane, and the table of the 29 coincidences G = A with t <= 100,
located from G and A only (`vertical_cut.py`, output `vertical_cut_output.txt`); they match the ordinates of the
zeros of zeta to 6e-7. Template: `template_v2.html` (+ `cut_data.json`, `cut_curve3d.json`, `vertical_cut.json`).
