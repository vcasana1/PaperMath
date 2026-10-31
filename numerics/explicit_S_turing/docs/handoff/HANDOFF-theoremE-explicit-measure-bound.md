# HANDOFF — Theorem E: explicit C in ∫_T^{2T} |S − Φ|^2 ≤ C T (unconditional) (31 Oct 2026).

User rules: no Platt / no numerical zero verification; no forbidden word; files: tex+txt+pdf.

Proved (chat): (d) meas{t∈[T,2T]: |N−N^C|>A} ≤ C1 T/A, C1 ≈ 3√C/(2π) (∫|N_a−N_b| ≤ Σ|a_k−b_k| + Cauchy–Schwarz).

## KEY INGREDIENT FOUND (step 3): explicit Selberg zero density
Simonič, "Explicit zero density estimate for the Riemann zeta-function near the critical line", arXiv:1910.08274v2
(published J. Math. Anal. Appl. 2020 — verify), Theorem 1: for T ≥ T0 := 3.0610046·10^10 and σ ∈ [1/2, 0.831],
  N(σ,2T) − N(σ,T) ≤ a T^{1−(σ−1/2)/4} log T + b log²T + c log T loglog T + d log T,
  a = 10395.2, b = 1.104, c = 0.173, d = 0.51.  For T ≥ 10^50, σ ∈ [1/2,0.569]: a = 5.357 (method cannot go below 3.259).
NOTE: T0 is only a threshold (proof needs T0 ≥ e^24); it does NOT use numerical verification of zeros (it uses the
explicit RvM formula (1)). Also gives explicit ∫|ζ(1/2+it)|² (Cor. 5) and explicit Selberg mollifier mean square (Prop. 2).

## Remaining chain
1. Explicit Selberg formula S(t) − (smoothed prime sum) = error (Selberg 1946 Lemma; Tsang 1986): make c1,c2,c3 explicit.
2. Montgomery–Vaughan explicit (in paper).
3. Zero term mean square via Simonič Thm 1 (dyadic in σ, Selberg's argument with x = T^θ).
4. Φ (paper, sharp cutoff, dyadic m_j) vs Selberg's smoothed sum: explicit mean-square difference.
5. Minkowski → C. Expect C large (a ≈ 10^4 enters), valid for T ≥ T0.

## Update (user's note, docs/handoff/TheoremE_explicit_constants_user_note.md)
Route via Simonič–Trudgian–Turnage-Butterbaugh 2020 (arXiv:2010.10675), Thm 5 / Cor. 2 (explicit fourth moment of
S − short prime sum, M = 2.69927·10^21, U ≥ e^{3520000}). Result for T ≥ e^{3520004}, unconditional:
(E1) Σ_{T<γ_k≤2T} |γ_k^C − γ_k|^2 ≤ 10^28 T/log T;  (E2) ∫_T^{2T}|N − N_C| ≤ 4·10^14 T;  (E3) Markov.
Does NOT improve C1, C2, C3 for all T (needs local control beyond integrated bounds).
