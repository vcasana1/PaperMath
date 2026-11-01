# Órdenes para ChatGPT — camino a la v10 de «Explicit and asymptotic estimates for the zero-counting function of the Riemann zeta-function»

Documento rector: `casanya_turing_jensen_v9` (Zenodo doi:10.5281/zenodo.23858827, 1 Nov 2026; GitHub `vcasana1/PaperMath`,
rama `explicit-S-turing`, `numerics/explicit_S_turing/docs/zenodo_note/`). Adjuntar siempre `casanya_turing_jensen_v9.txt`
(fuente LaTeX completa con programas, certificados y JSON) y el PDF.

Las cinco órdenes siguientes son independientes y se envían en chats separados, en este orden. Cada una produce un informe;
ninguna modifica el artículo. Los cambios los aplica el autor en la v10 a partir de los informes.

## Reglas comunes (pegar al principio de cada orden)

1. No inventes. Lo que no puedas comprobar se marca «NO VERIFICADO» con el motivo. Un «parece correcto» sin la fuente
   abierta no es una verificación.
2. Cita el identificador comprobable de cada dato (DOI resuelto, arXiv con versión, página del PDF adjunto).
3. Veredictos: OK / DISCREPANCIA (con la corrección exacta, lista para pegar en LaTeX) / NO VERIFICADO.
4. Lee las fórmulas en la imagen de la página, no en el texto extraído (el OCR de Backlund 1916 y von Mangoldt 1905 es
   delicado; en los demás, comprueba igualmente exponentes, cuantificadores y rangos sobre la página).
5. No propongas cambios matemáticos sin demostración completa, ni cambios de redacción fuera de lo pedido. El artículo
   usa voz impersonal; no sugieras primera persona.
6. Palabra prohibida en el artículo: «clock». No proponer verificaciones numéricas de ceros (Platt). Los únicos rangos
   que interesan son todo T ≥ 1 y T → ∞.
7. Entrega: tabla resumen al principio y fichas detalladas después, en español, con las cadenas corregidas en LaTeX.

---

## ORDEN 1 — Verificación bibliográfica contra las fuentes primarias

Adjuntar, de `LIBRARY TOTAL` (todos los nombres son exactos):
`013_Backlund_1916_…`, `022_Bellotti-Wong_2025_…`, `045_Bourgain_2017_…`, `105_Fiori_2025_…`,
`151_Hasanalizade-Shen-Wong_2022_Counting_Zeros_Riemann_Zeta.pdf`, `184_Johansson_2017_…`, `185_Johansson_2018_…`,
`286_Rademacher_1959_…`, `296_Rosser-Schoenfeld_1962_…`, `318_Titchmarsh-HeathBrown_1986_…`, `320_Trudgian_2012_…`,
`321_Trudgian_2014_…`, `337_vonMangoldt_1905_…`, `339_Amberger_2026_…_arXiv_v5.pdf` (y `338_…_v1.pdf` para comparar la
numeración), `340_Bellotti-Wong_2026_Counting_Zeros_Artin_L_Functions_arXiv_v1.pdf`,
`341_Davenport_1980_Multiplicative_Number_Theory_Second_Edition.pdf`, `342_HeathBrown_2016_…_arXiv_v3.pdf`,
`345_Olver_1997_Asymptotics_Special_Functions_AK_Peters_Reprint.pdf`, `346_Platt-Trudgian_2014_…_arXiv_v2.pdf`,
`348_Rosser_1941_…`, `349_Rudin_1987_…`, `350_Tao-Trudgian-Yang_2025_…_arXiv_v1.pdf`, `351_Titchmarsh_1939_…`,
`352_Trudgian-Yang_2024_Toward_Optimal_Exponent_Pairs_arXiv_v3.pdf`, `353_Turing_1953_…`.
En línea: DLMF §5.11(ii) (https://dlmf.nist.gov/5.11.ii), ANTEDB (https://teorth.github.io/expdb/), FLINT (https://flintlib.org),
Grossmann 1913 (tesis; buscar en Göttingen/Internet Archive; si no se abre, NO VERIFICADO).

Tarea: la orden detallada `orden_verificacion_bibliografia.md` (30 referencias; para cada una, datos bibliográficos y la
afirmación exacta que la nota le atribuye). Advertencias específicas:
- La nota cita Davenport **3.ª ed. (2000)**; el PDF disponible es la 2.ª (1980). Comprobar que los capítulos 12 y 13
  contienen lo citado (producto de Hadamard con B = −Σ Re(1/ρ); ζ(1+it) ≠ 0) y señalar si la numeración difiere entre
  ediciones.
- Olver: la nota cita (8.4.06) de *Asymptotics and Special Functions*; usar el PDF 345 (el 344 es otro libro).
- Platt–Trudgian 2015: el PDF 346 es el arXiv v2 del artículo de JNT 147; comprobar que los números 0.1100, 0.2900, 3.165
  son los del artículo (vía la Tabla 3 de Bellotti–Wong 2026).
- Heath-Brown: el PDF 342 es arXiv v3 (2016); el artículo es Proc. Steklov 296 (2017). Comprobar Thm. 2 en v3.
- Bourgain: numeración «Thm. 5» según arXiv:1408.5794v2; el PDF 045 puede ser la versión JAMS; comprobar ambas.
- Amberger: numeración según v5; anotar qué cambió respecto a v1 (Cor. 2, Tabla 6, Lema 9).

Entregable: tabla de 30 filas + fichas + lista de cadenas `\bibitem` corregidas.

---

## ORDEN 2 — Revisión matemática adversarial (informe de árbitro, demostraciones)

Adjuntar el .txt y el PDF de la v9. Objetivo: encontrar un error que invalide el Teorema 2.1, el Teorema 2.3 o el
Corolario 2.2, o certificar que no lo hay. Rehacer los cálculos, no solo leerlos. Puntos obligatorios:

1. **Lema 3.1 (identidad de Turing):** orientación del contorno, signo del término integral, factor 1/(2π), simetrización
   ρ ↦ 1−ρ̄, convergencia absoluta para intercambiar suma e integral, validez sin suponer β = ½, y que T no sea ordenada.
2. **Lema 3.2:** coeficiente (−1)^{j−1}/((j−1)! 2^j) de la poligamma en D_j, exclusión de (I,1), convergencia para j ≥ 2.
3. **Prop. 4.1:** signos de las cotas superior e inferior; que la cota inferior sea la superior con la parte impar cambiada.
4. **Lema sobre M_p:** grid de 4096 puntos y corrección de Lipschitz π/4096·Σ k|(a_k,b_k)|; agrupación de potencias.
5. **Lema de la cola (ψ(x) < 1.03883x):** la demostración por capas (layer-cake) con G no creciente; el paso
   ∫_{e^{L_B}}^∞ g ≤ ∫_{e^{L_B}}^{e^{L_1}} g + ∫_{e^{L_1}}^∞ g̃ cuando L_B > L_1; el lema de monotonía (num/low < σ1).
6. **Lema 4.7 (parte elemental, T ≥ T0):** cada término de la constante K, incluido el j = 1 con B/(T0·T); el resto de
   Stirling |R(z)| ≤ sec²(½ ph z)/(12|z|) y las estimaciones de Cauchy; que T·cota sea no creciente para j ≥ 2.
7. **Lema sobre ϑ(T):** |ϖ(T)| ≤ (1/16 + 1/8 + 1/3)/T y la relación N = ϑ/π + 1 + S con la convención de continuidad.
8. **Lema 5.2 (interpolación de Phragmén–Lindelöf para (s−1)ζ(s)):** crecimiento 3|s|(1+|s|), la cota |Q+s| ≤ 6|t| vía
   |Q+s|² ≤ 121 + t² ≤ 36t², el uso de Rademacher con α₂ = 0, y que el resultado sea un perfil admisible.
9. **Lema 5.3 (perfil e_P):** que cada nodo sea un teorema publicado; la envolvente convexa inferior; que no se usa la
   convexidad de μ más allá de lo dicho.
10. **§6 (Jensen):** el factor 2 de la simetría, la fórmula de Jensen con ceros en la circunferencia, la cota superior en
    el arco donde σ > 1 y 1 ≤ σ ≤ 2, la cota inferior |ζ(s0)| en el centro, el paso al límite superior y la fórmula (CH).
11. **Prop. 6.3 (certificación):** forma centrada, cola en u = 1/t con 4d³u + K5|u|³, inclusión de t = 0 y u = 0 en las
    cajas, positividad de 2dc_{R,1} − 2c_{R,2}, y que «all certified» implique la desigualdad en todo el dominio.
12. **Remark 2.4 (convenciones):** que las comparaciones del Corolario 2.2 sean entre cotas de la misma cantidad pese a la
    convención del peso ½ en las ordenadas.
13. **Corolario 2.2:** recomputar los cinco puntos de cruce de las seis rectas y las diferencias mínimas 2.231 y 0.291, y
    las dos afirmaciones sobre rectas individuales.

Entregable: informe de árbitro con veredicto por punto, cada error con contraejemplo o cálculo, y la corrección propuesta.

---

## ORDEN 3 — Correspondencia código ↔ fórmulas (auditoría estática)

Adjuntar el .txt. Para cada programa de certificación (`certutil.py`, `certify_hybrid.py`, `profile_published.py`,
`cz_gen_pp.py`, `elem_gen.py`, `certify_line_pp.py`) comprobar línea a línea que implementa la fórmula del artículo:
f y su forma regular en t = 0; F_Rj, F_Ij y sus derivadas; W_k y su cota inferior; la cola t²U en u; la expansión de f con
4d³u y K5; a(L), b(L), h(L); el máximo por primo; G escalonada; la integral invertida; D_j y dD_j con las poligammas;
la forma centrada en T; la constante K; los modos N y S; el redondeo dirigido (`up_str`/`down_str`) y la suma final con
`Decimal`/`ROUND_CEILING`; que ningún float entre en Arb por `A()` (solo `Fraction`/`int`) y que las constantes decimales
entren como cadenas (`arb('1.03883')`). Comprobar también que los SHA-256 impresos en los certificados coinciden con los
programas reproducidos (recalcularlos sobre los bloques del .txt) y que los JSON del Apéndice D son los que los
certificados declaran haber leído.

Entregable: tabla programa × fórmula con OK/DISCREPANCIA, y lista de supuestos implícitos que convendría convertir en
`assert`.

---

## ORDEN 4 — Literatura y posicionamiento

Buscar, **solo con DOI o arXiv verificable**: (a) cotas incondicionales de |S(T)| o |N(T)−main(T)| entre julio y noviembre
de 2026 con coeficiente principal ≤ 0.0946 (todo T) o ≤ 0.0749 (asintótico); (b) trabajos que combinen la identidad de
Turing/Amberger con la fórmula de Jensen o con discos; (c) confirmar o descartar un trabajo de 2026 de un autor «Ismail»
sobre cotas explícitas de S(T) a alturas finitas; (d) mejoras recientes de μ(σ) en (½,1) (pares exponente nuevos) que
bajarían C_H al añadirse al perfil. Comprobar que `289_Revers_2026_Improved_Explicit_Estimate_Zeta_Critical_Line.pdf`
(arXiv:2602.05614, cota explícita en σ = ½) no afecta a nada de lo afirmado (la nota no usa cotas explícitas de
subconvexidad). Entregable: lista con identificadores y una frase por ítem sobre su relación con la nota; si no hay
nada, decirlo.

---

## ORDEN 5 — Lectura de árbitro de Mathematics of Computation y corrección de inglés

Adjuntar el PDF. Dos partes. (a) Informe de árbitro para *Math. Comp.*: claridad de enunciados, novedad frente a
Amberger y Bellotti–Wong, suficiencia de los certificados, afirmaciones impugnables, qué material pasaría a suplemento
para una versión de revista (~25 páginas de texto principal), códigos MSC 2020 sugeridos. (b) Inglés matemático: lista de
errores o rigideces frase por frase, con la frase corregida; mantener voz impersonal y el estilo de Amberger (párrafos
cortos, variables introducidas antes de usarse). No tocar enunciados ni demostraciones.

---

## Después de las cinco órdenes (lo hace el autor con Claude): v10

Aplicar solo lo que venga con corrección exacta y comprobada; rehacer un certificado únicamente si cambia un programa
(los hashes lo detectan); añadir el DOI de Zenodo a *Data availability* (ya preparado); regenerar apéndices y compilar;
entregar pdf, tex, txt y zip; subir a GitHub y al Project; depositar la v10 en Zenodo como nueva versión del mismo
registro, incluyendo el zip de reproducibilidad.
