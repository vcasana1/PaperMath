# Comparación de resultados

Todas las cotas de esta tabla cubren **todo T>1**, con pendiente de referencia 0.08382.
La cifra anterior 4.40577136 se conserva como referencia del autor; su paquete no fue localizado.

| d | m | Coeficientes | C certificado | Corte N | Fases hasta p |
|---:|---:|---:|---:|---:|---:|
| 0.85 | 10 | 19 | 3.617361665 | 100000000 | 1000 |
| 1.006257 | 10 | 19 | 3.550718881 | 100000000 | 10000 |
| 0.85 | 12 | 23 | 3.564843682 | 1000000 | 10000 |
| 1.0 | 15 | 29 | 3.451028637 | 1000000 | 10000 |
| 1.0 | 20 | 39 | 3.428669516 | 100000000 | 1000 |
| 1.0 | 25 | 49 | 3.423587900 | 1000000 | 10000 |
| 1.0 | 40 | 79 | 3.420443518 | 1000000 | 10000 |
| 1.05 | 40 | 79 | 3.419376527 | 1000000000 | 10000 |
| 1.1 | 60 | 119 | 3.418966737 | 10000000000 | 1000000 |
| 1.0 | 80 | 159 | 3.419672796 | 200000000 | 10000 |
| 1.0 | 100 | 199 | 3.418799518 | 10000000000 | 1000000 |
| 1.0 | 100 | 199 | 3.418790008 | 100000000000 | 1000000 |
| 1.0 | 100 | 199 | 3.418790029 | 10000000000 | 1000000 |
| 1.0 | 100 | 199 | 3.418772350 | 10000000000 | 1000000 |
| 1.1 | 100 | 199 | 3.418794872 | 10000000000 | 1000000 |

Son mejores cotas superiores encontradas y certificadas para esos datos; no son pruebas de optimalidad en d o m.

Para un único núcleo con d=0.95,m=10, la dualidad exacta prueba 3.280652819907774820834 <= C_opt <= 3.56656806163738605688624; brecha certificada 0.28591524172961123605224. Esta comparación no se aplica a la unión de todas las familias ni a todas las envolventes.

La búsqueda HiGHS de orden 100 empleó una caja de parámetros [-10,10]. Su brecha impresa es numérica para ese modelo finito; no se usa como certificado. Los candidatos no incluidos en la tabla quedan como datos de búsqueda, aun si su estimación es favorable.
