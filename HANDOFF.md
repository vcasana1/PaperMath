# Handoff — Lean (PaperMath) y constantes del Teorema 1.3 — v4, 2026-10-27

Sustituye a `claude/HANDOFF-rvm-clock-lean-constantes-v2.md` del proyecto de Claude. Leer junto con
`claude/HANDOFF-rvm-clock-envelope-v10.md`.

## Dónde está todo
- **Repositorio canónico del Lean: `vcasana1/PaperMath`**, rama `main` (público; cambiar a privado si se quiere
  hasta el envío). Proyecto Lake completo; CI en GitHub Actions (`lake exe cache get && lake build &&
  scripts/audit.sh`), que además publica los logs en la rama `ci-logs` (`run-<id>/build.log`,
  `Audit_output.txt`) para leerlos sin descargar artefactos.
- Mac: `~/Lean/PaperMath/` tiene la misma estructura (escrita el 2026-10-27); faltan solo
  `.github/workflows/ci.yml` (ruta protegida) y el directorio `.lake` (lo regenera `lake exe cache get`).
  Las carpetas antiguas `PaperMath/RvmClock/` y `PaperMath/Zeta23Port/` del Mac siguen ahí, ya no las usa nadie.
- `REVIEWOWNPAPERS_OCT26`, rama `rvm-clock-articulo-y-lean`, `LEAN_RVM_CLOCK/`: copia histórica + bloque 12 +
  `PaperMath_2026-10-27/` con los ficheros nuevos.
- Sandbox del Mac: la VM de Claude quedó con los dos discos llenos (no es el Mac). En la nube funciona
  compilar desde cero (toolchain x86_64 de GitHub; Mathlib solo desde fuente, 3–4 h), pero lo práctico es
  **compilar en el CI de GitHub** (≈ 12 min por push con la caché) y leer `ci-logs`.

## Hecho (2026-10-27)
- Paso 0 completo: `Common/` + `Papers/`, `Audit.lean`, `HYPOTHESES.md`, `README.md`, CI. Primer CI verde:
  run 40426476309, commit `341d289`; `Audit_output.txt` en el repo.
- Punto 1: `RvmClock.Thm13.theorem_1_3_zeta` (`Papers/RvmClock/Thm13Zeta.lean`): `zc, z2c, zs` instanciadas con
  `riemannZeta`; `hzc`, `hz2c`, `hzeta`, `hzs` eliminadas.
- Punto 2: `RvmClock.ZetaSigS.log_zeta_sigS_le` (`Papers/RvmClock/ZetaSigS.lean`): `log ζ(σ♯) ≤ 1.52499`.
  Ruta: `Common.ZetaTail.zeta_le_partial_add_tail` (punto medio por AM–GM, N = 50) + 48 cotas racionales de
  12 cifras generadas con `gen_sigs.py` (ε₀ = σ♯ − 5/4 = 1375007/500002500000 exacto) + Taylor para el log.
  Cota: ζ(σ♯) ≤ 4.595076613723 (real 4.5950680197), log ≤ 1.5249854297 (margen 4.6·10⁻⁶).
- Reutilizable en `Common/`: `ZetaSeries` (ζ(1+s) ≤ 1+1/s, ζ(2+ε) ≥ π²/6 − εK, 1 ≤ ζ(s)), `LogBounds`
  (Taylor con resto para log(1−x), log 3), `ZetaTail` (punto medio, `rpow_neg_add_le`), `Zeta23Port`.

## Pendiente (máxima exactitud, sin aflojar umbrales)
3. (hecho) `hC1 ≤ 0.0978293`: `RvmClock.C1.C1_le` (`Papers/RvmClock/C1.lean`, generado por
   `scripts/gen_c1.py`). Integral exacta: `gE` es suma de términos `max 0 (σ − ς_i)`, cada uno integra a
   `(c − a)θ_a + R sin θ_a` (`int_max_a`, `int_max_b`); `θ_a = π/2 + arcsin((c − a)/R)` y
   `sin θ_a = √(1 − x²)`; 15 arcsin y 15 raíces acotados a 12 cifras con `Common.TrigBounds` (serie alternada
   de `sin`, `Antitone.alternating_series_le_tendsto`). Valor 0.0978292318785, margen 6.8·10⁻⁸ (no 7.7·10⁻⁷).
   `RvmClock.C1.theorem_1_3_numeric`: Teorema 1.3 solo con hipótesis de la literatura. CI run 40470337612.
4. (hecho) `I.zeta3` y la ecuación funcional: `ZetaFacts.lean` (`zeta3`, `chi`, `functional_equation`,
   `theorem_1_3_lit`; CI run 40472400023, commit 2077ae4).
5. Lema 4.3 (`hchi`, ahora enunciado para `ZetaFacts.chi`): necesita Stirling con resto explícito para
   `Complex.Gamma` (DLMF 5.11(ii)); Mathlib no lo tiene. Las demás hipótesis de `theorem_1_3_lit` son
   literatura (HPY, PY, Yang, Patel, Titchmarsh (2.1.4), Fiori, Bellotti–Wong 3.5, Platt) y no se formalizan.
6. La capa ζ del Teorema 1.5 (`ZetaInputs` con los ceros de `riemannZeta`, Lema 4.1, Teorema 3.1); el núcleo
   Selberg–Fujii (`FujiiA`, `FujiiB`) no.
7. Para la revista: release etiquetada + DOI de Zenodo; el Apéndice B de la v11 del artículo cita el commit 2077ae4.
