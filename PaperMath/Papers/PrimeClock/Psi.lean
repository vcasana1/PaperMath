import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

set_option linter.style.header false

/-!
# Formalización de Prime Corrected Clock

Formalización de la función Ψ_j definida en la ecuación (4.2)
del artículo Prime Corrected Clock.
-/

namespace PrimeClock

/--
La función Ψ_j de la ecuación (4.2):

Ψ_j(u) =
  ((1/2 + u)^(2j+1) + (1/2 - u)^(2j+1)) / (2j+1).
-/
noncomputable def psi (j : ℕ) (u : ℝ) : ℝ :=
  (((1 / 2 : ℝ) + u) ^ (2 * j + 1) +
    ((1 / 2 : ℝ) - u) ^ (2 * j + 1)) /
    ((2 * j + 1 : ℕ) : ℝ)

/-- La función Ψ₁ como caso particular de Ψ_j. -/
noncomputable def psiOne (u : ℝ) : ℝ :=
  psi 1 u

/-- Identidad Ψ₁(u) = u² + 1/12 de la ecuación (4.2). -/
theorem psiOne_eq (u : ℝ) :
    psiOne u = u ^ 2 + 1 / 12 := by
  norm_num [psiOne, psi]
  ring

end PrimeClock
