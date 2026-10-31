# Review of casanya_ordinal_primes_v49.tex

## Verified so far (incremental)
- L340: "see Section~\CGref{subsec:literature}" for the Kargin enumeration: the enumeration caveat is at L466-471, which lies in Section 1.2 (subsec:results, starts L365), not 1.3 (subsec:literature starts L482). [to confirm no other Kargin mention in 1.3]
- L554: exact excursion statement "changes only for the levels k-1/2 between these two values": at level = max_I F the measure of {F<max}∩I can be < |I| and differ between the two functions; precise range is min < k-1/2 <= max. Minor imprecision.
- L521: split 0.0000231+0.0029078 = 0.0029310 = 0.10076-0.09782899, not 0.10076-0.09783 (=0.00293); the residual 0.0000010 is the fixed-c,R/rounding cost. Minor.
- L931/933 (proof of Cor. bourgain): "a constant A_{eps'}>=1" then the argument of Lemma explicit_zeta for |t|<=3 is invoked; that argument needs RHS >= 34.9, but with A=1 and j=8 (kappa_8=0) the RHS minimum is 10.5*log 10.5 = 24.7 < 34.9. Need A_{eps'}>=2 (as in Lemma explicit_zeta). Gap (minor, trivially fixable).
- Checked OK: Lemma varpi constants (25/48), Lemma chi (0.6669/t+0.87/t^2<=0.0069), Lemma explicit_zeta (2.7167, 2.74, 34.9<49), sigma^sharp, delta^sharp (0.2500012499...), C2=0.7213464797, log(zeta(c)/zeta(2c))=12.6246665, E-term <0.00055, Lambda(0) closed form, Bourgain nodes (A-process recomputed), BW crossover 2425.8385 (both sides =7.1077), 2*pi*Lambda=0.6083129, 10.6+7/8+0.07, 7.20844+0.07<7.28.
- CONFIRMED L340 cross-ref: only Kargin mentions are L340 and L466-471 (both Sect. 1.2/intro); fix -> subsec:results.
- Kargin arXiv v2 checked: zeros with beta_k>=1/2, gamma_k>0, nondecreasing; window I_N = Z cap [N, N+floor(N^theta)-1]; moments converge (Thm 1.1(ii)). L471 "N<k<=N+N^theta" off by one (typo-level).
- L782 Remark 4.2 "constant 0.53 is needed only for (1.8)": also needed for |varpi|/pi<1/2 at Gram points (L361, every k>=1) and Remark 7.7 (|s_k+Delta_k|<1, gamma_k>=14). Inconsistency (minor).
- L551 item 1: mean square of Im of prime sum over (X,Y) needs the same real/imag-part step (Im P)^2 = |P|^2/2 - Re(P^2)/2 that v49 added only to item 2. Gap (minor).
- L1704 App. B row Selberg: omits use with every k in Remark 8.5 (stated at L763). Inconsistency.
- L344 intro: Gonek's C_3 and Phi(t) "in his notation" clash with C_3(T) and Phi (1.11); the local-symbol list L582 does not include this paragraph. Notation (minor).
- Sect. 9: delta_k, b_k, eps_k, n_T, sans D,B,E, d_k^C not in notation table; b listed as window endpoint; k_1,k_2,F declared local to Sect. 8 but reused in proof of Thm 9.3; c_{j,l} in Remark 8.5 undefined. Notation (minor).
- L863 / L983: section titles produce hyperref PDF-string warnings (bookmarks "A disc-based estimate for S(T)" loses $, "tau_k" subscript). Cosmetic.
- App. A: constantes_v5 prints 2425.8386 and 933.4679 (rounded), text quotes 2425.8385..., 933.4678... (truncated, matched by certify). Consistent, cosmetic.
- Checked OK: Lemma maximal (rising sun, weak 2, strong 24), Theorem transfer, Lemma gaps, Lemma fourth incl. v49 budget paragraph, proof Thm 1.5, Thm 8.1 + Psi_j, Prop 8.4, Thm 1.7, Remark 8.5 induction (Holder exponents T^{1-i}(loglog)^{j-i/2} correct), Sect. 9 (polarization, certificate m(m^2-1)/12), Prop 6.2, real-part step item 2, all constants vs certify output, label numbers in certify output vs aux.
