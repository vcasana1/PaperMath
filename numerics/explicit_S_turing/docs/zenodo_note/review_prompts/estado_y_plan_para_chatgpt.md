# Estado actual y plan de trabajo — nota «Explicit and asymptotic bounds for S(T)» (casanya_turing_jensen v9)

Documento para ChatGPT. Contiene el estado exacto del artículo, lo que ya está verificado, lo que falta, y las tareas que
se te encargan, en orden, con el formato de entrega. No modifiques el artículo: entrega informes; los cambios los aplica
el autor en una versión nueva (v10).

## 1. Estado al 1 de noviembre de 2026

**Artículo:** `casanya_turing_jensen_v9` (pdf 56 pp., `_l.tex` autocontenido, `.txt`, zip plano para Zenodo). Repositorio
público: `vcasana1/PaperMath`, rama `explicit-S-turing`, carpeta `numerics/explicit_S_turing/`.

**Resultados (incondicionales, certificados en aritmética de bolas Arb a 256 bits):**

- Teorema 2.1 (seis rectas, todo T ≥ 1): |N(T)−main(T)| ≤ min_k (A1_k log T + A3N_k) y |S(T)| ≤ min_k (A1_k log T + A3S_k);
  última recta 0.08382 log T + 5.326 y 0.08382 log T + 4.444. Corolario 2.2: por debajo de Bellotti–Wong 2026
  (min(0.0946L+5.746, 0.097L+4.954)) en todo T ≥ 1 por ≥ 2.231 y de Amberger (Cor. 2 y Tabla 6) por ≥ 0.291.
- Teorema 2.3 (asintótico): a = limsup |S(T)|/log T ≤ C_H < 0.0748596142711, híbrido núcleo + 90 discos de Jensen con el
  perfil e_P de cotas de subconvexidad publicadas. Sin altura efectiva (los exponentes no tienen constantes explícitas).
- Remark 2.4: los óptimos de malla sin discos se estancan en ≈0.079 (m = 4, 10, 20: 0.08831, 0.08071, 0.07983); responde a
  la pregunta de Bellotti–Wong §3.

**Qué está ya verificado (por lectores independientes, estáticamente):** identidad de Turing (Lema 3.1), sumas de núcleos
(3.2), signos de la Prop. 4.1, máximo de fase por primo, cola con ψ(x) < 1.03883x, parte elemental (Lema 4.7, constante K
alineada con el código), Jensen y perfil (§5), certificación (Prop. 6.3), redondeo decimal dirigido, trazabilidad (los
SHA-256 impresos en cada certificado coinciden con los programas reproducidos en el apéndice; comprobado desde el .txt).
Compila sin referencias rotas. Diez programas sintácticamente válidos.

**Qué NO está hecho:**
1. Verificación bibliográfica contra las fuentes primarias (30 referencias): **tu tarea principal**.
2. Reproducción numérica independiente de los 25 certificados (requiere python-flint; no es posible en el intérprete de
   ChatGPT sin red; se hará en el Mac del autor con `run_certificates.sh` o con Codex).
3. Híbrido explícito (Teorema 2.4 futuro): trabajo matemático aparte, no se te encarga.

## 2. Fuentes: qué hay en LIBRARY TOTAL y qué falta

El autor adjuntará PDF de su biblioteca `LIBRARY TOTAL` (337 PDF, índice en `INDEX.md`). Para las referencias de la nota:

**Disponibles en la biblioteca (adjuntar):**
`013_Backlund_1916_…pdf`, `022_Bellotti-Wong_2025_…pdf`, `045_Bourgain_2017_…pdf`, `105_Fiori_2025_…pdf`,
`151_Hasanalizade-Shen-Wong_2022_Counting_Zeros_Riemann_Zeta.pdf`, `184_Johansson_2017_Arb_…pdf`,
`185_Johansson_2018_Numerical_Integration_Ball_Arithmetic.pdf`, `286_Rademacher_1959_…pdf`,
`296_Rosser-Schoenfeld_1962_…pdf`, `318_Titchmarsh-HeathBrown_1986_…pdf`, `320_Trudgian_2012_…pdf`,
`321_Trudgian_2014_…pdf`, `337_vonMangoldt_1905_…pdf`.

**No localizadas en la biblioteca (buscar en línea por DOI/arXiv; si no se puede abrir, marcar NO VERIFICADO):**
Amberger arXiv:2510.27444v5; Bellotti–Wong arXiv:2606.31441v1; Heath-Brown 2017 (arXiv:1601.04493v3);
Trudgian–Yang arXiv:2306.05599v3; Tao–Trudgian–Yang arXiv:2501.16779v1; Turing 1953 (doi:10.1112/plms/s3-3.1.99);
Rosser 1941 (doi:10.2307/2371291); Platt–Trudgian 2015 (doi:10.1016/j.jnt.2014.08.019); Grossmann 1913 (tesis);
Davenport 2000; Rudin 1987; Olver 1974; Titchmarsh 1939; DLMF §5.11(ii) (web); ANTEDB (web); FLINT (web).

**Advertencia de la propia biblioteca (INDEX.md):** el OCR de Backlund 1916 y von Mangoldt 1905 es delicado; verificar
fórmulas en la imagen de la página, no en el texto extraído.

**Nota:** la biblioteca contiene `289_Revers_2026_Improved_Explicit_Estimate_Zeta_Critical_Line.pdf`, una cota explícita
de 2026 en la recta crítica. No está citada en la nota (la nota no usa cotas explícitas de subconvexidad). Comprobar si
afecta a algo de lo afirmado; en principio no.

## 3. Tareas, en orden

### Tarea 1 — Verificación bibliográfica (la orden detallada está en `orden_verificacion_bibliografia.md`)
Para cada una de las 30 referencias: datos bibliográficos (autores, título, revista/arXiv con versión y fecha, volumen,
páginas, año, DOI que resuelve) y **correspondencia cita–fuente**: que el teorema/lema/sección citado existe con ese número
en la versión citada y dice lo que la nota le atribuye (constantes, rangos de validez, hipótesis). La lista de lo que la nota
atribuye a cada referencia está en la orden. Veredicto por ítem: OK / DISCREPANCIA (con la cadena corregida) / NO VERIFICADO.

Puntos que exigen especial cuidado:
- Rosser–Schoenfeld Thm 12: ψ(x) < 1.03883 x para **todo x > 0** (no solo x grande).
- Trudgian–Yang Thm 2.4: los diez tramos (lo, hi, a, b) listados en la orden, continuidad en los extremos, último tramo
  hasta 277/300.
- Tao–Trudgian–Yang: los cuatro pares de Thm 20 y el Lema 23 (μ(ℓ−k) ≤ k); si hay versión posterior a v1, anotar cambios
  de numeración.
- Heath-Brown Thm 2: fórmula exacta del par exponente (2/((n−1)²(n+2)), 1 − (3n−2)/(n(n−1)(n+2)) + ε), n ≥ 3.
- Bourgain Thm 5: μ(1/2) ≤ 13/84; numeración según arXiv v2 frente a la versión JAMS.
- Amberger v5: Cor. 2 (0.097 log T + 4.807, T ≥ 1), Tabla 6 (siete cotas), Lema 9 (parte impar), fecha de v5.
- Bellotti–Wong 2026: Cor. 1.3 (dos cotas, T ≥ 1, incondicional para ζ), §3 (pregunta del ínfimo), Tabla 3 (filas
  históricas que la nota copia: comprobar cada número).
- Bellotti–Wong 2025: Cor. 1.5 (|S(T)| ≤ 0.10076 log T + 0.24460 log log T + 7.20844, T ≥ e) y la fila 0.10076/0.24460/8.08344.
- Backlund: 1916 (Acta Math. 41) en texto y bibliografía.
- Rudin Thm 15.18 (Jensen con ceros en la circunferencia) y Titchmarsh 1939 §3.61.
- DLMF 5.11(ii) y Olver (8.4.06): resto de Stirling |R(z)| ≤ sec²(½ ph z)/(12|z|).

### Tarea 2 — Literatura posterior (junio–noviembre de 2026)
Buscar cotas incondicionales nuevas de |S(T)| o |N(T)−main(T)| con coeficiente principal ≤ 0.0946 (todo T) o ≤ 0.0749
(asintótico), y cualquier trabajo que use discos de Jensen combinados con la identidad de Turing. **Solo con DOI o arXiv
verificable.** Si no hay nada, decirlo. En particular, confirmar o descartar con identificador la existencia de un trabajo
de 2026 de un autor «Ismail» sobre cotas explícitas de S(T) a alturas finitas (mencionado en una búsqueda anterior sin
identificador; no se ha podido localizar).

### Tarea 3 — Coherencia interna del .txt
Cada \cite tiene \bibitem y cada \bibitem se cita; años del texto = años de la bibliografía; la tabla histórica (Tabla 1)
coincide con Bellotti–Wong 2026 Tabla 3 en las filas anteriores a 2025; los valores de la Tabla 2 (seis rectas) coinciden
con los `summary_pp.json` del Apéndice D y con las últimas líneas de los certificados del Apéndice C.

### Tarea 4 — Lectura de árbitro (opcional, si queda capacidad)
Informe de árbitro para Mathematics of Computation: claridad del enunciado, novedad frente a Amberger y Bellotti–Wong,
suficiencia de los certificados, longitud (qué pasaría al suplemento), y cualquier afirmación que un árbitro competidor
pudiera impugnar. Sin reescribir nada.

## 4. Formato de entrega

Un único informe en español con: (1) tabla resumen de las 30 referencias (ítem, veredicto, acción); (2) fichas detalladas
con el identificador desde el que se verificó cada dato; (3) resultado de la Tarea 2 con identificadores; (4) lista de
incoherencias internas, si las hay; (5) opcionalmente el informe de árbitro. Las correcciones propuestas, como cadenas
exactas listas para pegar en el .tex. No proponer cambios matemáticos ni de redacción fuera de lo bibliográfico.
