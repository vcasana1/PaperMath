import PaperMath

/-!
# Audit: axioms of the main results

Run with `lake env lean Audit.lean` (after `lake build`). Every `#print axioms` below must list only
`propext`, `Classical.choice`, `Quot.sound` (the standard axioms of Mathlib); `sorryAx` or any other axiom
is a failure. `scripts/audit.sh` checks this automatically.
-/

-- Common
#print axioms Common.ZetaSeries.zeta_one_add_le
#print axioms Common.ZetaSeries.zeta_two_add_ge
#print axioms Common.ZetaTail.zeta_le_partial_add_tail
#print axioms Common.ZetaTail.rpow_neg_add_le
#print axioms Common.LogBounds.log_one_sub_le
#print axioms Common.TrigBounds.sin_le_partial
#print axioms Common.TrigBounds.arcsin_le_of_le_sin
#print axioms Zeta23.MV.mv_hilbert

-- Papers/RvmClock, Branch A (Theorems 1.5, 1.6 and their lemmas)
#print axioms RvmClock.maximal_cube_36
#print axioms RvmClock.transfer
#print axioms RvmClock.transfer_36
#print axioms RvmClock.xClock_lt_succ
#print axioms RvmClock.Sub_subset_two_tau
#print axioms RvmClock.budget_le_two_sqrt
#print axioms RvmClock.mean_value
#print axioms RvmClock.sum_log_div_le
#print axioms RvmClock.nth_prime_le_sq
#print axioms RvmClock.ZetaInputs.gaps_third_moment
#print axioms RvmClock.fourth_moment
#print axioms RvmClock.sublevel
#print axioms RvmClock.proportion

-- Papers/RvmClock, Branch B (Theorem 1.3)
#print axioms RvmClock.ZetaLines.lemma_4_4
#print axioms RvmClock.Backlund.master
#print axioms RvmClock.Explicit.thm_1_3
#print axioms RvmClock.Explicit.explicit_N
#print axioms RvmClock.Thm13.theorem_1_3
#print axioms RvmClock.ZetaConst.log_zeta_ratio_le
#print axioms RvmClock.ZetaSigS.zeta_sigS_le
#print axioms RvmClock.ZetaSigS.log_zeta_sigS_le
#print axioms RvmClock.Thm13.theorem_1_3_zeta
#print axioms RvmClock.C1.integral_eStar_eq
#print axioms RvmClock.C1.C1_le
#print axioms RvmClock.C1.theorem_1_3_numeric

-- statements of the main results, for the record
#check @RvmClock.transfer
#check @RvmClock.sublevel
#check @RvmClock.proportion
#check @RvmClock.Thm13.theorem_1_3
#check @RvmClock.Thm13.theorem_1_3_zeta
#check @RvmClock.ZetaConst.log_zeta_ratio_le
#check @RvmClock.ZetaSigS.log_zeta_sigS_le
#check @RvmClock.C1.C1_le
#check @RvmClock.C1.theorem_1_3_numeric
