# Hypotheses of the main theorems

For each main theorem: every hypothesis as it is written in Lean, its source in the literature (author, year,
statement, DOI) and whether it is a **literature** input, a **numerical** input (a real number checked by
interval arithmetic outside Lean), or a **proved** fact (formerly a hypothesis, now a theorem of this library).
The numbering of theorems, lemmas and equations is that of the article *The Riemann–von Mangoldt clock*
(`rvm_clock_envelope`, v10).

Lean guarantees that the conclusions follow from the hypotheses. It does **not** check that a hypothesis is
transcribed correctly from its source, nor that the hypotheses are satisfiable. Those two points are what an
external review has to verify, statement by statement, against the sources below.

## Branch B — Theorem 1.3, `RvmClock.C1.theorem_1_3_numeric` (`PaperMath/Papers/RvmClock/C1.lean`)

Conclusion: for every `T ≥ e`, `|S(T)| ≤ 0.09783 log T + 0.7214 log log T + 10.6`, inequality (1.7).

The parameters are `c = cc = 1.000002`, `R = RR = 1.000005`, `σ♯ = sigS = c + (c − 1/2)²/R`,
`δ♯ = delS = 2c − σ♯ − 1/2`, `𝔡 = dd = log (R/(c − 1/2))` (`Explicit.lean`), and `eStar = 𝔢_E^*` is the reflected
explicit profile of §4.1 (`Profile.lean`). `sp σ t = σ + it`.

| Lean hypothesis | Statement | Source | Kind |
|---|---|---|---|
| `S : ℝ → ℝ` | the function `S(T)`; it enters only through `hdec` and `hplatt` | — | abstract datum |
| `I : ExplicitInputs` (`ZetaLines.lean`) | `I.hpy`: `‖ζ(1/2+it)‖ ≤ 0.618 |t|^{1/6} log|t|` for `3 < |t| ≤ e^105` | Hiary–Patel–Yang 2024, Thm. 1.1, doi:10.1016/j.jnt.2023.09.003 (Theorem 3.3(a)) | literature |
| | `I.py`: `‖ζ(1/2+it)‖ ≤ 66.7 |t|^{27/164}` for `|t| > e^105` | Patel–Yang 2024, Thm. 1.1, doi:10.1016/j.jnt.2024.03.011 (Theorem 3.3(a)) | literature |
| | `I.yang`: `‖ζ(σ_m+it)‖ ≤ 2 |t|^{1/(2^m−2)} log|t|` for `4 ≤ m ≤ 9`, `|t| ≥ 3`, `σ_m = 1 − m/(2^m−2)` | Yang 2024, Thm. 1.1, doi:10.1016/j.jmaa.2024.128124, **with constant 2 instead of 1.546** (Remark 4.5(ii) of the article: Yang's constant on `3 ≤ |t| ≤ T_m` is recomputed as 1.878 ≤ 2) | literature, not literal |
| | `I.patel`: `‖ζ(1+it)‖ ≤ log|t|` for `|t| ≥ 3` | Patel 2022, Thm. 1.1, doi:10.1016/j.indag.2022.04.007 (Theorem 3.3(c)) | literature |
| | `I.zeta3`: `‖ζ(3+it)‖ ≤ 1.21` | trivial bound `|ζ(3+it)| ≤ ζ(3) = 1.2020…` (not yet proved in Lean) | literature (elementary) |
| | `I.small`: `‖Ξ(s)‖ ≤ ‖s‖ + 2‖s‖‖s−1‖` for `1/2 ≤ σ ≤ 3`, `Ξ(s) = (s−1)ζ(s)` | consequence of Titchmarsh 1986, (2.1.4) | literature (consequence, not the formula itself) |
| | `I.pl`: Phragmén–Lindelöf for `Ξ` between two lines, `Q = 10`, `A = B = 2`, equal log powers | Fiori 2026, Cor. 3, doi:10.48550/arXiv.2502.13282 (Theorem 3.4); Rademacher 1959, doi:10.1007/BF01162949. The holomorphy and growth hypotheses on `Ξ` are classical and not checked | literature |
| `chi : ℂ → ℂ`, `hFE` | `ζ(s) = χ(s) ζ(1−s)` for `−0.01 ≤ σ ≤ 1/2`, `t ≥ 98` | functional equation (Titchmarsh 1986, (2.1.1)) | literature (classical) |
| `hchi` | `‖χ(σ+it)‖ ≤ 1.0070 (t/2π)^{1/2−σ}` for `−0.01 ≤ σ ≤ 1/2`, `t ≥ 98` | Lemma 4.3 of the article (from Stirling with remainder, DLMF §5.11(ii)) | article lemma, not yet in Lean |
| `Z : ℝ → ℕ → ℝ`, `A0 D1 D2 E : ℝ → ℝ` | `Z T n = 𝒵_n(c,R)` at height `T`; `A0 = arg ζ(σ♯+iT)`-term, `D2 = Δ arg((s−1)ζ(s))` from `σ♯` to `1/2`, `D1 = Δ arg(s−1)`, `E T = 𝓔(T,δ♯)` | §5 of the article, (5.3) | abstract data |
| `hA` | Theorem 3.5(a): for every even majorant `Ψ ≥ (1/n) log|𝔣_n(c+Re^{iθ})|` there is a subsequence with `limsup 𝒵_{n_m} ≤ log(ζ(c)/(√((c−1)²+T²) ζ(2c))) + (1/π)∫₀^π Ψ` | Bellotti–Wong 2025, Lemma 2.1, doi:10.1090/mcom/4133 (after Hasanalizade–Shen–Wong 2022, Props. 3.5, 3.7, doi:10.1090/mcom/3665) | literature |
| `hB` | Theorem 3.5(b): `|D2| ≤ π 𝒵_n/(2𝔡) + 𝓔(T,δ♯)/2 + 3π/(2n) + π/4` for every `n ≥ 1` | Bellotti–Wong 2025, Lemmas 2.3, 2.4; Bennett–Martin–O'Bryant–Rechnitzer 2021, Lemma 3.4, doi:10.1090/mcom/3599 | literature |
| `hEc` | Theorem 3.5(c): `𝓔(T,δ♯)/π ≤ (640δ♯ − 112)/(1536(3T−1)) + 2^{−10}` for `T ≥ 100` | Bennett et al. 2021, p. 1463, as used in Bellotti–Wong 2025 | literature |
| `hdec` | `π S(T) = A0 T + D2 T − D1 T` for `T ≥ 100` | decomposition of `π S(T)` used in Bellotti–Wong 2025, §3 (equation (5.3) of the article) | literature (classical) |
| `hA0` | `|A0 T| ≤ log ζ(σ♯)` | `|arg ζ(σ♯+iT)| ≤ |log ζ(σ♯+iT)| ≤ log ζ(σ♯)` (Euler product, §5 of the article) | literature (classical) |
| `hD1` | `D1 T = arctan((σ♯−1)/T) + arctan(1/(2T))` | elementary (§5 of the article) | literature (elementary) |
| ~~`hC1`~~ | `C₁ = (1/(2π𝔡)) ∫₀^π 𝔢_E^*(c + R cos θ) dθ ≤ 0.0978293` | `RvmClock.C1.C1_le` (`C1.lean`): exact piecewise integration, value `0.0978292318785…`, margin `6.8·10⁻⁸` | **proved** |
| `hplatt` | `|S(T)| ≤ 2.5167` for `e ≤ T ≤ 100` | Bellotti–Wong 2025, (1.2), from Platt 2017, doi:10.1090/mcom/3198 (Theorem 3.6) | literature (computation) |
| ~~`hzc`, `hz2c`, `hzeta`~~ | `0 < ζ(c)`, `0 < ζ(2c)`, `log(ζ(c)/ζ(2c)) ≤ 12.62467` | `RvmClock.ZetaConst` (`ZetaConst.lean`), margin `2.44·10⁻⁶` | **proved** |
| ~~`hzs`~~ | `log ζ(σ♯) ≤ 1.52499` | `RvmClock.ZetaSigS.log_zeta_sigS_le` (`ZetaSigS.lean`), margin `4.6·10⁻⁶` | **proved** |

`RvmClock.Thm13.theorem_1_3` (`Thm13.lean`) is the same theorem with `zc, z2c, zs` free and the five struck-out
lines as hypotheses; `Thm13.theorem_1_3_zeta` (`Thm13Zeta.lean`) instantiates `zc := ζ(c)`, `z2c := ζ(2c)`,
`zs := ζ(σ♯)` (Mathlib's `riemannZeta`, real part) and discharges four of them; `C1.theorem_1_3_numeric`
discharges `hC1` too, so every remaining hypothesis is a literature input.

Intermediate results and their own hypotheses: `RvmClock.ZetaLines.lemma_4_4` (Lemma 4.4, hypotheses `I`,
`hFE`, `hchi`), `RvmClock.Backlund.master` (Proposition 5.1, general `c, R, K, h, Ω`), `RvmClock.Explicit.thm_1_3`
(the final deduction from the assembled bound (5.4)).

## Branch A — Theorem 1.5 and Corollary 1.6, `RvmClock.sublevel`, `RvmClock.proportion` (`Sublevel.lean`)

Data `Z : ZetaInputs` (`Inputs.lean`, extending `Ordinates` of `Gaps.lean`):

| Field | Statement | Meaning | Kind |
|---|---|---|---|
| `Z.γ : ℕ → ℝ`, `Z.mono`, `Z.unbounded` | monotone, unbounded sequence; `Z.N t = #{k : γ_k ≤ t}` | the ordinates `γ_{k+1}` (Lean index `k`), counted with multiplicity | abstract datum |
| `Z.varpi`, `Z.varpi_meas`, `Z.varpi_bound` | measurable, `|ϖ(t)| ≤ 1/t` for `t ≥ 1` | the Stirling remainder of the Riemann–Siegel theta; Lemma 4.1 gives `0.53/t` | abstract datum (Lemma 4.1 pending) |
| `Z.S := N − N₀ − ϖ/π` | definition | formula (1.1) used as the definition of `S` | definition |

| Lean hypothesis | Statement | Source | Kind |
|---|---|---|---|
| `hA : Z.FujiiA` (`Fourth.lean`) | `∃ A U₀, ∀ U ≥ U₀, ∫_U^{2U} |S(t) − (1/π) Im Σ_{p<U^{1/200}} p^{−1/2−it}|⁴ dt ≤ A U` | Fujii 1974, §3, pp. 232–233, doi:10.1090/S0002-9947-1974-0349603-2, with the corrections of Fujii 1981, §5, doi:10.1090/S0002-9947-1981-0621970-5 (Theorem 3.8(a), `k = 2`, `α_F = 1/5`, `H = T = U`, `Y = U^{1/200}`) | literature |
| `hB : Z.FujiiB` (`Inputs.lean`) | `∃ A T₀, ∀ T ≥ T₀, ∀ 0 < h ≤ 1, ∫_T^{2T} (S(t+h) − S(t))⁴ dt ≤ A T log²(2 + h log T)` | Fujii 1974, Main Theorem, p. 225, with Fujii 1981, §5 (Theorem 3.8(b), `k = 2`, `α_F = 1/2`, `H = T`) | literature |
| `hTi : Z.Titchmarsh` (`Sublevel.lean`) | `S(t) = O(log t)` and `γ_{k+1} − γ_k → 0` | Titchmarsh 1986, §§9.4, 9.12 (Theorem 3.1) | literature (classical) |

Everything else in Branch A is proved without hypotheses: Lemma 7.2 (`maximal_cube_36`), the bathtub
inequalities, Theorem 7.3 (`transfer`, `transfer_36`; see the scope note below), §7.1 and Proposition 7.1
(`Construction.lean`), the Mertens-type bounds (`Mertens.lean`), Theorem 3.9 (`mean_value`, from the
Montgomery–Vaughan inequality `Zeta23.MV.mv_hilbert` ported from zeta23), Lemma 7.4 and Lemma 7.5.

Scope notes (from the external review of 2026-10-26):
* `maximal_cube_36` is the *window* form of Lemma 7.2 (maximal function over intervals inside `[A,B)`), which
  is what Theorem 7.3 uses; the article states the stronger form on `ℤ`.
* `transfer_36` assumes, besides measurability of `f`, that `q_f²(q_f+1)²` is integrable on `(a,b]`; in the
  application (`Sublevel.lean`) this is proved, not assumed.
* Lemma 4.4: the intermediate constant of (4.5) is 2.7185 in Lean (2.7167 in the article); the final 2.74 is the same.

## Common

The lemmas of `PaperMath/Common/` have no hypotheses beyond their explicit arguments and depend only on the
standard axioms (`Audit.lean`).
