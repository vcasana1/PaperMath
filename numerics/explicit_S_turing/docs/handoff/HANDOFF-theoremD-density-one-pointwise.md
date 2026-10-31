# HANDOFF — Theorem D (unconditional, density one): |τ_k^C − γ_k| < |τ_k − γ_k| for almost all k (31 Oct 2026). To write.

Statement: Let K_T = {k : T < γ_k ≤ 2T}. Then #{k ∈ K_T : |τ_k^C − γ_k| ≥ |τ_k − γ_k|} = o(#K_T) as T → ∞. (No hypothesis.)

Proof plan:
1. Selberg CLT (unconditional): meas{t ∈ [T,2T] : |S(t)| ≤ ε sqrt(loglog T)} ≪ ε T + o(T). Need the version on the discrete set
   t = γ_k (or at the points s_k of the paper): Fujii / Hejhal / Tsang give CLT-type statements at zeros, or use the
   paper's s_k (value of N − N_0 at the sublevel points) with the transfer lemma.
2. Second moment of S − Φ_m (paper, Theorem 8.x, unconditional): Σ_{k∈K_T} |s_k^C|^2 ≪ #K_T ⇒ #{|s_k^C| > A} ≪ #K_T / A².
3. Distances: |τ_k − γ_k| ≍ 2π|s_k|/log T and |τ_k^C − γ_k| ≍ 2π|s_k^C|/log T up to the transfer error (Lemma s_bounds,
   Theorem transfer); need the pointwise (not only L²) form for typical k: check that the paper's transfer gives
   |τ_k − γ_k| ≥ 2π(|s_k| − 1/2 − o(1))/log T (eq. 6.1-type lower bound) and the upper bound for τ^C.
4. Choose A = (loglog T)^{1/4}: exceptional k have |s_k| ≤ 2A (density → 0 by CLT) or |s_k^C| > A (density ≪ 1/A² → 0).

Remaining work: verify step 1 at the zeros (literature: Fujii 1974 Acta Arith.; Tsang 1984 thesis; Hejhal), step 3 pointwise.
Insert in v58 with Theorem A plan (HANDOFF-tauC-pointwise-RH-theoremA.md).
