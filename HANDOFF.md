# Handoff — Lean (PaperMath) y constantes del Teorema 1.3 — v3, 2026-10-27

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
3. `hC1`: `(1/(2π𝔡)) ∫₀^π 𝔢_E^*(c + R cos θ) dθ ≤ 0.0978293`. Valor real 0.0978292318; margen 7.7·10⁻⁷.
   Ruta: integral exacta por trozos (el integrando es lineal a trozos en `cos θ`: nodos `ς_i` ⇒ ángulos
   `arccos((ς_i − c)/R)`), con cotas racionales de arccos y de sin a 9–10 cifras (ir a `Common/`), y la
   integral `∫ (a + b cos θ) dθ = a θ + b sin θ` en cada trozo. Hace falta `intervalIntegral` de funciones
   lineales a trozos en `cos`; `eStar` está definido con `max 0 (σ − ς_i)` (`Profile.lean`).
4. Lema 4.3 (`hchi`), la capa ζ del Teorema 1.5 (`ZetaInputs` con los ceros de `riemannZeta`, Lema 4.1,
   Teorema 3.1), el núcleo Selberg–Fujii (`FujiiA`, `FujiiB`), `I.zeta3` (|ζ(3+it)| ≤ 1.21, trivial desde
   `Common.ZetaSeries`).
5. Para la revista: release etiquetada + DOI de Zenodo; citar el commit en el Apéndice B.
