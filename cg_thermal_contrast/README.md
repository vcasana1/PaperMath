# Cg_Thermal_Contrast

Nota "The log-sine constant C_g as the sharp constant in the Ramsey contrast of a thermal cavity mode"
(Víctor Casaña-Giner). Versiones: v1 a v4, cada una con .tex, .txt (copia literal del .tex) y .pdf.
La versión vigente es la v4. Cada .tex compila desde esta carpeta con tres pasadas de pdflatex
(las figuras PNG están aquí) y lleva tras \end{document} las reglas y el comprobador CorrectVCG.

## Cómo se genera cada versión
- v1: escrita directamente; números en cg_tables.py, figuras con figures_note_v1.py y fig_bound_v1.py
  (usan cp_eval.py, zeros_G.txt y zeros_A.txt).
- v2: desde la v1 con make_v2_from_v1.py y make_v2_stage2.py (build_v2.sh), primer informe de revisión.
- v3: desde la v2 con make_v3_from_v2.py, segundo informe (revisión menor).
- v4: desde la v3 con make_v4_from_v3.py (build_v4.sh; entrada Cg_Thermal_Contrast_v3.tex como RECEIVED): enfoque y bibliografía
  según la revisión de literatura física; nueva Sección 6 (Proposición 6.1, coeficientes de Fourier de log V en el primer periodo).
- fix_tips.py pone en los tooltips los números de la compilación (lee el .aux).
- allowed_labels_v2.txt, allowed_labels_v3.txt, allowed_labels_v4.txt: bloques autorizados en la comprobación de cambios no pedidos.

## Cálculos y salidas
- cg_tables.py -> cg_tables_output.txt: C_g, constantes exp(-s G(s)), Tabla de V_1, resto R(tau), producto P(N).
- cg_tables_v2.py -> cg_tables_v2_output.txt: c_1(1), Tabla 2 (Poisson y térmicos desplazados), umbrales de amortiguamiento.
- damping_check_v2.py (usa lst_common.py) -> damping_check_v2_output.txt: cota de amortiguamiento frente a la forma cerrada.
- fourier_check_v4.py (usa lst_common.py) -> fourier_check_v4_output.txt: Proposición 6.1 (térmico desplazado, muestreo,
  amortiguamiento, desintonía, distribución p0=2/3, p1=1/3).
- figures_note_v1.py -> figures_note_v1_output.txt; fig_bound_v1.py -> fig_bound_v1_output.txt.
- exploration/: cálculos previos a la nota (eficiencias de Fisher frente a la línea de vacío, horquilla de C_g,
  modelo amortiguado, sesgo por amortiguamiento), con sus salidas *_output.txt.

Cada .py lleva su copia .py.txt. Python 3 con numpy, scipy, mpmath y matplotlib.
