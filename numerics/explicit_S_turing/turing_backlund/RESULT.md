# Turing–Backlund split (31 Oct 2026) — exploratory, grid LP, not certified

Identity (proved in chat): pi S(T) = arg zeta(b2+iT) − ∫_{β*}^{b2} F − ∫_{β*}^{2β*−1/2} F − Σ_ρ g_δ(b_ρ,t_ρ) + O(1), β* = 1/2+δ,
Σ g_δ = −(1/2) Σ f_δ (pairing ρ ↔ 1−ρ̄ works for every δ > 0); kernel may be evaluated at any abscissa 1/2+dk > 1.

Result of the test (tb_scan.py):
- Kernel part A(δ) ≈ 0.080–0.091 for δ ∈ {0.05, 0.1, 0.2}, m ≤ 12, dk ∈ {0.55, 0.8}: essentially independent of δ.
  The binding constraint is the jump π of f_δ at t → 0 for |b| < δ, which kernels of width ≥ dk cannot follow.
- Backlund part B (Jensen on (ζ(z+iT)+ζ(z−iT))/2, centre c0 ≥ 1.75 so Re ζ(c0+iT) > 0): B(0.6) ≈ 0.44, B(0.75) ≈ 0.25.
- Total A + B ≫ 0.0775: this split does NOT improve the hybrid. (A centre c0 → 1 as in the paper's Backlund argument
  would lower B, but A alone is already ≥ 0.080 > 0.0775.)
Conclusion: discard this route; the hybrid (kernel + Jensen discs on ζ) remains the best asymptotic method (0.0775 certified).
