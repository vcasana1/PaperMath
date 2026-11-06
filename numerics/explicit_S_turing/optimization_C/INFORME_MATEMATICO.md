# Optimización ejecutada de la constante aditiva de S(T)

Este informe acompaña cálculos ejecutados y certificados con Arb. El resumen
numérico seleccionado se añade al final de la ejecución en `FINAL_NUMBERS.md`.
No se afirma que se haya alcanzado el límite absoluto de la construcción.

## Fuentes, conservación y auditoría inicial

La base es `vcasana1/PaperMath`, rama `explicit-S-turing`, commit
`e41acb3936b6b97c224ed7f31c7eb18bf6d9c5c1`. Se leyeron las secciones 3 y 4 y
la observación armónica de la sección 7.1 de `casanya_turing_jensen_v11_l.tex`,
así como `opt_line.py`, `cz_gen_pp.py`, `elem_gen.py`, `certify_hybrid.py` y
`certutil.py`. Las fuentes originales no se han editado. Los coeficientes se
leen de sus JSON completos, conservando exactamente la interpretación racional
que emplean los certificadores, no de las tablas impresas.

Se buscó el ZIP `certificado_S_4_40577136.zip` y los programas solicitados en
Descargas, Documentos, Escritorio, adjuntos de Codex y el árbol del repositorio.
No se encontraron. Por ello **4.40577136 es la referencia indicada por el
autor, no un certificado anterior auditado en este trabajo**. Su ausencia no
se interpreta como refutación. Se ha reconstruido y certificado por separado
el núcleo `line_D6000` de v11, y se reprodujo su cota elemental completa.

La búsqueda de nombres se amplió al directorio personal accesible; los registros
`prior_certificate_full_home_search*` conservan el resultado y los cinco errores
de acceso. Por ello se dice «no localizado», sin afirmar inexistencia en el Mac.
Los dos manuscritos añadidos por el autor durante la ejecución se conservan con
hashes en `inputs/supplementary/`. Se inspeccionaron sus resúmenes y referencias
a S(T); ningún teorema suyo se usa en este certificado. Esta ejecución no es una
auditoría completa de esos dos trabajos y no modifica sus fuentes.

## Problema y distinción entre búsqueda y prueba

Se mantienen las definiciones de v11:

\[
 U(b,t)=\sum_{\iota\in\mathcal B_m}c_\iota G_\iota(b,t),\qquad
 f(b,t)\le U(b,t),\quad |b|\le\tfrac12,\ t\ne0.
\]

Con \(z_\pm=d\pm b+it\), las funciones de base son
\(G_{R,j}=\Re(z_+^{-j}+z_-^{-j})\) y
\(G_{I,j}=-\Im(z_+^{-j}+z_-^{-j})\). La función mayorada es

\[
f(b,t)=\pi\operatorname{sgn}(t)
-2\arctan\frac{t}{d+b}-2\arctan\frac{t}{d-b}
+\arctan\frac{t}{2d+b}+\arctan\frac{t}{2d-b}.
\]

Las normalizaciones aritméticas utilizadas en todos los certificadores son

\[
a(L)=-\frac1\pi\sum_{(R,j)}\frac{c_{R,j}L^{j-1}}{(j-1)!},\qquad
b(L)=\frac{e^{-dL}-2}{\pi L}
 -\frac1\pi\sum_{(I,j)}\frac{c_{I,j}L^{j-1}}{(j-1)!},
\]

\[
f_p(x)=(\log p)\sum_{k\ge1}p^{-k(d+1/2)}
 \{a(k\log p)\cos(kx)+b(k\log p)\sin(kx)\}.
\]

La constante aritmética verdadera es
\(C_\zeta=\sum_p\max_x f_p(x)\). Su valor certificado incluye todas las
potencias de todos los primos. Para la búsqueda se usa una función convexa
aproximante: máximos de polinomios trigonométricos para primos pequeños, normas
para los restantes términos finitos y cuadratura de la cola. Esa aproximación
no se utiliza como cota demostrada.

Con \(a_0=0.08382\), la búsqueda de la rama alta minimiza

\[
 J_{L_0}(c)=C_\zeta(c)-A(c)\log(2\pi)
                  +(A(c)-a_0)L_0,
 \quad A(c)=\frac{c_{R,1}}{2\pi},\quad A(c)\le a_0,
\]

con \(L_0=100\). Esta es la contribución asintótica a la constante aditiva de
una rama que se usa en \(T\ge e^{100}\), manteniendo la holgura de pendiente.
La prueba añade después el resto elemental explícito, sin tomarlo por cero.
El núcleo de cobertura inferior tiene pendiente mayor que \(a_0\), lo cual
está permitido al utilizarlo únicamente en un intervalo acotado.

El refinamiento final alimenta el objetivo con la medida de potencias de
primos realmente cribadas hasta \(10^8\), en lugar de usar la densidad continua
desde \(2\cdot10^4\). En paneles de anchura 0.02 en el logaritmo, una cuadratura
gaussiana empírica de tres nodos y pesos positivos reproduce seis momentos
numéricos. Los pesos positivos conservan la convexidad del programa finito.
Esto mejora el objetivo de búsqueda, pero no convierte esa cuadratura en una
cota rigurosa: los certificadores independientes no la importan ni la usan.
También se ejecuta el aumento del número de primos cuyas fases se acoplan en
el objetivo, y no únicamente en la certificación posterior.

Para \(d,m\) fijos, (K), la restricción de pendiente y los epígrafos son convexos.
Clarabel resuelve los problemas cónicos finitos. La búsqueda en \(d\) y en el
orden es exterior y no convexa. Sus resultados no prueban optimalidad global
en esos parámetros. Las restricciones de (K) se refinan por planos de corte
y minimización local de todos los mínimos cercanos al contacto detectados
en la búsqueda; esta última búsqueda sigue siendo numérica.

## Cambio de base para órdenes altos [DED]

Con \(z=d\pm b+it\) y \(\lambda=2d-1>0\), se emplean las bases equivalentes

\[
 z^{-1}(1-\lambda/z)^{j-1}\quad(R),\qquad
 z^{-2}(1-\lambda/z)^{j-2}\quad(I).
\]

La expansión binomial es triangular e invertible y conserva exactamente los
\(2m-1\) grados de libertad originales. Los coeficientes del polinomio
aritmético se evalúan como \(L_{j-1}(\lambda L)\) y
\(L L^{(1)}_{j-2}(\lambda L)/(j-1)\). No se ha cambiado el espacio de núcleos
por usar esta representación. La conversión de los parámetros decimales al
JSON original se hace en racionales; el certificador comprueba la igualdad
exacta de ambas representaciones. Las constantes finales no dependen de una
inversión de matriz en coma flotante.

## Certificación global de (K) [ADAPT: v11, sección 7.1]

Se implementa la reducción de borde ya observada en v11. En cada semibanda
\(H=U-f\) es armónica, par en \(b\), continua hasta \(t=0^\pm\), con límites
uniformes

\[
 H(b,0^+)=U(b,0)-\pi,\qquad H(b,0^-)=U(b,0)+\pi,\qquad
 H(b,t)\longrightarrow0\quad(|t|\to\infty).
\]

Se certifican con Arb: \(U(b,0)>\pi\) para todo \(0\le b\le1/2\);
\(H(1/2,t)>0\) en ambos intervalos finitos de \(t\); y ambas colas del borde.
Las funciones se encierran mediante Taylor de segundo orden con resto intervalar
en intervalos cerrados, bisecando todos los intervalos no decididos. Para la
cola se usa la expansión con resto explícito de la sección 4.4 de v11 en
\(u=1/t\), incluyendo \(u=0\). Se aumenta \(T_1\) de 100 a 2000 si es necesario.

Para justificar el paso al interior, se aplica el principio del mínimo al
rectángulo \([-1/2,1/2]\times[\varepsilon,R]\). Por continuidad uniforme, el
borde inferior es \(\ge-o(1)\) al tender \(\varepsilon\) a cero; el superior
es \(\ge-o(1)\) al tender \(R\) a infinito. Los bordes verticales son
positivos. Haciendo ambos límites se obtiene \(H\ge0\) en toda la semibanda.
El argumento en la semibanda negativa es idéntico. Esto certifica todos los
\(b,t\) del dominio; no extrapola desde puntos de una malla.

### Certificador final por aislamiento completo de puntos críticos [DED/ADAPT]

Para los órdenes altos se ejecuta además `certify_kernel_critical.py`,
independiente del certificador por subdivisión. En el borde \(b=1/2\) se
escribe, con coeficientes racionales exactos,

\[
 U(1/2,t)=\frac{P_1(t)}{(x_1^2+t^2)^m}
         +\frac{P_2(t)}{(x_2^2+t^2)^m},\qquad x_{1,2}=d\pm\tfrac12.
\]

Los numeradores se obtienen expandiendo las partes real e imaginaria de
\((x-it)^j\). La derivada de \(f\) también es racional:

\[
 f'=-\frac{2x_1}{x_1^2+t^2}-\frac{2x_2}{x_2^2+t^2}
       +\frac{2d+1/2}{(2d+1/2)^2+t^2}
       +\frac{2d-1/2}{(2d-1/2)^2+t^2}.
\]

Por tanto \((U-f)'=N(t)/D(t)\), donde el denominador es estrictamente
positivo en toda la recta real. El programa forma \(N\) exactamente en
\(\mathbb Q[t]\), cancela factores comunes con el denominador —que no tienen
ceros reales— y guarda su numerador entero. Aísla **todas** sus raíces con
FLINT, verifica el número total con multiplicidades y evalúa \(U-f\) en los
intervalos que pueden contener raíces reales. No se acepta una lista de
raíces aproximadas. La garantía de aislamiento completo y las multiplicidades
se documentan en [FLINT, raíces certificadas](https://flintlib.org/doc/arb_fmpz_poly.html)
y en la documentación de `fmpz_poly.complex_roots` de python-flint.

Si \(U-f\) fuera negativo en alguna de las dos semirrectas, su valor positivo
en el extremo \(t=0^\pm\) y su límite cero en el infinito obligarían a un
mínimo negativo interior, que sería uno de esos puntos críticos. Las
evaluaciones positivas excluyen esta posibilidad. Se certifica por separado
todo el borde \(t=0\), \(0\le b\le1/2\), y se aplica el principio armónico ya
demostrado. Esta prueba cubre también las colas hasta el infinito sin fijar
una altura máxima. El límite de \(t^2(U-f)\) se comprueba positivo como control
adicional. Se cruzó el nuevo método con los certificados previos en núcleos
de referencia antes de aplicarlo al orden 100.

## Aritmética: fases acopladas y cola [LIT + DED]

Para \(p\le P_0\) se maximiza el polinomio que contiene **todas** las potencias
\(p^k\le N_0\). El certificador cubre la circunferencia completa por intervalos.
La cota de Taylor

\[
 f_p(x)\le f_p(x_m)+|f'_p(x_m)|r+
 \frac{r^2}{2}\sum_k k^2\sqrt{a_{p,k}^2+b_{p,k}^2}
\]

permite descartar intervalos; una cota de signo de la derivada reduce un
intervalo monótono a su extremo. Los restantes intervalos, que contienen los
puntos críticos posibles, se bisecan hasta que la cota superior y un valor
inferior evaluado difieren menos que la tolerancia indicada. No se identifica
el máximo de una malla con el máximo verdadero. Para \(p>P_0\) se usa la norma
de cada armónico. Toda potencia omitida por el corte entra en la cola global.

Para acelerar los primos grandes se demuestra además la siguiente cota global
[DED]. Escribiendo \(f_p(\phi_1+\delta)=R_1\cos\delta+g(\phi_1+\delta)\),
\(|\delta|\le\pi\), y \(L_g=\sum_{k\ge2}kR_k\), la desigualdad
\(1-\cos\delta\ge2\delta^2/\pi^2\) y Lipschitz dan

\[
 \max f_p\le R_1+g(\phi_1)+\frac{\pi^2L_g^2}{8R_1}.
\]

Se evalúa \(e^{i\phi_1}=(a_1+ib_1)/R_1\) con Arb, sin una malla de fases.
La cota solo se acepta directamente si su diferencia respecto al valor
inferior evaluado es menor que la tolerancia; en los restantes casos se
mantiene la subdivisión certificada. Para un solo armónico el máximo es
exactamente su norma.

También se incluyen en los máximos de \(p\le P_0\) potencias hasta \(10^{30}\),
aunque excedan el corte global \(N\). Sea \(D\) la suma de sus normas para
\(N<p^k\le10^{30}\). La cola global de normas ya contenía esos términos;
por tanto se resta una **cota inferior** de \(D\) al reemplazar los máximos
truncados por los ampliados. Es la identidad de separación de términos, no
una nueva estimación de \(\psi\). Las potencias que aún se omiten siguen
cubiertas por la cola. De esta forma el acoplamiento no queda artificialmente
limitado por \(p^k\le N\).

Sea \(g(x)=x^{-\sigma}h(\log x)\), con
\(\sigma=1/2+d\), \(h=\sqrt{a^2+b^2}\), y \(\Delta=\psi-x\). Integración por
partes de Stieltjes da, exactamente,

\[
 \sum_{n>N}\Lambda(n)g(n)
 =\int_N^\infty g(x)\,dx+(N-\psi(N))g(N)
              -\int_N^\infty\Delta(x)g'(x)\,dx.
\]

Por tanto se usa la cota [DED]

\[
 \int_{\log N}^\infty h(L)e^{(1-\sigma)L}\,dL
 +(N-\psi(N))h(\log N)N^{-\sigma}
 +\int_{\log N}^\infty\epsilon(e^L)e^{(1-\sigma)L}
                  |h'(L)-\sigma h(L)|\,dL.
\]

Se conserva el signo del término de borde y se evalúa conjuntamente
\(h'-\sigma h\), sin imponer monotonía global al peso ni reemplazarlo por un
mayorante escalonado. El peso es absolutamente continuo; en sus posibles ceros
se emplea la desigualdad de Lipschitz para la norma, válida casi en todas partes.

Las cotas externas [LIT] utilizadas son los lemas 6, 7 y 8 de Johnston,
Ramaré y Trudgian, *An explicit upper bound for L(1,χ) when χ is quadratic*:

- \(|\psi(x)-x|\le0.64673x/(\log x)^2\), \(x\ge10^5\).
- \(|\psi(x)-x|\le0.94\sqrt x\), \(11<x\le10^{19}\).
- \(|\psi(x)-x|\le1.994\cdot10^{-8}x\), \(x\ge e^{40}\).

Fuente primaria: <https://ramare-olivier.github.io/Maths/JRT_Submitted.pdf>.
Se verificaron los dominios. El código usa la segunda hasta \(e^{40}<10^{19}\),
la tercera desde allí y la primera como cota de cobertura. Son teoremas
incondicionales; sus comprobaciones finitas incorporadas no se convierten en
una hipótesis global de RH.

La integral principal usa cuadratura rigurosa de Arb, desplazando los polinomios
al centro de cada panel. El término con valor absoluto se encierra por
cuadratura intervalar en todos los subintervalos. El extremo infinito usa
polinomios de coeficientes absolutos e integrales gamma incompletas en forma
cerrada. El punto final se aumenta hasta que esa cota sea menor que \(10^{-25}\).
Esta elección evita las pérdidas que aparecían al fijarlo demasiado pronto.

### Ampliación del corte mediante momentos enteros certificados [DED]

`certify_arithmetic_binned.py` es una segunda implementación de la suma finita.
Usa una criba segmentada, con memoria independiente del corte global. Los
primos pequeños y todas sus potencias se suman directamente. Los primos
restantes son mayores que \(\sqrt N\) y solo aportan su primera potencia al
intervalo finito. Se agrupan en conjuntos disjuntos de primos, conservando el
conteo y los enteros exactos

\[
 \sum(p-p_m),\qquad\sum(p-p_m)^2.
\]

Para \(\phi(x)=\log x\,x^{-\sigma}h(\log x)\), Taylor con resto de Lagrange da

\[
 \sum_{p\in B}\phi(p)\in
 \#B\,\phi(p_m)+\phi'(p_m)\sum_{p\in B}(p-p_m)
 +\frac12\phi''([p_{\min},p_{\max}])\sum_{p\in B}(p-p_m)^2.
\]

La derivada segunda se evalúa conjuntamente como

\[
 \phi''(x)=e^{-(\sigma+2)L}
 \{Lh''+[2-(2\sigma+1)L]h'
       +[\sigma(\sigma+1)L-(2\sigma+1)]h\},\quad L=\log x.
\]

La identidad se verificó también simbólicamente. Las derivadas de la norma se
usan solo cuando su intervalo excluye cero; en caso contrario se aplica la
cota natural intervalar. La masa \(\psi(N)\) se encierra con el mismo Taylor
para \(\log p\). Se comprueba que los momentos enteros no desborden. Los
logaritmos de coma flotante eligen únicamente los grupos: sus extremos reales
son los primos enteros mínimo y máximo y se reevaluán con Arb, por lo que esa
elección no introduce una hipótesis numérica en el certificado.

La comparación independiente contra la suma directa hasta \(10^6\) está en
`certificates/binned_validation.json`. La diferencia observada entre las sumas
parciales fue menor que la suma de los errores certificados de agrupación y
maximización de fases. Los costes y pérdidas de los cortes mayores se
conservan en los JSON y registros de cada ejecución. La agrupación no sustituye
el teorema por una malla: cuenta todos los primos y encierra cada término.

## Parte elemental, transición y todos los T>1

Para el núcleo de alturas bajas se ejecutó `elem_gen.py` en modo S: encierra
las funciones completas sobre los 9215 intervalos de \([1,10^4]\), más el resto
explícito de v11 para \(T\ge10^4\). No usa valores puntuales como supremo.

Para cada núcleo alto se calcula exactamente con Arb la constante \(K\) de
v11, incluyendo la corrección de theta. Para \(T\ge e^{L_0}\) se obtiene

\[
 |S(T)|-a_0\log T\le C_\zeta-A\log(2\pi)
                 +(A-a_0)L_0+K e^{-L_0},
\]

pues \(A\le a_0\), \(\log T\ge L_0\) y \(1/T\le e^{-L_0}\). El término
\(K e^{-L_0}\) se incluye con redondeo hacia arriba, incluso cuando es diminuto.
Para \(1\le T\le e^{L_0}\), el núcleo `low_L60` da la cota

\[
 C_{\zeta,\mathrm{low}}+F^S_{\mathrm{low},\sup}
                  +(0.09473-a_0)L_0.
\]

La constante final es el máximo certificado de esas dos expresiones. La
transición elegida no necesita ser la intersección de dos rectas: ambos
intervalos cerrados se certifican hasta el mismo punto exacto \(e^{L_0}\).
La envolvente mínima de ambos núcleos también queda cubierta por esta prueba.
El comportamiento en el infinito queda controlado explícitamente por la
pendiente y el resto anterior.

En el refinamiento final, la opción `--Lswitch auto` ajusta además el punto de
cobertura: aproxima la intersección de las dos expresiones afines, elige un
valor racional con seis decimales y vuelve a evaluar **ambas** cotas, incluido
el resto exponencial. Por tanto la validez no depende de suponer que ese punto
sea una intersección exacta. El valor efectivo figura en cada certificado.

La identidad de v11 se demuestra fuera de las ordenadas. En una ordenada, el
valor por la derecha es límite de valores fuera de las ordenadas, y el miembro
derecho es continuo. La misma prueba por la izquierda controla el límite
izquierdo; el valor medio, si se usa esa convención, queda controlado por
convexidad del valor absoluto. No se supone simplicidad de los ceros.

## Cotas inferiores y alcance exacto

Hay dos tipos de cota inferior, que no deben confundirse.

1. `universal_lower_zeros.json` certifica un valor necesario para **cualquier**
   desigualdad uniforme \(|S(T)|\le a_0\log T+C\): se elige un punto racional
   fuera de las ordenadas, Arb certifica \(N(T)\), y se evalúa
   \(|N(T)-1-\theta(T)/\pi|-a_0\log T\). La búsqueda finita de ese punto no es
   una prueba de que maximice la expresión; un solo punto basta para la cota
   inferior. Esta cota se aplica también a cualquier envolvente de núcleos.

2. `*_dual_certificate.json` acota por abajo el óptimo **de un único núcleo**
   con \(d,m\) fijos, (K) y restricción de pendiente. Se relajan (K) a un conjunto
   finito de puntos y el supremo elemental a la cara superior en \(T=e^{100}\).
   Se acota \(C_\zeta\) por soportes lineales que evalúan, a fases racionales,
   la serie completa de cada primo hasta el corte en primos. Los primos
   restantes tienen máximos no negativos y pueden descartarse para esta
   cota inferior. Las series completas se calculan con
   \(\operatorname{Li}_{1-j}(z)\), funciones racionales para estos órdenes,
   y logaritmos para el término independiente.

   El LP numérico elige las restricciones activas. El verificador independiente
   forma con Arb el sistema dual **exacto**, resuelve para los multiplicadores
   reales y certifica que todos son positivos. Por dualidad débil, la suma de
   sus miembros derechos es una cota inferior rigurosa. No se usa como prueba
   el residuo o la brecha que imprime HiGHS. Las restricciones artificiales de
   caja, si resultasen activas, invalidarían ese certificado y se rechazan.

La segunda cota no se extiende a otras d, órdenes o envolventes sin otra prueba.
No se ha demostrado optimalidad absoluta ni una brecha pequeña para la unión
de todas las familias. `COMPARACION.md` distingue límites certificados,
candidatos numéricos y certificados duales del ámbito que corresponde.

## Incidencias y límites de la ejecución

Los registros se conservan también cuando fallan. La primera formulación
cónica tenía normas con factores exponenciales fuera del cono, lo que produjo
un error numérico de Clarabel; se movieron esos factores dentro. En Arb se
evitan potencias genéricas de intervalos de signo variable cuando la librería
devuelve `nan`; los certificados fallidos no se aceptaron. Una pérdida del
extremo de la cola en órdenes altos motivó el corte adaptativo explicado antes.

Reducir el margen de (K) sin refinar todos los mínimos cercanos al contacto
produjo un candidato no certificable entre puntos de la malla. Se corrigió la
búsqueda de mínimos continuos. Este es precisamente el motivo de exigir la
prueba independiente: ningún candidato fallido se presenta como teorema.

La exploración exterior, las cuadraturas de búsqueda y las brechas numéricas
no constituyen un certificado de optimalidad. La ejecución entrega las cotas
demostradas y los archivos para continuarlas, y señala expresamente todo lo
que no ha quedado agotado. No se propone una nueva versión del artículo.

El ensayo local `d100_m100_margin` fue rechazado por el aislamiento exacto:
en un punto crítico próximo a t=-94.738843 se certificó U-f<0, aproximadamente
-8.27·10^-14. Se conserva como intento fallido, sin certificado de (K).
Su campo C_est fue heredado del punto inicial y no evalúa los parámetros
modificados; no debe interpretarse como una mejora numérica. El trabajo
aritmético dependiente se interrumpió. `certify_candidate.py` detiene ahora la
cadena de etapas ante el primer fallo.

Las cotas superiores se redondean hacia arriba. Una **cota inferior** se
redondea hacia abajo, pues hacerlo hacia arriba podría invalidarla.

Los primeros ensayos de órdenes 200 y 1000 usaron 32 nodos de Gauss por panel
en log x. La cola de alta frecuencia quedó insuficientemente resuelta: la
reevaluación con 64, 128 y 256 nodos en sqrt(log x) eliminó las mejoras aparentes.
El código de búsqueda se corrigió antes del último ensayo de orden 1000. Los
registros y la versión anterior se conservan. Los números de ese objetivo
aproximante nunca se aceptaron como certificados.

En algunos registros históricos se editaron metadatos o aserciones defensivas
del certificador mientras un cálculo ya estaba en marcha; el hash inicial del
registro identifica el código cargado, mientras que el campo de hash escrito
al final puede reflejar la revisión posterior del archivo. Las revisiones se
conservan. El resultado final se reprodujo con una versión estable, y
`verify_chain.py` exige que su hash de código coincida con el archivo entregado.

<!-- FINAL_RESULTS -->

## Resultado seleccionado y alcance

### Valores finales

\[\boxed{|S(T)|\le0.08382\log T+3.418772350,\qquad T>1.}\]

| Cantidad | Valor | Alcance |
|---|---:|---|
| C anterior | 4.40577136 | Referencia del autor; paquete anterior no localizado |
| C nuevo | 3.418772350 | Cota superior uniforme certificada |
| C inferior | 0.688655186978719794671238 | Cota inferior necesaria para cualquier desigualdad uniforme, incluidas envolventes |

Reducción certificada respecto a la cifra de referencia: **0.986999010**.
Núcleo alto: d=1.0, m=100, 199 coeficientes.
Corte aritmético: 10000000000; fases acopladas hasta p=1000000; transición log T=135.199646.

No se ha probado optimalidad global. Para la familia fija de un núcleo d=0.95,m=10,
la cota dual es 3.280652819907774820834 y la cota superior 3.56656806163738605688624;
esta segunda comparación no se extiende a todas las envolventes.

### Verificación ejecutada

La reproducción completa terminó con C=3.418772350. Etapas superadas: low_kernel, low_arithmetic, low_elementary, high_kernel, high_arithmetic, envelope, universal_lower. Registro: `reproduction/20261106_171005`.

### Criterio de cierre indicado por el autor

Se priorizan mejoras de 0.0001 o mayores mientras el cálculo siga siendo rápido en el Mac. Se dejan de perseguir mejoras limitadas a la quinta cifra decimal o posteriores, y se evita extender cálculos cuyo coste resulte excesivo. Esto sustituye un criterio de agotamiento absoluto, que no se ha demostrado.

La suma ya se extendió de 455052511 primos hasta 10^10 a 4118054813 primos hasta 10^11 para un núcleo de orden 100. El beneficio de ese aumento fue de unas pocas centésimas de millonésima, muy por debajo del nuevo umbral. `ARITHMETIC_BUDGET.md` conserva los tiempos y los términos de error. No se confunde el corte P0 de fases conjuntas con el número total de primos incluidos.

El binario del autor fue validado por igualdad exacta con la criba completa (42.2 s en esta ejecución), sin modificarlo. Los ensayos nuevos agregan todos sus 455052511 primos. Las agregaciones y cuadraturas son herramientas numéricas de búsqueda; la prueba aritmética sigue siendo independiente.

### Órdenes superiores: reevaluación numérica separada

| Archivo | Orden | Nodos de Gauss por panel | Objetivo numérico |
|---|---:|---:|---:|
| d100_m100_lowmargin.json | 100 | 64 | 3.418902225600 |
| d100_m100_lowmargin.json | 100 | 128 | 3.418902238348 |
| d100_m100_lowmargin.json | 100 | 256 | 3.418902239851 |
| d100_m200_primoss.json | 200 | 64 | 3.419062690410 |
| d100_m200_primoss.json | 200 | 128 | 3.419064306059 |
| d100_m200_primoss.json | 200 | 256 | 3.419064216858 |
| d100_m1000_sparse_primoss.json | 1000 | 64 | 3.419214623128 |
| d100_m1000_sparse_primoss.json | 1000 | 128 | 3.419213243061 |
| d100_m1000_sparse_primoss.json | 1000 | 256 | 3.419213074046 |
| d100_m1000_sparse_resolved.json | 1000 | 64 | 3.418907097850 |
| d100_m1000_sparse_resolved.json | 1000 | 128 | 3.418907071290 |
| d100_m1000_sparse_resolved.json | 1000 | 256 | 3.418907070182 |

Estos números son evaluaciones numéricas de un objetivo aproximante, no cotas uniformes certificadas. La comparación se hace con los mismos datos y una cuadratura más densa en sqrt(log x). No se sustituyen por ellos los valores probados anteriores. El ensayo de orden 1000 libera 269 parámetros seleccionados, frente a los 1999 de la familia completa; no se afirma optimalidad en esa familia.

El ensayo corregido de orden 1000 (`d100_m1000_sparse_resolved.json`) terminó en 272.6 s. Su objetivo reevaluado no mejora al del núcleo vigente. No se inició una certificación aritmética costosa de ese candidato. El núcleo de orden 200 sí superó la prueba global de (K), aislando las 803 raíces de su polinomio derivado en 45.1 s, pero su reevaluación aritmética numérica tampoco ofreció la mejora requerida; no se publica una nueva constante a partir de él. Estos resultados explican el cierre práctico, sin excluir una mejora futura con otros parámetros ni con los 1999 coeficientes libres.

### Restricciones próximas al contacto

Para el núcleo seleccionado, A está entre 0.0838199999840863336458757 y 0.0838199999840863336458758; la holgura inferior del límite de t²(U-f) es 0.0000000190210633986148239999999. Los veinte puntos críticos más próximos al contacto y sus holguras dirigidas figuran en `certificates/active_constraints.json`. Son holguras certificadas, no una prueba dual de optimalidad.

La brecha global sigue siendo amplia. Las dos familias de un solo núcleo con dual certificado figuran en `certificates/fixed_family_gap_d095_m10.json` y `certificates/fixed_family_gap_d1006257_m10.json`; sus cotas inferiores no se trasladan a la unión de todas las envolventes. Para las demás familias no se ha obtenido un dual específico; sí les aplica la cota inferior universal.
