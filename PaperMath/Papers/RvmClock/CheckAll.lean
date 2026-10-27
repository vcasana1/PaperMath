import PaperMath.Papers.RvmClock.Transfer
import PaperMath.Papers.RvmClock.Construction
import PaperMath.Papers.RvmClock.Mertens
import PaperMath.Papers.RvmClock.MeanValue
import PaperMath.Papers.RvmClock.Inputs
import PaperMath.Papers.RvmClock.Sublevel
-- Lemma 7.2 (discrete maximal inequality)
#check @RvmClock.maximal_cube
#check @RvmClock.maximal_cube_36
-- Bathtub inequalities
#check @RvmClock.bathtub_right
#check @RvmClock.bathtub_left
-- Theorem 7.3 (sublevel transfer), article v7 form
#check @RvmClock.transfer
-- article v6 forms
#check @RvmClock.transfer_24
#check @RvmClock.transfer_36
#print axioms RvmClock.maximal_cube_36
#print axioms RvmClock.transfer
#print axioms RvmClock.transfer_24
#print axioms RvmClock.transfer_36
-- Section 7.1 and Proposition 7.1 (prime-corrected clock)
#check @RvmClock.abs_PhiM_le
#check @RvmClock.abs_Phi_le_sqrt
#check @RvmClock.continuousOn_F
#check @RvmClock.F_two_pi_le
#check @RvmClock.volume_Sub_lt_top
#check @RvmClock.xClock_pos
#check @RvmClock.xClock_lt_succ
#check @RvmClock.Sub_subset_two_tau
#check @RvmClock.budget_le_two_sqrt
#print axioms RvmClock.xClock_lt_succ
#print axioms RvmClock.xClock_pos
#print axioms RvmClock.Sub_subset_two_tau
#print axioms RvmClock.budget_le_two_sqrt
-- Mertens-type bounds (replace Theorem 3.10 in Lemma 7.6)
#check @RvmClock.sum_log_div_le
#check @RvmClock.sum_inv_prime_le
#check @RvmClock.nth_prime_le_sq
#print axioms RvmClock.sum_log_div_le
#print axioms RvmClock.sum_inv_prime_le
#print axioms RvmClock.nth_prime_le_sq
-- Montgomery–Vaughan (ported from zeta23) and the mean value theorem (Theorem 3.9)
#check @Zeta23.MV.mv_hilbert
#check @RvmClock.mean_value
#print axioms Zeta23.MV.mv_hilbert
#print axioms RvmClock.mean_value
-- Lemma 7.5 (third moment of the gaps), conditional on Fujii (b) as an explicit hypothesis
#check @RvmClock.sum_cube_le
#check @RvmClock.Ordinates.sum_D_le_two_vol
#print RvmClock.ZetaInputs.FujiiB
#check @RvmClock.ZetaInputs.vol_A_le
#check @RvmClock.ZetaInputs.gaps_third_moment
#print axioms RvmClock.ZetaInputs.gaps_third_moment
-- Fourth moments of prime Dirichlet polynomials (𝒟₁, 𝒟₂ in Lemma 7.6)
#check @RvmClock.prime_fourth_moment
#print axioms RvmClock.prime_fourth_moment
-- Expansion of the finite Euler phase (proof of Lemma 7.6)
#check @RvmClock.eulerArg_expand
#check @RvmClock.PhiM_expand
#print axioms RvmClock.PhiM_expand
-- Lemma 7.6 (fourth moment of the counting error), conditional on Fujii (a) as an explicit hypothesis
#print RvmClock.primesLt
#check @RvmClock.mem_primesLt
#print RvmClock.zp
#print RvmClock.ZetaInputs.FujiiA
#check @RvmClock.block_arith
#check @RvmClock.A_moment
#check @RvmClock.fourth_moment
#print axioms RvmClock.fourth_moment
-- Theorem 1.5 and Corollary 1.6, conditional on FujiiA, FujiiB, Titchmarsh (Theorem 3.1)
#print RvmClock.ZetaInputs.Titchmarsh
#print RvmClock.ZetaInputs
#print RvmClock.ZetaInputs.S
#check @RvmClock.F_lt_low
#check @RvmClock.F_gt_high
#check @RvmClock.xClock_eq
#check @RvmClock.Q_bound
#check @RvmClock.gap_window
#check @RvmClock.card_KT_ge
#check @RvmClock.sublevel_mean_square
#check @RvmClock.sublevel
#check @RvmClock.proportion
#print axioms RvmClock.sublevel
#print axioms RvmClock.proportion
