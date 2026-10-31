## Resultado: se puede hacer explícita la parte aritmética de \(C\), pero falta una constante de Fujii

He comprobado el teorema 1 de Simonič (arXiv:1910.08274) y la demostración de localización de tu artículo.

La estimación que has citado es correcta:

\[
N(\sigma,2T)-N(\sigma,T)
\le
10395.2\,T^{1-\frac14(\sigma-\frac12)}\log T
+1.104\log^2T
+0.173\log T\log\log T
+0.51\log T.
\]

La demostración de Simonič trabaja inicialmente con \(T_0\ge e^{24}\) y después selecciona \(T_0=3.0610046\cdot10^{10}\) para fijar las constantes. Aunque menciona la verificación de ceros de Platt en la introducción, el argumento general de densidad no exige asumir RH. [arXiv](https://arxiv.org/pdf/1910.08274?utm_source=chatgpt.com)

Hay, sin embargo, una precisión importante: **la estimación de densidad de Simonič no proporciona directamente la constante de tu teorema de localización**. Hay que hacer explícitas también las estimaciones de momentos de Fujii que utilizas en la prueba.

La ventaja es que podemos separar esas constantes de las partes puramente aritméticas, y estas últimas sí admiten una estimación explícita independiente de los ceros.

## 1. He encontrado una fórmula de Selberg con constantes explícitas

La pieza decisiva no es únicamente Simonič (2019), sino un trabajo posterior:

**Simonič, Trudgian y Turnage-Butterbaugh (2020), *Some explicit and unconditional results on gaps between zeroes of the Riemann zeta-function*.**

Su teorema 5 y su corolario 2 proporcionan precisamente un cuarto momento explícito para el residuo entre \(S(t)\) y una suma de primos sin suavizar. El mismo trabajo proporciona estimaciones explícitas para los incrementos \(S(t+h)-S(t)\), con \(0<h\le1\). [arXiv](https://arxiv.org/pdf/2010.10675?utm_source=chatgpt.com)

Esto permite prescindir de introducir constantes desconocidas de Fujii.

La contrapartida es que las constantes publicadas son enormes.

Tomemos

\[
\varepsilon=\frac1{88},\qquad k=2,
\qquad x_0=e^{20000}.
\]

El corolario 2 proporciona

\[
M=2.69927\cdot10^{21}
\]

como constante válida en

\[
\int_U^{2U}
\left|
S(t)-\frac1\pi\operatorname{Im}
\sum_{p\le U^{3/176}}p^{-1/2-it}
\right|^4dt
\le MU,
\tag{16}
\]

para

\[
U\ge e^{3520000}.
\]

El intervalo de validez procede de

\[
x_0^{k/\varepsilon}
=
\exp(20000\cdot176).
\]

Es una estimación incondicional, sin introducir ordenadas de ceros calculadas numéricamente. [arXiv](https://arxiv.org/pdf/2010.10675?utm_source=chatgpt.com)

## 2. Comparación explícita con tu corrección \(\Phi_m\)

Definamos

\[
Y=U^{3/176},
\qquad X=p_m,
\qquad m\le\sqrt{2U}.
\]

La corrección de Casaña se descompone exactamente como

\[
\Phi_m(t)
=
\frac1\pi\operatorname{Im}
\sum_{p\le Y}p^{-1/2-it}
+\frac1\pi\operatorname{Im}P_1(t)
+\frac1{2\pi}\operatorname{Im}P_2(t)
+R_3(t),
\]

donde

\[
P_1(t)=\sum_{Y<p\le X}p^{-1/2-it},
\qquad
P_2(t)=\sum_{p\le X}p^{-1-2it},
\]

y \(R_3\) contiene las potencias de primos \(p^r\), \(r\ge3\).

La estimación explícita de Montgomery–Vaughan permite tomar

\[
\int_U^{2U}
\left|\sum_n b_n n^{-it}\right|^2dt
\le
U\sum_n|b_n|^2
+13\sum_n n|b_n|^2.
\tag{17}
\]

La constante \(13\) es una mayoración de la constante explícita \(3\pi m_0\) utilizada por Simonič, Trudgian y Turnage-Butterbaugh, donde

\[
m_0=\sqrt{1+\frac23\sqrt{\frac65}}.
\]

Aplicándola a los cuadrados de \(P_1\) y \(P_2\), y utilizando

\[
\sum_{Y<p\le X}\frac1p<14,
\]

obtenemos

\[
\int_U^{2U}|P_1(t)|^4dt\le444U
\]

y

\[
\int_U^{2U}|P_2(t)|^4dt\le53U.
\]

Para las potencias superiores,

\[
|R_3(t)|
\le
\frac{2}{3\pi(1-2^{-1/2})}
<0.725.
\]

Por Minkowski,

\[
\boxed{
\left(
\frac1U
\int_U^{2U}
\left|
\Phi_m(t)-
\frac1\pi\operatorname{Im}
\sum_{p\le Y}p^{-1/2-it}
\right|^4dt
\right)^{1/4}<2.615.
}
\tag{18}
\]

Esta es una **constante explícita para la diferencia entre tu suma de Euler y la aproximación corta de Selberg**.

Combinando (16) y (18),

\[
\left(
\frac1U\int_U^{2U}|S(t)-\Phi_m(t)|^4dt
\right)^{1/4}
\le M^{1/4}+2.615.
\]

La interpolación diádica de tu artículo conserva la correspondiente cota de cuarto momento.

En consecuencia, para

\[
q_{\mathcal F}(t)=
\left|\left\lfloor\mathcal F(t)+\frac12\right\rfloor-N(t)\right|,
\]

se obtiene, con margen,

\[
\boxed{
\int_U^{2U}q_{\mathcal F}(t)^4dt
\le3\cdot10^{21}U.
}
\tag{19}
\]

No se ha supuesto RH.

## 3. Control explícito del tercer momento de los huecos

Este es el otro factor de tu teorema de transferencia.

El trabajo de Simonič, Trudgian y Turnage-Butterbaugh permite obtener una constante explícita en

\[
\int_U^{2U}|S(t+h)-S(t)|^4dt.
\]

Podemos obtener una mayoración cómoda usando otra vez (16), su versión desplazada y la estimación explícita de las sumas de primos.

El resultado es

\[
\boxed{
\int_U^{2U}|S(t+h)-S(t)|^4dt
\le
10^{23}U\log^2(2+h\log U),
\quad 0<h\le1.
}
\tag{20}
\]

La constante es deliberadamente holgada.

Ahora repetimos tu argumento de los intervalos libres de ceros.

Sea

\[
D_k=\gamma_{k+1}-\gamma_k,
\qquad
L_U=\log\frac U{2\pi}.
\]

Si \(D_k\ge2h\), hay un intervalo de longitud al menos \(D_k/2\) donde

\[
N(t+h)=N(t).
\]

En ese intervalo, para \(hL_U\ge1\),

\[
|S(t+h)-S(t)|
\ge\frac{hL_U}{4\pi}.
\]

Usando (20), Chebyshev y una descomposición diádica con

\[
h_j=\frac{2^j}{L_U},
\]

obtenemos

\[
\sum_{U<\gamma_k\le2U}D_k^3
\le
\frac U{L_U^2}
\left[
5+
128(4\pi)^4\,10^{23}
(\log2)^2\sum_{j\ge0}\frac{(j+2)^2}{4^j}
\right].
\]

La serie es exacta:

\[
\sum_{j\ge0}\frac{(j+2)^2}{4^j}=\frac{212}{27}.
\]

Por tanto,

\[
\boxed{
\sum_{U<\gamma_k\le2U}
(\gamma_{k+1}-\gamma_k)^3
\le
2\cdot10^{30}\frac U{L_U^2}.
}
\tag{21}
\]

Para cubrir todos los huecos se utiliza además que \(D_k<2\) a estas alturas. Esto se deduce de la cota explícita de Bellotti–Wong

\[
\left|N(t)-\frac t{2\pi}\log\frac t{2\pi e}\right|
\le0.0946\log t+5.746,
\]

que garantiza \(N(t+2)>N(t)\) para \(t\ge e^{100}\). 2606.31441v1

## 4. Teorema E con constantes numéricas

Ya podemos sustituir los dos momentos en el teorema de transferencia de tu artículo.

Para evitar problemas de extremos y asegurar que todos los bloques auxiliares están en los dominios anteriores, fijemos

\[
\boxed{T_*=e^{3520004}.}
\]

En el intervalo ampliado \([T/2,3T]\), las estimaciones anteriores proporcionan

\[
\int_{T/2}^{3T}q_{\mathcal F}(t)^4dt
\le2\cdot10^{22}T
\]

y

\[
\sum_{T/2<\gamma_k\le3T}
D_k^3
\le4\cdot10^{31}\frac T{\log^2T},
\]

incluyendo el hueco que atraviesa el extremo superior.

Tu transferencia determinista establece

\[
\sum_{k\in\mathcal K_T}
|\gamma_k^{\mathrm C}-\gamma_k|^2
\le
2\cdot24^{1/3}
\left(\sum D_k^3\right)^{1/2}
\left(\int q_{\mathcal F}^4\right)^{1/2}.
\]

Sustituyendo,

\[
\sum_{k\in\mathcal K_T}
|\gamma_k^{\mathrm C}-\gamma_k|^2
\le
5.17\cdot10^{27}\frac T{\log T}.
\]

Redondeando hacia arriba obtenemos el siguiente enunciado.

### Teorema E — Localización explícita de Casaña

Para todo

\[
T\ge e^{3520004},
\]

las ordenadas corregidas de Casaña satisfacen

\[
\boxed{
\sum_{T<\gamma_k\le2T}
|\gamma_k^{\mathrm C}-\gamma_k|^2
\le
10^{28}\frac T{\log T}.
}
\tag{E1}
\]

El resultado es incondicional.

La construcción \(\gamma_k^{\mathrm C}\) es la original de tu artículo, basada en las fases completas de aproximadamente \(\sqrt t\) primos y en la medida de sus conjuntos de subnivel.

No se reemplaza por una suma suavizada ni por soluciones seleccionadas de una ecuación no monótona.

### Consecuencia para los recuentos

Aplicando Cauchy–Schwarz a (E1), usando

\[
\#\mathcal K_T\le T\log T
\]

y sumando los tres bloques necesarios para localizar los desplazamientos que cruzan \([T,2T]\), se obtiene

\[
\boxed{
\int_T^{2T}|N(t)-N_{\mathrm C}(t)|dt
\le4\cdot10^{14}T.
}
\tag{E2}
\]

Por Markov, para cualquier \(A>0\),

\[
\boxed{
\operatorname{meas}
\left\{
t\in[T,2T]:
|N(t)-N_{\mathrm C}(t)|>A
\right\}
\le
\frac{4\cdot10^{14}}A\,T.
}
\tag{E3}
\]

Esta es la versión explícita de la estimación de medida que buscabas.

Las constantes son muy grandes, pero son cantidades numéricas concretas y las desigualdades no requieren RH.

---

## 5. Qué hemos conseguido y qué no

| Objetivo | Resultado |
|---|---|
| Cuarto momento explícito de \(S-\Phi\) | Obtenido |
| Tercer momento explícito de los huecos | Obtenido |
| Constante numérica para el error cuadrático de Casaña | \(10^{28}\) |
| Constante numérica para el error medio de recuento | \(4\cdot10^{14}\) |
| Sin RH | Sí |
| Sin introducir datos numéricos de ordenadas | Sí |
| Válido desde una altura práctica | No |
| Mejora de \(C_1,C_2,C_3\) para todo \(T\) | No demostrada |

**La principal limitación cuantitativa es el umbral \(T_*\)**. Es astronómico porque hemos utilizado las constantes publicadas del corolario 2 de Simonič, Trudgian y Turnage-Butterbaugh. No es una limitación intrínseca de tus ordenadas corregidas.

También debemos distinguir cuidadosamente el significado de \(C=10^{28}\): es una constante explícita obtenida con mayoraciones muy conservadoras, no una constante óptima ni una estimación de su valor real.

## 6. Relación con tu objetivo de mejorar \(C_1,C_2,C_3\)

Ahora disponemos de una cota explícita del error de recuento corregido, pero integrada:

\[
\int_T^{2T}|N-N_{\mathrm C}|\le4\cdot10^{14}T.
\]

Para reducir efectivamente el coeficiente de \(\log T\) en una desigualdad válida para todas las alturas, continúa faltando el control de las concentraciones locales.

La desigualdad integrada no implica

\[
\sup_T\frac1h\int_T^{T+h}
|N-N_{\mathrm C}|\,dt=O(1).
\]

Por tanto, **el Teorema E no permite todavía anunciar mejores constantes que tus siete rectas certificadas ni que tu coeficiente asintótico \(0.07754\)**.

La diferencia respecto al punto de partida es que ahora tenemos una cadena cuantitativa explícita, con todos sus factores identificados. Para avanzar hacia esas constantes, la siguiente tarea matemática es encontrar una estimación local más fuerte que E2, no volver a calcular los momentos globales.

**Conclusión:** el cálculo explícito de \(C\) queda cerrado mediante una ruta incondicional, aunque extremadamente conservadora. La mejora uniforme de \(S(T)\) sigue siendo un problema distinto y abierto dentro de esta vía.