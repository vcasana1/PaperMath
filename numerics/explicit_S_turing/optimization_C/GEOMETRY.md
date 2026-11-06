# Discos alternativos y rectángulos: alcance de la ampliación

Esta etapa responde a la ampliación solicitada después de preparar el primer
ZIP. La cota certificada 3.418772350 se conserva como resultado de referencia.
Las búsquedas se separan de las pruebas independientes. El resultado geométrico
seleccionado y su reproducción están enlazados desde `certificates/FINAL_RESULT.json`.

## Procedencia

- [ADAPT] Los discos y el doblamiento por reflexión de los ceros proceden de
  v11, sección 5. Se varían centros, radios y desplazamientos conjuntamente
  con los coeficientes del núcleo.
- [ADAPT/DED] Para los rectángulos se adapta la identidad de Green--Jensen.
  La función de Green se construye a continuación por reflexión y se contrasta
  numéricamente con una expansión independiente de Fourier. No se reivindica
  novedad de esta construcción.
- [LIT] Las cotas verticales explícitas utilizadas para el perfil son
  [Hiary--Patel--Yang, teorema 1.1](https://arxiv.org/html/2207.02366v1),
  [Yang, teorema 1.1](https://arxiv.org/html/2301.03165v2), y la cota de
  Backlund de la sección 2 de
  [Trudgian](https://arxiv.org/html/1210.6743v1). La interpolación usa el
  [lema 3 de Trudgian](https://arxiv.org/html/1208.5846v2).

## Rectángulo y función de Green [DED]

Sea D=(a,b)×(-H,H), con a>=1/2, a<c<b y c>1. El polo de la función de
Green está en (c,0); los ceros reflejados evaluados tienen x=1/2+|β-1/2|<=1<c.
Escribimos W=b-a y k=π/(2H). La función de Green de la banda horizontal es

\[
g_H(u,y)=\operatorname{atanh}\frac{\cos(ky)}{\cosh(ku)}.
\]

Se obtiene aplicando el mapa exp(kz) al semiplano derecho y usando
log|(w+1)/(w-1)|. Tiene singularidad -log|z|, es armónica fuera del polo y
se anula en y=±H. La suma de imágenes

\[
G_D(c;x,y)=\sum_{n\in\mathbb Z}
 \{g_H(x-c+2nW,y)-g_H(x+c-2a+2nW,y)\}
\]

converge localmente uniformemente lejos del polo, por el decaimiento
exponencial de g_H. El cambio de índice n↦-n cancela los términos en x=a;
el cambio n↦-n-1 hace lo mismo en x=b. En el interior solo permanece el polo
de carga -log|z-c|. La unicidad del problema de Dirichlet demuestra que es
la función de Green del rectángulo; en particular, G_D>=0.

Para x<c, una segunda representación por separación de variables es

\[
G_D(c;x,y)=\frac{2\pi}{H}\sum_{n\ge1,\ n\text{ impar}}
\cos(k_n y)\frac{\sinh(k_n(x-a))\sinh(k_n(b-c))}
 {k_n\sinh(k_nW)},\qquad k_n=\frac{n\pi}{2H}.
\]

La normalización se fija con Δ(-log|z-c|)=-2πδ_c. Las pruebas numéricas
comparan esta serie con la suma de imágenes, sin usar esa comparación como
certificado intervalar. La evaluación se estabiliza factorizando exp(-k|u|).

## Coste de Green--Jensen [ADAPT]

Para el rectángulo trasladado verticalmente hasta T+v y sin el polo s=1,
la fórmula de Green aplicada a log|ζ| da

\[
\sum_{w\in D_T}G_D(c;w)
=\int_{\partial D_T}\log|\zeta(s)|\,d\omega_c(s)
-\log|\zeta(c+i(T+v))|.
\]

El miembro derecho se obtiene distribucionalmente de
Δ log|ζ|=2πΣm_wδ_w, con el signo de la función de Green anterior.
El producto de Euler da -log|ζ(c+it)|<=log(ζ(c)/ζ(2c)). El doblamiento de v11
produce la misma cota superior con factor 2 para los ceros originales y sus
pesos reflejados. En la desigualdad de S(T), dividida por 2π, el coste es
por tanto (J log T+G log log T+A)/π por unidad de peso geométrico.

Si h(x) es un dato de borde que depende únicamente de la abscisa, su extensión
armónica en (c,0) es

\[
\ell(c)+\sum_{n\ge1}\widehat h_n
 \frac{\sin(n\pi(c-a)/W)}{\cosh(n\pi H/W)},\qquad
\widehat h_n=\frac2W\int_a^b(h(x)-\ell(x))
\sin\frac{n\pi(x-a)}W\,dx,
\]

donde ℓ interpola h(a),h(b). Esta fórmula respeta los cuatro lados del
rectángulo. Se aplica separadamente a los perfiles e(x), g(x) y a(x). En el
código exploratorio los coeficientes se aproximan mediante una transformada
discreta de senos; todavía no son integrales certificadas.

## Perfil explícito y correcciones

Se utilizan los puntos σ=1/2, σ_k=1-k/(2^k-2), k=4,...,9, y σ=1. Las cotas
son 0.618·t^(1/6)·log t; 1.546·t^(1/(2^k-2))·log t; y log t en la 1-línea.
La última se toma en esta etapa por su demostración elemental independiente.
Se certifica con Arb el puente [3,50] y las condiciones compactas [0,3] de
la interpolación de (s-1)ζ(s), usando Q=3. En s=1 se usa la zeta desinflada
de FLINT: (s-1)ζ(s)=1+(s-1)(ζ(s)-1/(s-1)); no un resto supuesto de Stieltjes.
El resultado está en `certificates/geometry_PL_inputs.json`.

Entre las líneas, se interpolan linealmente e y log A. Para σ>1 se usa
log ζ(σ) por el producto de Euler. El coste de centro se añade una sola vez.
El lema de interpolación contiene **|log(Q+s)|**, distinto de log|Q+s|.
Por ello el ensayo incluye el término G·π²/(8(log T)²), además de G log log T.
Las correcciones de T+v y de |Q+s| respecto de T se incorporan explícitamente
en el certificado de envolvente; se justifican abajo desde log T>=10.

## Optimización ejecutada

La familia inicial contiene 168 discos y 840 rectángulos. Los discos usan
c∈{1.03,1.1,1.25,1.5,2,3}, abscisa izquierda en {0.5,0.65,0.8,0.9}, y siete
desplazamientos entre -1.5 y 1.5. Los rectángulos usan cinco centros, tres
abscisas izquierdas, dos extensiones a la derecha y cuatro semialturas entre
0.2 y 2, con los mismos desplazamientos.

`screen_geometry.py` optimiza conjuntamente el núcleo y los pesos no negativos.
El objetivo es el supremo del residuo de altura alta, aproximado por planos
en L=log T y refinado en el pico B/(0.08382-A). Se impone A+B/Lmax<0.08382,
lo que controla la derivada más allá de la última altura para este modelo.
Las desigualdades del núcleo se comprueban en dos dimensiones y se refinan
por cortes; las fases de los primos se refinan también. Se usa la agregación
de los 455052511 primos del archivo del autor.

## Certificación implementada y comprobaciones necesarias

La cadena ejecutada certifica la desigualdad geométrica completa
en dos dimensiones, las integrales armónicas y sus colas de series, las
correcciones explícitas de altura, la parte aritmética y la envolvente para
todo T>1. La reducción armónica al borde usada sin discos no se traslada:
los pesos extendidos por cero cambian de fórmula en las fronteras geométricas.
Ninguna salida de esta etapa se incorpora automáticamente al resultado probado.

### Reducción a todas las interfaces [DED/ADAPT]

La función H=U-f+ΣκG es armónica en cada celda abierta delimitada por los
lados de los rectángulos y las circunferencias. Los polos de Green están
fuera de la franja objetivo, pues c>1 y x=1/2+b<=1. H es continua a través
de las interfaces; t=0 se trata por sus dos límites. El principio del mínimo
se aplica por separado a cada celda. Por tanto basta certificar **todas** las
interfaces, b=0, b=1/2 y t=0, junto con las colas verticales. La simetría en b
extiende el resultado a la otra mitad de la franja. En las celdas no acotadas
se recorta en |t|=R y se usa H→0 uniformemente al hacer R→∞.

El certificador construye las interfaces independientemente en racionales.
La primera versión reutilizaba coordenadas de la búsqueda en coma flotante;
por ejemplo, 0.7-0.5 aparecía desplazado aproximadamente 4·10^-17. Esa versión
se sustituyó y se repitieron las pruebas con el lado **exacto** b=1/5. Las
salidas finales exigen la marca `constructed independently in exact rational
arithmetic` y enlazan el hash de la versión corregida.

En cada intervalo de una curva se conservan solo los pesos cuya región
interior contiene la caja completa; los demás se descartan por no negatividad.
El resultado es un minorante analítico en ese intervalo. Se encierra mediante
Taylor con segunda derivada intervalar. También se certifican monotonía y,
cuando H''>0, la cota obtenida completando el cuadrado. Las sumas de imágenes
de Green llevan restos exponenciales explícitos, incluidos sus derivados.
Las dos colas b=0 y b=1/2 se prueban aislando **todas** las raíces del numerador
racional exacto de (U-f)' y evaluando todos los puntos críticos exteriores a
los soportes geométricos. El límite en el infinito es cero. Así no se
extrapola una malla ni se omite la cola.

### Integrales armónicas rigurosas

El código de prueba no usa la transformada discreta de senos de la búsqueda.
Integra exactamente cada tramo lineal contra los senos, encierra el resto
de Fourier con una serie geométrica y evalúa la parte de Euler con cuadratura
Arb. Para x>1 se escribe x=1+exp(u) y

\[
\log\zeta(1+e^u)=\log\{1+e^u\zeta_{\rm def}(1+e^u)\}-u.
\]

Se corta en e^u=2^-48. El trozo omitido se mayoriza usando
ζ(x)<=x/(x-1), con la integral explícita de -log(x-1). La misma separación
elimina la singularidad integrable del coste circular. Los resultados J,G,A
se redondean individualmente hacia arriba y luego se multiplican por κ>=0.

### Corrección explícita de altura

Para toda geometría ensayada, |t-T|<=10 y Q+σ<=10 en la parte del borde donde
se aplica Phragmén--Lindelöf. Si L=log T>=10, T>20 y 110/(TL)<1,

\[
\log|Q+s|\le L+110/T,\qquad \log|s-1|\ge L-20/T,
\]

y |arg(Q+s)|<=π/2. Escribiendo ℓ=log|Q+s|,

\[
\log|\log(Q+s)|=\tfrac12\log(\ell^2+\arg(Q+s)^2)
 \le\log L+\frac{220}{T}+\frac{\pi^2}{8L^2}.
\]

Como e<=1/6, el resto total es menor que
(110(3+1/6)+20)/T<400/T. En la parte σ>1 el producto de Euler no necesita
esta corrección, pero añadir 400/T a todo el borde mantiene una cota superior.
Así se demuestra, sin un término O oculto,

\[
\sum_\rho W_k(b_\rho,\pm t_\rho)
\le2\{J_k L+G_k\log L+A_k+G_k\pi^2/(8L^2)+400/T\}.
\]

El signo ± equivale a reflejar el desplazamiento v; los costes son los mismos.
Las constantes se usan desde T=e^L0, con L0>=10; la geometría está lejos
del polo s=1. El núcleo de cobertura certificado cubre desde T=1 hasta allí.
El corte L0 se selecciona numéricamente y después se verifica como racional
exacto; no se presupone una igualdad exacta entre las dos ramas.

### Supremo uniforme

Con A=A_kernel+ΣκJ/π, B=ΣκG/π y δ=0.08382-A>0, se usa la identidad

\[
\sup_{L\ge L_0}\{-\delta L+B\log L\}
=B\{\log(B/\delta)-1\}
\]

cuando B/δ>=L0; en el otro caso se evalúa en L0. El resto π²B/(8L²) se acota
por su valor en L0 y el resto exponencial por su valor en T0. Esto absorbe
**todo** log log T y controla T→∞. El máximo de esta cota y la cobertura
inferior demuestra la recta uniforme final. No se usa el objetivo de una
altura aislada como sustituto del supremo.

Se exploran dos vías geométricas: una adaptación de los discos de v11 y una
adaptación de Green--Jensen con construcción de Green deducida aquí. No se
afirma que sean nuevas en la literatura ni que agoten todas las formas posibles.


## Acoplamiento exacto de los centros con los primos [DED]

La cota separada -log|ζ(c+it)|<=log(ζ(c)/ζ(2c)) pierde información:
las fases de cada término de centro son las mismas fases T log p del núcleo.
Se conserva por tanto su serie de Euler exacta en el polinomio de cada primo.
La procedencia es una deducción directa de la serie absolutamente convergente
para log ζ en Re(s)>1; no se reivindica novedad bibliográfica.

Sea σ0=d+1/2 y σ=min(σ0,c1,...,cr)>1. Si a0,b0 son los pesos originales,
los nuevos pesos son

\[
 a(L)=e^{-(\sigma_0-\sigma)L}a_0(L)
 -\sum_j\frac{\kappa_j}{\pi L}e^{-(c_j-\sigma)L}\cos(v_jL),
\]
\[
 b(L)=e^{-(\sigma_0-\sigma)L}b_0(L)
 +\sum_j\frac{\kappa_j}{\pi L}e^{-(c_j-\sigma)L}\sin(v_jL).
\]

Se mayoran ahora los máximos en x=T log p del polinomio
(log p)Σk p^(-kσ){a(k log p)cos(kx)+b(k log p)sin(kx)}.
El signo del seno resulta de -cos(kx+v k log p). Para la otra cota de S,
la reflexión x↦-x, v↦-v conserva el mismo máximo; no se añade otro coste.
En el coste de borde se retira la estimación de centro que ya estaba incluida
en A. Se resta su extremo **inferior** de Arb, de modo que el resto continúa
siendo un mayorante dirigido.

`certify_arithmetic_coupled.py` certifica estas funciones independientemente del
optimizador. Usa ramas y cotas intervalares de las fases, momentos enteros
exactos en los bins y una cota de segunda derivada para su exceso, así como
colas infinitas con el exponente real de cada centro c_j-1. Las identidades de
sus dos primeras derivadas y de la curvatura en x se contrastaron con
diferenciación automática independiente de series de Arb en
`certificates/coupled_weight_validation.json`. Este contraste ayuda a auditar
las fórmulas; la prueba de todas las fases y de las colas sigue siendo la del
certificador completo, no tres evaluaciones puntuales.

La optimización `screen_geometry_joint.py` modifica a la vez los coeficientes
del núcleo y los pesos de los rectángulos usando este acoplamiento. Después
se varían sus dimensiones y centros y se repite la cadena independiente.
Los números finales de discos y rectángulos se toman del resultado congelado. Ninguna de
estas búsquedas demuestra optimalidad en todas las geometrías posibles.


## Variación adicional de d y del orden [ADAPT/DED]

Se ensayan también valores de d distintos de 1 con λ=2d-1. La base estable
es z^-1(1-λ/z)^(j-1) en la parte real y z^-2(1-λ/z)^(j-2) en la imaginaria.
Su expansión binomial se convierte a los coeficientes monomiales exactos; el
verificador de (K) comprueba esa igualdad racional antes de iniciar la prueba.
Las transformadas son L_(j-1)(λL) y L·L_(j-2)^1(λL)/(j-1), respectivamente.
La identidad σ0-λ/2=1 permite conservar el mismo factor e^-L en los mapas
numéricos ponderados. El término libre conserva separadamente
exp(-(d+1/2)L)(exp(-dL)-2)/(πL).

Esta ampliación usa `screen_geometry_joint_general.py` y
`repair_geometry_general.py`; la prueba posterior sigue usando los mismos
certificadores independientes de (K), costes, aritmética y envolvente. La
condición de cola usada durante la búsqueda se adapta a
Σ_j (2d+2(j-1)λ)·parameter_R,j>=0. Es una condición necesaria de búsqueda;
la aceptación procede de las colas infinitas verificadas, no de esa condición.
La elevación de m inserta ceros exactos en los nuevos parámetros antes de
reoptimizar; no extrapola el éxito de un orden a otro.

## Perfil sub-Weyl verificado [LIT/ADAPT]

Se incorpora por una cadena separada el [teorema 1.1 de Patel--Yang](https://arxiv.org/html/2302.13444v1):
|ζ(1/2+it)|<=66.7·t^(27/164) para t>=3, sin hipótesis de ceros.
En el nodo crítico se sustituyen e=1/6, g=1, A=0.618 por
**e=27/164, g=0, A=66.7**. En los otros nodos se conservan las entradas
anteriores. El lema 3 de Trudgian permite exponentes logarítmicos distintos,
no negativos, en los dos bordes; solo requiere que los exponentes de la
potencia sean decrecientes. Aquí 27/164>1/14 y se cumple esa condición.
Se interpolan e, g y log A en el primer tramo; en los restantes g=1.

`certify_pl_inputs_subweyl.py` repite la prueba compacta en [0,3] con el
exponente logarítmico correcto. `certify_geometry_costs_subweyl.py` integra
el nuevo perfil g de forma exacta por tramos y certifica de nuevo todas las
integrales armónicas. Como 0<=g<=1 y e<=1/6, la corrección explícita
G·π²/(8L²)+400/T sigue siendo válida. La envolvente y el máximo en L
se recalculan; no se deduce una nueva cota restando una mejora numérica.

`certify_subweyl_candidate.py` conserva idénticos todos los bytes de los
coeficientes y de las geometrías, verificando su SHA-256. Eso permite reutilizar
las pruebas de (K) y de la aritmética para esos mismos datos. Los costes de
borde, las condiciones PL y la envolvente se ejecutan de nuevo. La reproducción
final vuelve a ejecutar también (K) y la aritmética, sin esa reutilización.
Los certificados originales de cada perfil se conservan por separado.

Se comprobó además el [teorema 1.1(a) de Revers](https://arxiv.org/html/2602.05614v1),
con constante 0.611 y el mismo exponente 1/6 y logaritmo para t>=3.
Su ahorro numérico en el ensayo de orden 60 fue de unos 3.7·10^-6; no se
persigue por el criterio del autor. El cambio sub-Weyl ahorró unas
4.2·10^-4 y sí se llevó a certificación. Estas comparaciones iniciales se
conservan en `certificates/boundary_profile_screen.json`, identificadas
expresamente como cribado numérico.

## Selección de nodos de interpolación [ADAPT/DED]

No es obligatorio usar todos los nodos de Yang a la vez. Se cribaron las
64 subfamilias de los seis nodos interiores, conservando 1/2 y 1. Para cada
subfamilia se aplican las mismas cotas verticales y el mismo lema PL a los
tramos consecutivos. Los exponentes de potencia siguen siendo decrecientes;
las condiciones compactas ya certificadas contienen todos los extremos usados.
El perfil seleccionado `pruned_subweyl` conserva k=4,5,6,7 y omite k=8,9.

Esta modificación puede empeorar la pendiente y mejorar la constante; por eso
se vuelve a calcular el supremo uniforme y no se compara únicamente A.
`certify_geometry_costs_pruned.py` integra el perfil seleccionado con Arb y
`certify_geometry_envelope_pruned.py` comprueba toda la envolvente. No se
identifica un perfil numéricamente favorable a una altura con una cota uniforme.
La búsqueda geométrica posterior usa este mismo perfil, manteniendo separados
sus costes numéricos y las integrales certificadas.

El cribado adicional de entradas de Patel en la 1-línea se conserva como
experimento numérico en `profile_subset_screen.json`. Su mejor ahorro estimado
respecto del perfil sin desplazamiento, para la solución de orden 60 y d=1.1,
fue de unas 5·10^-5. No se incorpora a la prueba ni se persigue ese refinamiento
por el criterio de parada del autor. No se usa la antigua cota 0.75 log t cuya
procedencia se vio afectada por el error de Kusmin--Landau.

## Reducción del coste de la certificación aritmética

`certify_arithmetic_coupled_fast.py` conserva las mismas funciones, derivadas,
fases y momentos exactos. El corte de la cola se busca usando por separado
el exponente del polinomio base y los exponentes c_j-1 de los centros. Todo
lo omitido sigue entrando mediante su mayorante positivo explícito. Se acepta
una cola residual de hasta 10^-14 y una tolerancia absoluta de cuadratura
Arb de 10^-18; las bolas finales, incluidos esos restos, se redondean hacia
arriba. No se descarta ningún primo ni se toma un resto por cero.

La comparación ejecutada sobre datos idénticos dio 113.4 s frente a 60.7 s,
con una diferencia entre los dos mayorantes menor que 5·10^-15.
`certificates/coupled_fast_comparison.json` enlaza ambos certificados y
comprueba la identidad AST de las fórmulas de derivación. La reproducción
final elige el programa exacto registrado en `FINAL_RESULT.json`.

El certificador `certify_geometry_kernel_fast.py` conserva las mismas funciones
de prueba y el mismo resto exponencial para la suma de imágenes. Reduce
únicamente el número de imágenes, eligiéndolo con desigualdades de Arb. En
una caja interior de un rectángulo de anchura W, |x-c| y |x+c-2a| son <=2W;
por tanto el parámetro D del resto satisface D>=2NW. Se aumenta N hasta que
los restos del valor y de las dos primeras derivadas sean <=10^-18. El
resto específico de cada caja sigue añadiéndose en la evaluación.

La prueba completa sobre la solución de la etapa 8 pasó de 309.7 s a 232.0 s
en estas ejecuciones. `certificates/fast_kernel_comparison.json` conserva ambas
pruebas, sus hashes y la comprobación AST de las funciones de prueba, que son
idénticas. Se mantienen todas las interfaces, la aritmética racional y las
raíces completas de ambas colas infinitas. Los snapshots de un mismo valor
con distinta cadena de prueba se guardan en directorios distintos.
