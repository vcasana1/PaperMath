# Auditoría independiente de la evidencia de reproducción — Casaña–Turing–Jensen v9

**Fecha:** 2026-11-01. **Alcance:** inspección independiente del informe `REPRODUCCION_2026-11-01.md` y de los contenidos de `REPRODUCCION_2026-11-01_evidencia.zip`. No se ejecutaron los cálculos de alta carga de Arb por segunda vez en esta revisión; sí se inspeccionaron los resultados originales y los reproducidos, se recalcularon hashes y se cotejaron las diferencias.

## Resultado directo

- Archivo ZIP: 910 entradas, comprobación CRC completa sin errores.
- Certificados: 25 archivos publicados y sus 25 archivos reproducidos, incluidos los 24 de las seis rectas y el híbrido. Comprobación SHA-256 independiente: 25/25 pares de hashes concordantes con el manifiesto `independent_final_hash_check.json`.
- Comparación independiente línea por línea: 25/25 idénticos después de normalizar únicamente la versión de Python y las cadenas de duración en segundos. No hay alteraciones numéricas de cotas, radios, recuentos de cajas/intervalos ni inclusiones.
- Referencias SHA-256 impresas a archivos de datos o programas: 76/76 resueltas y verificadas contra archivos reales del ZIP.
- El registro `finalize.log` termina en `finalize ok` y muestra exactamente las 18 constantes de las seis rectas. `run_certificates.log` termina en `ALL_CERTIFICATES_DONE`.
- Los datos exactos del certificado híbrido contienen la inclusión
  
  `C_H in [0.074859614271090718755, 0.074859614271090718756]`.

## Correspondencia con el commit Git

Con la lectura del repositorio `vcasana1/PaperMath` fijada en el commit `7c28834103e7c1e2f7d9cd6879b4febe09dbe1f3`, se contrastó el hash Git de contenido para los cinco ficheros siguientes con el obtenido recalculando `SHA1("blob <size>\\0" + contenido)` sobre el ZIP:

| Archivo | Hash Git coincide |
|---|---|
| `hybrid_asymptotic/certify_hybrid.py` | Sí |
| `family/cz_gen_pp.py` | Sí |
| `family/elem_gen.py` | Sí |
| `hybrid_asymptotic/profile_published.py` | Sí |
| `docs/zenodo_note/casanya_turing_jensen_v9_l.tex` | Sí |

## Constantes confirmadas en la evidencia

| Recta | A1 | A3_N | A3_S |
|---|---:|---:|---:|
| L5 | 0.20176 | 1.369 | 0.844 |
| L20 | 0.10823 | 2.171 | 1.286 |
| L60 | 0.09473 | 2.834 | 1.946 |
| L150 | 0.09349 | 2.987 | 2.099 |
| C400 | 0.08399 | 5.202 | 4.318 |
| D6000 | 0.08382 | 5.326 | 4.444 |

La evidencia `tex_constants_verification.json` documenta el cálculo por intervalos de cada A1 y la suma exacta decimal con redondeo dirigido de los A3. Se ha inspeccionado dicho registro, así como las salidas originales y reproducidas.

## Qué demuestra y qué no demuestra este procedimiento

**CONFORME como auditoría de reproducción y procedencia.** Los resultados obtenidos por el mismo software en la otra máquina coinciden. Esto reduce sustancialmente el riesgo de errores de entorno, archivos discordantes o salidas no reproducibles. La adaptación de `rerun/finalize.py` es únicamente una ruta absoluta documentada y no cambia ecuaciones.

**No es una segunda implementación independiente de los algoritmos de certificación.** Si la fórmula aplicada por un programa no fuera una cota válida, o si faltase una hipótesis analítica en el artículo, una reproducción exacta heredaría el mismo defecto. Tampoco equivale a una revisión externa de toda la semántica de Arb/FLINT o de todas las fuentes matemáticas utilizadas. La revisión analítica previa del manuscrito no ha encontrado un fallo en los pasos examinados, pero esta evidencia no sustituye su revisión lógica completa.

**Conclusión:** reproducción informática **OK (25/25)**; integridad de datos y código **OK (76/76)**; validez matemática global de los teoremas **no deducible de la reproducción por sí sola**, aunque el resultado computacional anunciado queda sólidamente respaldado por la evidencia adjunta.

No se modificó ningún artículo, certificado publicado, ni repositorio.
