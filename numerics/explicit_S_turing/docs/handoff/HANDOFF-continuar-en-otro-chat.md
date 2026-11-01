# Traspaso: nota Zenodo "Turing–Jensen" (casanya_turing_jensen) — estado al 1 Nov 2026

Repositorio: `vcasana1/PaperMath`, rama `explicit-S-turing`, carpeta `numerics/explicit_S_turing/`.
Nota: `docs/zenodo_note/` (fuente `body.tex` + ficheros generados; se compila con `build.py vN`, que produce
`casanya_turing_jensen_vN.pdf`, `_l.tex` (autocontenido) y `.txt`). Última entregada: v11 (1 Nov 2026, commit 2668fa8; revisión larga de la v10 aplicada: texto, tooltips y apéndices;
ningún programa de certificación ni JSON tocado, certificados y constantes idénticos a v8). Handoff largo: `HANDOFF-turing-explicit-S.md`.

## Reglas del autor (obligatorias)
- Preguntar antes de cambiar nada que no sea una corrección evidente; nunca inventar; impersonal en el artículo.
- Nunca usar la palabra "clock". Nada de verificación numérica de ceros (Platt). Rango de interés: todo T >= 1, o T -> infinito.
- Cada entrega: pdf + tex + txt (misma numeración de versión nueva), zip plano para Zenodo (pdf, tex, txt, programas,
  certificados, JSON de las rectas renombrados `line_<tag>_<fichero>`), subir a GitHub, escribir el tex al Project
  (`claude/casanya_turing_jensen_vN.tex`). Matemáticas del chat en LaTeX display.
- No mencionar tau^C ni el Teorema D del otro artículo. Atribución honesta: identidad, núcleos y máximo de fase por primo
  son de Amberger / Bellotti–Wong; propio: híbrido con discos de Jensen, optimización convexa, certificación Arb.
- Apéndices en hoja nueva (ya está: `\clearpage` antes de `\appendix` y de cada apéndice B, C, D).
- La cuestión abierta (híbrido explícito) va al final de §7 ("An open question"), breve y sin receta.

## Resultados certificados (no tocar)
- Seis rectas para todo T >= 1 (`family/line_{L5,L20,L60,L150,C400,D6000}/summary_pp.json`): la última
  |N-main| <= 0.08382 log T + 5.326, |S| <= 0.08382 log T + 4.444.
- Híbrido: a <= C_H < 0.0748596142711 (`hybrid_asymptotic/hyb_m10_P.json`, `cert_m10P.txt`, 90 discos, perfil e_P).

## Programas definitivos (todos en el apéndice y en el zip)
Certificación: `hybrid_asymptotic/{certutil.py, certify_hybrid.py, profile_published.py}`,
`family/{cz_gen_pp.py, elem_gen.py, certify_line_pp.py}`. Búsqueda: `hybrid_asymptotic/{lpcommon.py, explore_discs.py,
kernel_only.py}`, `family/opt_line.py`. Cada certificado empieza con los SHA-256 de su entrada y de sus programas;
`gen_appendix.py` comprueba esos hashes contra los ficheros reproducidos (si un programa cambia, hay que rehacer sus
certificados o la nota no compila).

## Cómo cerrar una versión tras rehacer certificados
    ./run_certificates.sh [JOBS]            # o las colas de rerun/; salidas *.new
    python3 rerun/finalize.py               # instala cert_*.txt, recalcula summary_pp.json, exige constantes iguales
    mv hybrid_asymptotic/cert_m10P.txt.new hybrid_asymptotic/cert_m10P.txt     # si se rehizo el híbrido
    cd docs/zenodo_note && python3 gen_appendix.py && python3 gen_values.py && python3 build.py vN
    # build imprime páginas, referencias/citas indefinidas (deben ser 0) y overfull (0). Luego el zip plano:
    # pdf, _l.tex, .txt + programas + certificados + hyb_m10_P.json + kernel_only.txt + line_<tag>_{sol.json,summary_pp.json,
    # cert_kernel.txt,cert_czeta_pp.txt,cert_elem.txt,cert_elem_S.txt,sol_czpp.json,sol_elem.json,sol_elemS.json}
    # (ver el zip de la versión anterior como plantilla). Commit + push; project_write del _l.tex.

## Estado al escribir esto
DEPOSITADO EN ZENODO: doi:10.5281/zenodo.23858827 (https://zenodo.org/records/23858827), 1 Nov 2026, v9 (solo el PDF;
el zip con código y certificados está en GitHub; conviene subirlo también a Zenodo como fichero adicional).
v8 ENTREGADA (1 Nov 2026, commit 9b9443b): los 25 certificados rehechos con los programas definitivos (procedencia
SHA-256, bola con radio real, inclusión a 20 dígitos), constantes idénticas, 56 pp., cada apéndice en hoja nueva,
"An open question" en §7.5 (sin receta; la frase-receta antigua de §7.4 se eliminó y con ella tres referencias que
quedaban sin citar), Backlund 1916, referencia ANTEDB. Ficheros: docs/zenodo_note/casanya_turing_jensen_v8{.pdf,_l.tex,
.txt,_zenodo.zip}; Project: claude/casanya_turing_jensen_v8.tex. Siguiente paso previsto por el autor: auditoría
bibliográfica externa (docs/zenodo_note/review_prompts/orden_verificacion_bibliografia.md) y reproducción de código.

## Pendiente (requiere modelo fuerte, no es mecánico)
Híbrido explícito: con el mismo núcleo y los mismos 90 discos (sin reoptimizar), sustituir e_P por un perfil con
cotas explícitas (Hiary–Patel–Yang en 1/2, Yang en sigma_k, 1-línea, zeta(sigma) en sigma>1; interpolación explícita
del Lema 5.2 / Rademacher) y hacer la contabilidad de Jensen explícita (cota superior de log|zeta| en el arco con sus
constantes y factores log t, cota inferior en el centro |zeta(c+it)| >= zeta(2c)/zeta(c)). Resultado esperado:
|S(T)| <= A_H log T + B_H log log T + C_H' para T >= T_0, con A_H ~ 0.076 (evaluación exploratoria no certificada:
0.07590 con Yang). Hacerlo en rama aparte sin tocar la nota; decidir con A_H, B_H, C_H', T_0 certificados y la altura
de cruce con l6000 si entra como Teorema 2.4 en una v9. Leer los enunciados exactos de las fuentes; no citar de memoria.
