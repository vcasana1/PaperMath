# Explicit hybrid bound (kernel + Jensen discs with explicit zeta bounds), all T >= T1
Goal: |N(T) - main(T)| <= A1 log T + B loglog T + A3 for T >= T1, combined with the certified kernel-only lines
(../family) for 1 <= T <= T1.  Explicit inputs (no zero verification):
- Hiary, Patel, Yang (2024): |zeta(1/2+it)| <= 0.618 t^{1/6} log t, t >= 3.
- Yang (2023, arXiv:2301.03165, Thm 1.1): |zeta(sigma_k+it)| <= 1.546 t^{1/(2^k-2)} log t, sigma_k = 1-k/(2^k-2), k >= 4, t >= 3.
- Trudgian (2014, Bull. Aust. Math. Soc. 89): |zeta(1+it)| <= (3/4) log t, t >= 3.
- Trudgian (2014, JNT, arXiv:1208.5846), Lemma 3: Phragmen-Lindelof with logarithms (extension of Rademacher), applied
  to (s-1)zeta(s) between consecutive lines.
- Jensen's formula; |zeta(s0)| >= zeta(2c)/zeta(c) at the centre; |zeta(sigma+it)| <= zeta(sigma) for sigma > 1.
Status: optimiser opt_hybrid_line.py (uncertified estimates). Pending: rigorous constants for |t| < 3 on the lines
(PL hypothesis on whole lines), the corrections log|Q+s| - log t, Arb certification of a_k, g_k, J_k and of the
kernel+disc inequality (../hybrid_asymptotic/certify_hybrid.py), C_zeta (../family/cz_gen.py), sup F (../family/elem_gen.py).
