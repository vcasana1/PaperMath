# HANDOFF — Theorem A: pointwise gain of τ^C under RH (31 Oct 2026). Started, nothing computed yet.

## Goal (urgent: improve casanya_ordinal_primes before IJNT referees read v55; v57 already corrects literature)
Under RH, prove explicitly, for T ≥ T0:
  |S(T) − Φ_x(T)| ≤ C1 log T / log x + C2,  x = T^θ,  Φ_x(T) = −(1/π) Σ_{p≤x} arg(1 − p^{−1/2−iT})  (Euler phases),
hence |τ_k^C − γ_k| ≤ c / log γ_k pointwise (sublevel/transfer machinery of the paper: Prop. 6.2 / Lemma s_bounds).
Compare: uncorrected under RH, S ≤ (1/4+o(1)) log T/loglog T (Carneiro–Chandee–Milinovich) ⇒ |τ_k−γ_k| ≤ (π/2+o(1))/loglog γ_k.
Gain: factor log T/loglog T pointwise.

## Why only under RH (lemma to include in the paper)
If |S−P| ≤ c log T + C and sup|P| ≤ B then |S| ≤ c log T + C + B: bounded prime corrections cannot lower the provable leading
coefficient. Growing corrections (Φ_m with m≈√T) need pointwise control of zeros off the line near T (open unconditionally).

## Steps
1. Literature (verify exact statements, sharp cutoff at σ=1/2 vs Selberg smoothing Λ_x, σ_x):
   Selberg 1946 (Arch. Math. Naturvid. 48); Goldston–Gonek, Bull. LMS 39 (2007) 482–486;
   Carneiro–Chandee–Milinovich, Math. Ann. 356 (2013) 939–968; Tsang 1986 (Proc. LMS 52).
2. Explicit RH formula S(T) = −(1/π) Σ_{n≤x} Λ(n) sin(T log n)/(√n log n) + error with explicit constants; compare with Φ_x
   (prime powers k≥2 contribute O(1) explicitly).
3. Transfer to τ^C_k − γ_k with explicit constants (paper's Section 9 tools).
4. Theorem B: same unconditionally for T ≤ H (RH verified to 3·10^12, Platt–Trudgian) with far-zero control.
5. Insert as new section in v58 (= v57 + Theorems A/B/D + results of HANDOFF-turing-explicit-S.md).

## Files
- v57 and letter: ../ (this folder's parent, docs/).
- Explicit S(T)/N(T) seven-line family + hybrid a<0.07755: ../../family, ../../hybrid_asymptotic.
