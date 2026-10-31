# Inventory of numerical claims: casanya_ordinal_primes_v47.tex (body, lines 287-1787)

Programs (all in this directory, run with `python3 -I <file>`; python-flint 0.9.0, Arb, 256 bits, 40 printed digits):

- `constants_arb.py` (already there): Λ(e_B), Λ(0), C_1, C_2, σ#, δ#, d, I_{e_E*}, log ζ(σ#), log(ζ(c)/ζ(2c)), χ factor, K_1, K, E/(2π), C_3(100), the crossing with Bellotti–Wong (with its sign structure on [1,∞)), and the crossing with Yang (4.29).
- `paper_numerics_arb.py` (new) and its output `paper_numerics_arb_output.txt`: 112 checks certified, 4 claims certified to FAIL. Exit code 0.
- `../b47/code/yang_smallt_arb.py` (the paper's Appendix A program, Arb at 120 bits): re-run, output identical to the paper's (max 1.87781, at m=9).

Reading conventions:

- "x = d…" means truncated digits: d ≤ x < d + 10^-k. Every other "…" value in the paper follows this convention; that is why the three rounded displays are listed as failures.
- A displayed bound must be rounded in the safe direction.
- Exact rationals are handled with `Fraction`, and every inequality is asserted on the whole ball.

Types: OWN = constant of the paper; ARITH = arithmetic on an external constant; EXT = external constant quoted (checked only as quoted); RAT = exact rational/polynomial identity.

## A. Substantive items

| id | tex line | quote | type | formula / how it is determined | status |
|---|---|---|---|---|---|
| S1 | 387, 925 | nine Bourgain nodes; at ε'=0 the ς'_j increase, ς'_7<1, κ_j decrease | OWN/RAT | (λ_j−κ_j, κ_j), (κ_j,λ_j)=A^j(13/84,55/84) | CERTIFIED (exact equality with display) |
| S2 | 394, 937, 305 | Λ(e_B)=0.0968160063238…; 0.0968160063…; 0.0968160… | OWN | (1/(2π log2))∫_0^π e_B*(1+cosθ)dθ; three independent exact evaluations: hinge closed form (5.9), exact piecewise antiderivative (new), acb.integral (constants_arb) | CERTIFIED; true 0.09681600632384896560… |
| S3 | 939, 1634 | 0.096816006 ≤ Λ(e_B) ≤ 0.096816007; margins ≥ 3·10^-10 | OWN | as S2 | CERTIFIED; lower margin 3.2385·10^-10 (tight but true) |
| S4 | 413, 998, 307 | 2πΛ(e_B)=0.6083129… < 0.60832 | OWN | 2π·S2 | CERTIFIED; 0.60831290843381374984… |
| S5 | 937 | θ_h = 2π/3 at c=R=1 | OWN | arccos(−1/2) | CERTIFIED |
| S6 | 917, 921, 525 | Λ(0)=(3√3−π)/(12π log2)=0.0786252…; ∫_{2π/3}^π(−½−cosθ)dθ=√3/2−π/6 | OWN | exact antiderivative of 0* on the circle | CERTIFIED; 0.07862527909020537718… |
| S7 | 920 | Lindelöf ⇒ 𝔞 ≤ 0.0786253 | OWN | Λ(0) ≤ 0.0786253 (rounded up) | CERTIFIED |
| S8 | 1002 | 2πΛ(0)=0.49401… | OWN | 2π·S6 | CERTIFIED; 0.49401719835247279040… |
| S9 | 815, 822 | σ_m nodes 5/7,…,167/170; e_i=1/(2^{i+3}−2); e_i nonincreasing, max 27/164; ς_i increasing; Q=10>1−ς_i | OWN/RAT | σ_m=1−m/(2^m−2) | CERTIFIED (exact) |
| S10 | 942 | c−R=−3·10^-6, σ#=1.25000275…, δ#=0.2500012499…, (eq:backlund_conditions), δ#∈[1/4,5/8], [c−R,c+R]⊂[−0.01,3] | OWN | σ#=c+(c−½)²/R, δ#=2c−σ#−½ (exact rationals) | CERTIFIED |
| S11 | 957 | closed form uses π, fifteen arccos values at rational points and fifteen square roots | OWN | θ_h plus θ_ς, θ'_ς for the 7 hinges (6 nodes and ς=1) | CERTIFIED (15 distinct arguments in (−1,1)) |
| S12 | 959, 405 | C_1=0.0978292318785…; 0.0978292318… | OWN | I_{e_E*}/(2π𝔡), 𝔡=log(R/(c−½)); closed form and exact antiderivative agree to 10^-60 | CERTIFIED; 0.09782923187851794633… |
| S13 | 959 | C_2=0.7213464797… | OWN | 1/(2𝔡) | CERTIFIED; 0.72134647976617563459… |
| S14 | 959, 965 | log(ζ(c)/ζ(2c))=12.6246665…; ≤ 12.62467 | OWN | Arb ζ at real points | CERTIFIED; 12.62466650920143470221… |
| S15 | 966 | σ#−½ ≤ 0.7501 | OWN | 0.75000275… | CERTIFIED |
| S16 | 970, 1634 | log ζ(σ#)=1.52498…, ≤ 1.52499 | OWN | Arb ζ(σ#); margin 6.44·10^-6 | CERTIFIED; 1.52498355868919915303… |
| S17 | 970 fn | the N=10^4 bound gives log ζ(σ#) ≤ 1.5249836 | OWN | Σ_{n<N} n^-σ + (N−½)^{1−σ}/(σ−1), Arb sum of 9999 terms; also checked ≥ ζ(σ#) | CERTIFIED; log of bound 1.52498355870053478247… |
| S18 | 974 | 640δ#−112 = 48.0008… > 0 | OWN | δ# exact | > 0 CERTIFIED; the digits FAIL (see F1) |
| S19 | 970 | E(T,δ#)/(2π) ≤ ½((640δ#−112)/(1536·299)+2^-10) < 0.00055 | ARITH | Bennett et al. Lemma 3.4 majorant (EXT) at T=100 | CERTIFIED; 0.00054053964604218924… |
| S20 | 976, 1628 | C_3(100)=10.598602…; with exact differences 10.598545…; 10.5986…, 10.5985… | OWN | the sum defined at lines 972-974 | CERTIFIED; 10.59860234834944286017…, 10.59854547332779879951… |
| S21 | 974 | "with the rounded values displayed, C_3(100) ≤ 10.5987" | OWN | with 12.62467, 0.7501: 10.598605175…; also with C_1, C_2, log ζ(σ#) rounded up: 10.598607226… | CERTIFIED (both variants) |
| S22 | 978, 1634 | 0.09783>C_1, 0.7214>C_2, 10.6>C_3(100); margins ≥ 3·10^-10 | OWN | margins 7.7·10^-7, 5.4·10^-5, 1.4·10^-3 | CERTIFIED |
| S23 | 972-974 | C_3(T) nonincreasing on [100,∞) | OWN | analytic: each term decreases; the majorant decreases because 640δ#−112>0 (S18) | CERTIFIED (analytic argument plus S18) |
| S24 | 978 | for e≤T≤100, 2.5167 < RHS of (eq:explicit_S) | ARITH | RHS increasing on [e,∞); value at T=e is 10.6978 | CERTIFIED |
| S25 | 978, 504, 510 | \|ϖ(T)\|/π ≤ 0.53/(πe) < 0.07 | OWN | 0.0620… | CERTIFIED |
| S26 | 519 | c,R→1: BW-profile quotient 0.10073687…, reflected profile 0.09782899… | OWN | Λ with the chord ½−σ+(27/82)σ on [0,½] (BW §3.1), and Λ(e_E) | CERTIFIED; 0.10073687033405844993…, 0.09782899554298332712… |
| S27 | 516 | the reflection lies below the chord (e_E convex) | OWN | piecewise linear vs affine function: checked at all kinks | CERTIFIED (exact) |
| S28 | 793 | ω_1∈[¼,0.505], ω_2∈[−0.005,¼], y≥49 | RAT | affine in σ | CERTIFIED |
| S29 | 806 | \|φ(ω_i,y)\| ≤ 0.108/y² ≤ 0.435/t² (0.505·0.256/2 + 0.043 ≤ 0.108) | OWN | log(1+x)≤x; alternating arctan series | CERTIFIED (exact rationals plus analytic steps) |
| S30 | 806 | sec²(½ ph z_i) ≤ 2.0005 | OWN | ph z_2 ≤ π/2+arctan(0.005/49); value 2.000204… | CERTIFIED |
| S31 | 806 | \|R(z_1)\|+\|R(z_2)\| ≤ 2·2.0005/(6t) ≤ 0.6669/t; 2·0.435=0.87 | OWN | DLMF bound (EXT) | CERTIFIED |
| S32 | 806 | 0.6669/t+0.87/t² ≤ 0.00690 (t≥98); e^{0.0069} < 1.0070 | OWN | decreasing in t, checked at t=98: 0.0068956892…; e^{0.0069}=1.0069238… | CERTIFIED |
| S33 | 829 | 1/6−27/164=1/492; e^{105/492} < 2/0.618; 105>66.7/2 | ARITH | HPY 0.618, PY 66.7 (EXT) | CERTIFIED |
| S34 | 829 | ζ(3) < 2 log 3 | OWN | Arb ζ(3) | CERTIFIED |
| S35 | 829 | \|t\|≤3: \|Ξ\| ≤ 4.243+2·4.243·3.606 < 34.9; RHS ≥ 2·10.5 log10.5 > 49 | OWN | √18, √13, log 10.5 as balls | CERTIFIED |
| S36 | 829 | constant 2 on every line: 0.618·e^{1/492·105}, 66.7/105, 1.546, 1.878, 1 | ARITH | as S33, S41 | CERTIFIED |
| S37 | 836-840 | 2(1+84.5/98²)^{1+27/164}(1+(84.5/98²+π/2)/log98) ≤ 2.7167 | OWN | each factor decreases in t (analytic), value at t=98 | CERTIFIED; 2.7166062888…, margin 9.37·10^-5 |
| S38 | 845 | 1.0070·2.7167 ≤ 2.74 | OWN | S32·S37 | CERTIFIED |
| S39 | 849 | (i) HPY alone for 3<\|t\|≤e^{577}: e^{577/492} < 2/0.618 | ARITH | margin 0.00533 (577 is the largest integer exponent that works) | CERTIFIED |
| S40 | 849 | (i) above e^{577} any C ≤ 1154 suffices | ARITH | C ≤ 2 log\|t\|, 2·577=1154 | CERTIFIED |
| S41 | 853, 1644 | (ii) constant 1.878 (precisely ≤ 1.87781, attained for m=9) on 3≤t≤T_m | OWN | yang_smallt_arb.py (Arb covering of [log 3, log T_m]) | CERTIFIED by that program (re-run: 1.54798, 1.68940, 1.77986, 1.83178, 1.86126, 1.87781) |
| S42 | 1644 | exponent split (1−σ_m)/3 = 1/(2K−2) + (m−3)/(6K−6), exponent > 0 | RAT | K=2^{m−1}, 4≤m≤9 | CERTIFIED |
| S43 | 354, 1045 | N_0(2π)=−1/8 | OWN | ball containing −1/8 (radius < 10^-60; exact by hand) | CERTIFIED |
| S44 | 439 | N_0(2πe)=7/8; k≥2 ⇔ τ_k ≥ 2πe | OWN | as S43; ½ < 7/8 ≤ 3/2 | CERTIFIED |
| S45 | 359 | g_{−1}=9.66… | OWN | θ(t)=Im lgamma(¼+it/2) − (t/2)log π (Arb); θ(9.66)<−π<θ(9.67); θ'>0 on [6.5,9.67] (grid of 4001 points plus an Arb trigamma bound for θ'') | CERTIFIED |
| S46 | 359 | \|ϖ\|/π < ½ at the Gram points | OWN | 0.53/(9.66π) < ½ | CERTIFIED |
| S47 | 994, 996 | γ_1 > 14 > 2π (> e) | EXT/OWN | Arb acb.zeta_zero(1) = 14.134725141734693790… (rigorous isolation) | CERTIFIED |
| S48 | 1185 | \|s_k+Δ_k\|<1 for γ_k ≥ 14 | OWN | 0.53/(14π) < ½ | CERTIFIED |
| S49 | 1028 | (1/π)arcsin(2^{−½}) = ¼ | OWN | ball | CERTIFIED |
| S50 | 1045, 1033, 547 | 2π∈[4,8], m_2=m_3=2, F(2π) ≤ −1/8+½ = 3/8 < ½; m_j=0 for j≤−1; m_j≤2 for j≤3; F < 7/8+½ < 3/2 on (0,2π] | OWN | m_j=⌊2^{j/2}⌋ (exact for even j, ball floor for odd j) | CERTIFIED |
| S51 | 1047 | t/(4π) > √(2t)/4 for t ≥ 4πe, since 4πe > 2π² | OWN | equivalence t > 2π² (analytic), 4πe=34.16 > 19.74 | CERTIFIED |
| S52 | 1163 | N_0(t)−¼√(2t) increases for t ≥ 2πe | OWN | derivative L(t)−1/(4√(2t)) increases; its value at 2πe is 0.11638… > 0 | CERTIFIED |
| S53 | 1178 | 2log2−log(2πe) = −1.45… | OWN | −1.45158270528945486472… | CERTIFIED |
| S54 | 727 | T≥9 ⇒ H−(H/√T)^{1/8} ≥ H−H^{1/8} ≥ 1 | OWN | H−H^{1/8} increasing; 3−3^{1/8}=1.85 ≥ 1 | CERTIFIED |
| S55 | 1114 | log(2+h log4T) ≤ 2 log(2+hL_T) for hL_T≥1, h≤1 | OWN | (2+v)² − (2+v+h log 8π) ≥ 6 − log 8π > 0 | CERTIFIED |
| S56 | 899 | η-family: σ#=5/4+3η/2, δ#=¼+η/2 ∈[¼,5/8], R/(c−½)=2, conditions hold, [−η,2+3η]⊂[−0.01,3] for 0<η<10^-2 | RAT | affine in η: exact checks at the endpoints | CERTIFIED |
| S57 | 314, 409, 1628 | crossing with Bellotti–Wong "log T > 2425.8386…" | ARITH | root of (1.7) − BW Cor 1.5 (bisection on balls; sign structure in constants_arb) | value CERTIFIED in (2425.8385, 2425.8386); digits FAIL (F2) |
| S58 | 330, 1622 | "improves only for log T > 2425.84" | ARITH | as S57 | FAILS (F3) |
| S59 | 1622 | (eq:explicit_N) smaller than Yang (4.29) as soon as log t > 933.5 | ARITH | crossing 933.46789604929362221… < 933.5; the +0.2/t_0 term only helps | CERTIFIED |
| S60 | 1628 | crossing "log t = 933.47…" | ARITH | as S59 | FAILS (F4) |
| S61 | 1316, 456 | Selberg constant at k=1: 1/(2π²); 4π²·1/(2π²) = 2 (leading constant 2 log log T/log²T) | ARITH | (2k)!/(k!(2π)^{2k}) | CERTIFIED |
| S62 | 1204, 1201, 1228, 1547 | Ψ_1=u²+1/12; general Ψ_j expansion (j=1..8); 1/12=∫x²; Σ(i−(m−1)/2)² = m(m²−1)/12 | RAT | polynomial identities, exact evaluation at deg+1 points | CERTIFIED |

### Trivial arithmetic and rounding checks (one row; all pass, asserted in the program)

10.2 = 10.7 − ½ (416); 10.6 + 0.07 ≤ 10.7 (978); 10.6 + 7/8 + 0.07 = 11.545 < 11.55 (504); 8.08344 − 7.20844 = 7/8 (508); 7.20844 + 0.07 ≤ 7.28 (510); 0.10076 − 0.09783 = 0.00293 and 0.1038 − 0.10076 = 0.00304 (525); 25/48 = 1/16 + 1/8 + 1/3 < 0.53 (776); 13² = 169, 169/2 = 84.5 (836); 1.87781 ≤ 1.878 ≤ 2, 1.546 ≤ 2 (829, 853); 2·577 = 1154 (849); Fujii parameters 7/10, 1/200 ≤ ½, 1/40 (549, 1140); (m²−1)/3 ≥ 1 for m ≥ 2 (1549); 0.09783 is the smallest A_1 in the table (405); 100 ≤ 30 610 046 000 (978).

For an upper bound only rounding up is safe. Every table conversion in Table tab:records (lines 492-504) is rounded up or exact:

- von Mangoldt: 0.43200 → 0.4320 (exact); 1.91662 → 1.9167 (up); 13.07873 → 13.0788 (up).
- Grossmann: 0.29062 → 0.2907 (up); 1.7862 (exact); 6.13695 + 7/8 = 7.01195 → 7.0120 (up).
- Backlund: 4.350 + 7/8 = 5.225 (exact).
- Trudgian 2012: 1.998 + 7/8 = 2.873 (exact).
- Bellotti–Wong: 7.20844 + 7/8 = 8.08344 (exact).
- This work: 11.545 → 11.55 (up).

## B. FAILURES (the paper is not modified)

All four are display or rounding-convention problems. None affects a proof: every inequality the proofs use is certified above.

- **F1 (line 974).** "640δ#−112 = 48.0008…". The certified value is 48.00079999984000079999…. As truncated digits the display should read 48.0007…; it can also be written as ≈48.0008 without the ellipsis. The claim used, 640δ#−112 > 0, is certified.
- **F2 (lines 314, 409, 1628).** "log T > 2425.8386…". The certified crossing is 2425.83858012258894712627….
  - As truncated digits the paper should write 2425.8385…; it can also write 2425.83858… or ≈2425.8386 without the ellipsis.
  - Read literally, "smaller exactly/only when log T > 2425.8386" is false on (2425.83858…, 2425.8386].
- **F3 (lines 330 and 1622).** "improves upon theirs only for log T > 2425.84". This is false: (1.7) is already smaller than Bellotti–Wong on (2425.83858…, 2425.84]. An "only for" threshold must not exceed the crossing, so the paper should say "only for log T > 2425.83" (or 2425.8385…).
- **F4 (line 1628).** "the crossing point log t = 933.47…". The certified value is 933.46789604929362221420…. As truncated digits this is 933.46…; the paper should write 933.4679… or ≈933.47. The claim at line 1622, "as soon as log t > 933.5", is correct (certified).

## C. EXTERNAL-QUOTED (checked only as quoted; constants taken as given)

- Bounds for ζ:
  - Hiary–Patel–Yang 0.618|t|^{1/6}log|t| (3<|t|≤e^{105}); Patel–Yang 66.7|t|^{27/164}.
  - Yang 1.546|t|^{1/(2^m−2)}log|t|; Patel log|t| on σ=1.
  - Hiary–Leong–Yang (3070, 3.69·10^8, log|t|−0.45); 58.096 (Leong Lemma 5); Bellotti 70.6995 and exponent 4.43795; Revers 0.611.
- Disc and constant-term inputs:
  - Bellotti–Wong c=1.000225, r=1.000605.
  - Bennett et al. majorant (640d−112)/(1536(3T−1))+2^-10 with d∈[¼,5/8], T≥5/7.
  - Platt/BW (1.2): |S|≤2.5167 for T ≤ 30 610 046 000.
- Table and literature constants:
  - The rows of Table tab:records and the source values in its caption: 0.43200, 1.91662, 13.07873, 0.137, 0.443, 4.350, 0.29062, 1.7862, 6.13695, 0.17, 1.998, 0.111/0.275, 9.3675/9.4925, Rosser 2.4630, 3.165, 0.2573, 0.24460, 8.08344, 7.20844, 1.68845, 1.50956.
  - Leading coefficients 0.112/0.111, 0.110, 0.1038, 0.10076; Yang (4.29) 0.11, 0.29, 2.29, 0.2/t_0.
- Other analytic inputs: Yang's Q_0=1.31 and the threshold T_m of (3.4); DLMF sec²(½ph z)/(12|z|); Bourgain's pair (13/84, 55/84); Fiori Cor. 3; Fujii's exponents; Montgomery–Vaughan.

## D. NOT CERTIFIABLE (and why)

- **Unspecified constants.** Asymptotic statements with absolute but non-explicit constants or T_0 cannot be checked by arithmetic: Theorem thm:sublevel and Corollary cor:proportion (C, C', C'', T_0, C' = 8πC); Lemmas lem:gaps and lem:fourth; #K_T ≥ T log T/(8π) for T ≥ T_0 (line 1174, with an O(log T) term of unknown constant); Proposition prop:s_meansquare; Theorem thm:meansquare; Section 7 (Propositions and Theorems on d_k^C).
- **Purely analytic steps.** These have no numerical content, so there is nothing to put a ball on:
  - log(1+x) ≤ x; arctan x ≤ x; √(1+x) ≤ 1+x/2.
  - log(3+x)/log(2+x) decreasing (line 737).
  - |s±iT−1| ≤ √(9+(T+2)²) ≤ T+3 for T ≥ 2.
  - The (log log u)' argument (970); the footnote AM-GM step; Λ(e) ≥ Λ(0).
  - The symbolic identities y log y − y − (t/2)log π = (t/2)log(t/(2πe)) and N_0(2T)−N_0(T) = (T/2π)(log T + 2log2 − log 2πe).
- **The mpmath program's own claims.** Appendix A, line 1634, says the floating-point evaluations agree to more than 20 digits. This describes constantes_v5.py and is not certifiable as such. The values themselves are now certified by Arb (S2, S12–S22, S57–S60).

## E. Notes

- constants_arb.py, line 120, bounds the χ factor with ε = (1/3 + 2.0005/6)/t + 0.87/t². That uses sec² < 2 for z_1 and is slightly sharper than the paper's written chain, which uses 2·2.0005/(6t) ≤ 0.6669/t. The paper's own chain (0.6669/t + 0.87/t² ≤ 0.0069, e^{0.0069} < 1.0070, 1.0070·2.7167 ≤ 2.74) is certified separately here (S31, S32, S38), so nothing in the paper depends on the difference.
- Λ(e_B) and I_{e_E*} now have three independent rigorous evaluations: the hinge closed form, the exact piecewise antiderivative, and acb.integral. They agree to 10^-60.
