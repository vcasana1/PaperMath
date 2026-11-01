# Orden de trabajo: verificación bibliográfica exhaustiva de la nota «casanya_turing_jensen» (v8)

Eres un revisor bibliográfico riguroso. Tu tarea es verificar, **contra las fuentes primarias**, cada una de las 30 referencias
de la nota adjunta (`casanya_turing_jensen_v8.txt`) y cada uso que el texto hace de ellas. No se trata de opinar sobre las
matemáticas de la nota, sino de comprobar que lo que se cita existe, está bien descrito y dice exactamente lo que la nota le
atribuye.

## Reglas

1. **Nunca inventes.** Si no puedes acceder a una fuente, escribe «no verificado: sin acceso» y di qué intentaste. Un
   «parece correcto» sin haber abierto la fuente cuenta como no verificado.
2. Cita siempre el **identificador comprobable** (DOI resuelto, URL de arXiv con versión, página del libro) desde el que
   verificaste cada dato. Si un DOI no resuelve o resuelve a otro artículo, dilo.
3. Distingue tres veredictos por ítem: **OK** / **DISCREPANCIA** (con la cadena corregida exacta, lista para pegar) /
   **NO VERIFICADO**.
4. Para cada resultado matemático citado, transcribe literalmente (o traduce fielmente) el enunciado de la fuente y
   compáralo con el uso en la nota: hipótesis, rango de validez, constantes, numeración del teorema **en la versión citada**.
5. Si detectas una referencia que podría ser una alucinación (autor, título o DOI que no existen), señálalo como tal.
6. No propongas cambios de redacción ni de matemáticas; solo bibliografía y correspondencia cita–fuente.
7. Entrega: una tabla resumen (ítem, veredicto, acción) y, debajo, la ficha detallada de cada ítem.

## Lista de referencias y de lo que la nota les atribuye

Para cada entrada: (a) datos bibliográficos a comprobar; (b) afirmaciones de la nota que dependen de ella.

1. **Amberger2025** — V. S. G. Amberger, *Estimating the number of zeros of Dedekind zeta-functions*, arXiv:2510.27444v5
   (12 Oct 2026; v1 31 Oct 2025). (b) Cor. 2: |N(T)−main(T)| ≤ 0.097 log T + 4.807 para todo T ≥ 1; Tabla 6: las siete
   cotas 0.097L+4.807, 0.1L+4.140, 0.12L+2.830, 0.14L+2.306, 0.16L+2.027, 0.18L+1.847, 0.2L+1.722; Lema 9: la cota inferior
   se obtiene de la superior cambiando el signo de la parte impar (máximo sobre la fase común de las potencias de un primo);
   convención: cero con parte imaginaria exactamente T contado con peso ½; método inspirado en Turing 1953, Lema 1.
   Comprobar que la v5 existe con esa fecha y que la numeración (Cor. 2, Tabla 6, Lema 9) es la de v5.
2. **ANTEDB** — Tao, Trudgian, Yang et al., Analytic Number Theory Exponent Database, https://teorth.github.io/expdb/ ,
   capítulo sobre el crecimiento de ζ, tabla de cotas de μ(σ). (b) La nota dice que esa tabla contiene nodos atribuidos a
   «Cushing (2025)» sin fuente citable, y que por eso no los usa. Comprobar la existencia de la tabla y de esos nodos.
3. **Backlund1918** (clave) — R. J. Backlund, *Über die Nullstellen der Riemannschen Zetafunktion*, Acta Math. 41 (1916)
   345–375, doi:10.1007/BF02422950. (b) Año del volumen 41 (1916 vs 1918); constantes históricas 0.1370, 0.4430, 5.2250,
   T0 = 200 (tomadas de Bellotti–Wong 2026, Tabla 3).
4. **Bellotti2024** — eliminada en v8 (no citada). Confirmar que no queda ninguna mención.
5. **BellottiWong2025** — C. Bellotti, P.-J. Wong, *Improved estimates for the argument and zero-counting function of the
   Riemann zeta-function*, Math. Comp., publicado en línea 14 Nov 2025, doi:10.1090/mcom/4133; numeración según
   arXiv:2412.15470v2. (b) Cor. 1.5: |S(T)| ≤ 0.10076 log T + 0.24460 log log T + 7.20844 para T ≥ e; fila de la tabla
   histórica: 0.10076, 0.24460, 8.08344, T0 = e (para N − main).
6. **BellottiWong2026** — *Counting zeros of Artin L-functions*, arXiv:2606.31441v1, 30 Jun 2026. (b) Cor. 1.3:
   |N(T)−main(T)| ≤ min(0.0946 log T + 5.746, 0.097 log T + 4.954) para T ≥ 1, incondicional para ζ; §3: pregunta sobre el
   ínfimo del coeficiente principal con finitos núcleos; Tabla 3: filas históricas de von Mangoldt a Bellotti–Wong 2025 que
   la nota reproduce (ver tabla de la nota); convención del peso ½ en la ordenada.
7. **Bourgain2017** — J. Bourgain, *Decoupling, exponential sums and the Riemann zeta function*, J. Amer. Math. Soc. 30
   (2017) 205–224, doi:10.1090/jams/860; numeración según arXiv:1408.5794v2. (b) Thm. 5: μ(1/2) ≤ 13/84.
8. **CasanaGiner2026** — V. Casaña-Giner, manuscrito propio, versión 57, enviado. (b) Cor. 1.2: a ≤ 0.0968160…; Remark 5.2:
   Λ(0) = (3√3−π)/(12π log 2) = 0.0786252… como límite inferior del método de Backlund con discos cerca de s = 1.
   Solo comprobar coherencia interna si se dispone del manuscrito; si no, marcar «no verificable externamente».
9. **Davenport2000** — H. Davenport, *Multiplicative Number Theory*, 3.ª ed., GTM 74, Springer 2000,
   doi:10.1007/978-1-4757-5927-3. (b) Cap. 12: producto de Hadamard ξ'/ξ(s) = B + Σ_ρ (1/(s−ρ) + 1/ρ) con B = −Σ Re(1/ρ);
   Cap. 13: ζ(1+it) ≠ 0 (Hadamard–de la Vallée Poussin).
10. **DLMF** — §5.11(ii), Release 1.2.4 (2025-03-15). (b) Fórmula de Stirling con resto: |R(z)| ≤ sec²(½ ph z)/(12|z|) para
    |ph z| < π (comprobar número de ecuación y forma exacta del resto R_1).
11. **Fiori2025** — A. Fiori, *A note on the Phragmén–Lindelöf theorem*, arXiv:2502.13282v3. (b) Cor. 3 con α₂ = 0: la
    versión del teorema usada para interpolar |Z(s)| ≤ A|Q+s|^{1+e_i+ε} entre dos rectas; comprobar la versión v3 y que el
    corolario 3 es el que corresponde.
12. **FLINT** — FLINT 3.6.0, https://flintlib.org . Comprobar que 3.6.0 es una versión existente y que python-flint 0.9.0
    la usa (o indicar la versión de FLINT que python-flint 0.9.0 incorpora).
13. **Grossmann1913** — J. Grossmann, tesis doctoral, Göttingen 1913, *Über die Nullstellen der Riemannschen Zeta-Funktion
    und der Dirichletschen L-Funktionen*. (b) Constantes históricas 0.2907, 1.7862, 7.0120, T0 = 50 (vía BW 2026 Tabla 3).
14. **HasanalizadeShenWong2022** — J. Number Theory 235 (2022) 219–241, doi:10.1016/j.jnt.2021.06.032. (b) 0.1038, 0.2573,
    9.4925, T0 = e.
15. **HeathBrown2017** — D. R. Heath-Brown, *A new k-th derivative estimate for exponential sums via Vinogradov's mean
    value*, Proc. Steklov Inst. Math. 296 (2017) 88–103, doi:10.1134/S0081543817010084; numeración según
    arXiv:1601.04493v3. (b) Thm. 2: (2/((n−1)²(n+2)), 1 − (3n−2)/(n(n−1)(n+2)) + ε) es un par exponente para todo n ≥ 3 y
    ε > 0. Comprobar fórmula exacta y numeración.
16. **Johansson2017** — F. Johansson, *Arb: efficient arbitrary-precision midpoint-radius interval arithmetic*, IEEE Trans.
    Comput. 66 (2017) 1281–1292, doi:10.1109/TC.2017.2690633. (b) referencia general de Arb.
17. **Johansson2018** — F. Johansson, *Numerical integration in arbitrary-precision ball arithmetic*, ICMS 2018, LNCS 10931,
    255–263, doi:10.1007/978-3-319-96418-8_30. (b) La integración rigurosa de Arb usa Gauss–Legendre solo en subintervalos
    donde el integrando se certifica holomorfo (parámetro «analytic»), y recurre a la inclusión directa si no.
18. **Olver1974** — F. W. J. Olver, *Asymptotics and Special Functions*, Academic Press 1974; reimpresión A K Peters 1997,
    doi:10.1201/9781439864548. (b) Ecuación (8.4.06): el mismo resto de Stirling. Comprobar numeración.
19. **PlattTrudgian2015** — J. Number Theory 147 (2015) 842–851, doi:10.1016/j.jnt.2014.08.019. (b) 0.1100, 0.2900, 3.165,
    T0 = e.
20. **Rademacher1959** — H. Rademacher, *On the Phragmén–Lindelöf theorem and some applications*, Math. Z. 72 (1959)
    192–204, doi:10.1007/BF01162949. (b) Teorema de tipo Phragmén–Lindelöf con cotas A|Q+s|^α en los bordes de una banda e
    interpolación lineal del exponente.
21. **Rudin1987** — W. Rudin, *Real and Complex Analysis*, 3.ª ed., McGraw-Hill 1987. (b) Thm. 15.18: fórmula de Jensen,
    válida con ceros sobre la circunferencia.
22. **Rosser1941** — J. B. Rosser, *Explicit bounds for some functions of prime numbers*, Amer. J. Math. 63 (1941) 211–232,
    doi:10.2307/2371291. (b) 0.1370, 0.4430, 2.4630, T0 = 2.
23. **RosserSchoenfeld1962** — Illinois J. Math. 6 (1962) 64–94, doi:10.1215/ijm/1255631807. (b) Thm. 12: ψ(x) < 1.03883 x
    para todo x > 0. Comprobar que es el Teorema 12 y el rango «x > 0».
24. **TaoTrudgianYang2025** — *New exponent pairs, zero density estimates, and zero additive energy estimates: a systematic
    approach*, arXiv:2501.16779v1, 28 Jan 2025. (b) Thm. 20: los pares (89/1282, 997/1282), (652397/9713986,
    7599781/9713986), (10769/351096, 609317/702192), (89/3478, 15327/17390); Lema 23: μ(ℓ−k) ≤ k para todo par exponente.
    Comprobar numeración en v1 y si existe una versión posterior con numeración distinta.
25. **Titchmarsh1939** — *The Theory of Functions*, 2.ª ed., OUP 1939. (b) §3.61: fórmula de Jensen.
26. **Titchmarsh1986** — *The Theory of the Riemann Zeta-Function*, 2.ª ed. rev. Heath-Brown, Clarendon 1986. (b) §2.1,
    (2.1.12)–(2.1.13): ξ entera, ξ(s) = ξ(1−s), real y positiva en el eje real; (2.1.4): ζ(s) = s/(s−1) − s∫₁^∞ {x} x^{−s−1} dx
    para Re s > 0; Thm. 3.5: ζ(1+it) ≪ log t (y |ζ(s)| ≪ log t en 1 ≤ σ ≤ 2); §5.1: definición de μ(σ) y convexidad; §5.20 y
    (5.20.1): pares exponente y μ(ℓ−k) ≤ k; §9.3: N(T) = ϑ(T)/π + 1 + S(T); §9.4: Σ|γ|^{−2} < ∞.
27. **Trudgian2012** — Math. Comp. 81 (2012) 1053–1061, doi:10.1090/S0025-5718-2011-02537-8. (b) 0.1700, 0, 2.8730, T0 = e.
28. **Trudgian2014** — J. Number Theory 134 (2014) 280–292, doi:10.1016/j.jnt.2013.07.017. (b) 0.1120, 0.2780, 3.3850, T0 = e.
29. **TrudgianYang2024** — *Toward optimal exponent pairs*, arXiv:2306.05599v3, 15 Jul 2024. (b) Thm. 2.4: cota lineal a
    trozos para μ(σ), μ ≤ a − bσ en [lo, hi], con los diez tramos siguientes (lo, hi, a, b):
    (1/2, 88225/153852, 31/84, 3/7), (88225/153852, 521/796, 220633/620612, 62831/155153), (521/796, 53141/76066,
    1333/3825, 1508/3825), (53141/76066, 3620/5119, 405/1202, 227/601), (3620/5119, 52209/69128, 49318855/170145110,
    52938216/170145110), (52209/69128, 1389/1736, 471957/1682490, 502648/1682490), (1389/1736, 134765/163248, 2841/10316,
    3016/10316), (134765/163248, 18193/21906, 859/3214, 908/3214), (18193/21906, 249/280, 5·8707/180277, 5·9067/180277),
    (249/280, 277/300, 29/130, 30/130). Comprobar cada tramo, la continuidad en los extremos y que la pieza final llega a
    277/300.
30. **Turing1953** — A. M. Turing, *Some calculations of the Riemann zeta-function*, Proc. London Math. Soc. (3) 3 (1953)
    99–117, doi:10.1112/plms/s3-3.1.99. (b) Lema 1: la identidad de tipo Turing (integral de ξ'/ξ en horizontal).
31. **VonMangoldt1905** — Math. Ann. 60 (1905) 1–19, doi:10.1007/BF01447494. (b) N(T) = main(T) + O(log T); fila histórica
    0.4320, 1.9167, 13.0788, T0 = 28.5580.

## Comprobaciones adicionales

- **Literatura posterior:** busca cotas incondicionales de |S(T)| o de |N(T)−main(T)| publicadas o depositadas entre
  julio y noviembre de 2026 con coeficiente principal ≤ 0.0946 (todo T) o ≤ 0.0749 (asintótico). Solo con identificador
  verificable (DOI o arXiv). Si no encuentras nada, dilo; no inventes autores ni títulos.
- **Coherencia interna de la nota:** cada \cite tiene su \bibitem y cada \bibitem se cita al menos una vez; los años del
  texto coinciden con los de la bibliografía (p. ej. Backlund 1916 en ambos sitios).
- **Formato:** todas las entradas con DOI cuando existe; arXiv con versión y fecha; páginas e intervalos correctos.

Entrega el informe en español, con la tabla resumen al principio.
