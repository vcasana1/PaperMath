# HANDOFF — explicit and asymptotic bounds for S(T), Turing–Amberger–Bellotti–Wong method (31 Oct 2026)

Folder: `numerics/explicit_S_turing/` of this branch (`explicit-S-turing`). Python + Arb certificates; not Lean.

## Context
- Paper casanya_ordinal_primes (v55 submitted to IJNT, 30 Oct 2026). v57 (docs/) adds Amberger 2025 (arXiv:2510.27444,
  0.097 log T + 5.081) and Bellotti–Wong 2026 (arXiv:2606.31441, Cor. 1.3: |N(T) − (T/2π)log(T/2πe)| ≤ 0.0946 log T + 5.746
  and ≤ 0.097 log T + 4.954, T ≥ 1), and removes the false record claims.
- Turing-type identity: N(T) = (1/π)(2 arg ξ(1/2+d+iT) − arg ξ(1/2+2d+iT)) + (1/2π) Σ_ρ f(b_ρ, T−γ_ρ),
  f(b,t) = 2atan((d+b)/t)+2atan((d−b)/t)−atan((2d+b)/t)−atan((2d−b)/t), b = 1/2 − β.
- Kernel U = Σ c_ι [F_ι(d+b,t)+F_ι(d−b,t)], F_Rj = Re(x+it)^{-j}, F_Ij = −Im(x+it)^{-j}; need f ≤ U on 0≤b≤1/2, t≠0.
- Explicit bound: |N − main| ≤ A1 log T + C_ζ + sup_T F; C_ζ = Σ Λ(n) n^{-σ1} hypot(A0,B0)(log n) (combined cos/sin per
  prime power); F = exact elementary part (Γ, s(s−1), main term) minus A1 log T.

## Certified results (Arb, 256 bits; no Platt; ψ(x) < 1.03883x of Rosser–Schoenfeld only for the C_ζ tail)
1. Seven lines for N(T), all T ≥ 1 (family/line_L*/summary.json), L = log T:
   0.20176L+1.505 | 0.10823L+2.382 | 0.09473L+3.075 | 0.09349L+3.237 | 0.09152L+3.776 | 0.09012L+4.593 | 0.08844L+6.988,
   active on L ∈ [0,9.4],[9.4,51.3],[51.3,130.6],[130.6,273.6],[273.6,583.6],[583.6,1425.6],[1425.6,∞).
   Min gap to BW: 1.996 at L ≈ 51.4. Single lines below BW for all T ≥ 1: 0.09349L+3.237 and 0.09012L+4.593.
2. Same slopes for S(T), all T ≥ 1, constants 0.979 | 1.498 | 2.187 | 2.350 | 2.887 | 3.704 | 6.099.
   Previous: BW2025 0.10076L+0.2446 log L+7.208; BW2026-derived 0.0946L+6.691; v55 0.09783L+0.7214 log L+10.6.
3. BW's own kernels (2.43),(2.44): min(0.0946L+5.138, 0.097L+4.507) (explicit_allT_BWkernels/).
4. Hybrid asymptotic (kernel + Jensen discs + Bourgain profile): limsup|S|/log T < 0.0775422804104 (m=10), below
   Λ(0)=0.0786253 (Lindelöf floor of Backlund's method). Grid (uncertified): 0.07603 (m=10, 1045 discs), 0.07515 (m=20).

## Update 31 Oct 2026 (evening)
5. CERTIFIED (Arb): limsup |S|/log T <= C_H < 0.0748871398241. m=10, d=0.9, 85 Jensen discs (centres up to log 5,
   vertical offsets |v| <= 2), mu-profile = ANTEDB Table 6.2 (Tao-Trudgian-Yang; profile_tty.py). Data:
   hybrid_asymptotic/expl_m10_d0.90_vwide_T_eta0.001_fix.json (LP solution with c_R1 + 2e-4: first certification found a
   true violation -8.9e-5, cert_m10T_vwide.txt); certificate hybrid_asymptotic/cert_m10T_vwide_fix.txt.
   Uncertified explorations: m=20 TTY 0.07404 (cut planes not converged), explicit profile E 0.07571, Bourgain 0.07531.
6. Per-prime phase maximum in C_zeta (Amberger 2025, Lemma 2.7; cz_gen_pp.py, p <= 1000 certified on 4096-point grid +
   Lipschitz): all lines recertified (family/line_*/summary_pp.json). Best single line for all T >= 1:
   |N - main| <= 0.08399 log T + 5.202, |S| <= 0.08399 log T + 4.318 (line_C400, m=10, d=0.85).
   Envelope beats Bellotti-Wong by >= 2.232 for all T >= 1.
7. Attribution correction: the combined cos/sin Euler constant is Amberger's (per prime, max over the phase); own:
   hybrid method, LP/SOCP optimisation, Arb certification.
8. In progress: explicit hybrid (hybrid_explicit/: Hiary-Patel-Yang 0.618 t^{1/6} log t, Yang 1.546 t^{1/(2^k-2)} log t,
   Trudgian (3/4) log t, Trudgian JNT 2014 Lemma 3 PL; PL hypothesis for |t|<=3 checked with Q=3), lower-slope lines
   (sweepD candidates 0.08381 L + 5.302 at L*=6000, uncertified).

## Code (family/)
opt_line.py (SOCP optimizer), sweep.py, pick.py, certify_line.py, cz_gen.py (exact sum n ≤ 1e8 + tail with non-increasing
step majorant on [log N0, 2000], certified monotonicity beyond), elem_gen.py (mode N or S), finalize_line.py.

## Next steps
1. Closed formula α log T + β√(log T) + γ above the seven-line minimum (certified comparison).
2. Longer kernels (m ≥ 6) for slopes below 0.0884; certify the hybrid m=20 (≈0.0752).
3. Write-up (v58) with attribution: identity and kernel method = Amberger / Bellotti–Wong; own = hybrid (Jensen discs +
   subconvexity), LP/SOCP optimisation, combined Euler constant, exact elementary part. BW announce optimisation as future
   work (their §3): consider an arXiv preprint soon.
4. Theorems A (RH, pointwise) and D (unconditional, density one): see the other two handoff notes in this folder.
