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

<!-- GEOMETRY_RESULTS -->

## Ampliación geométrica ejecutada

| C superior | m | Rectángulos | Discos | Perfil | Centros conjuntos | N | Candidato |
|---:|---:|---:|---:|---|:---:|---:|---|
| 3.261088008 | 40 | 7 | 0 | baseline | no | 10000000000 | geometry_m40_repaired |
| 3.233517487 | 40 | 7 | 0 | baseline | no | 100000000 | geometry_m40_refined1_repaired |
| 3.221892682 | 40 | 11 | 0 | baseline | no | 100000000 | geometry_m40_refined2_repaired |
| 3.215519918 | 40 | 12 | 0 | baseline | no | 100000000 | geometry_m40_refined3_repaired |
| 3.072778369 | 40 | 11 | 0 | baseline | sí | 100000000 | geometry_m40_refined2_repaired |
| 3.041017900 | 40 | 6 | 0 | baseline | sí | 100000000 | geometry_m40_joint_fixed_repaired |
| 3.030373080 | 40 | 8 | 0 | baseline | sí | 100000000 | geometry_m40_joint_neighbors1_repaired |
| 3.009218401 | 40 | 9 | 1 | baseline | sí | 100000000 | geometry_m40_joint_neighbors2_repaired |
| 3.006993157 | 40 | 8 | 1 | baseline | sí | 100000000 | geometry_joint_probe_d11_repaired |
| 3.004783351 | 40 | 13 | 2 | baseline | sí | 100000000 | geometry_m40_joint_neighbors3_repaired |
| 3.003249188 | 40 | 16 | 2 | baseline | sí | 100000000 | geometry_m40_joint_neighbors4_repaired |
| 3.003074882 | 40 | 16 | 2 | baseline | sí | 100000000 | geometry_m40_joint_neighbors5_repaired |
| 3.002915344 | 40 | 16 | 2 | baseline | sí | 100000000 | geometry_m40_joint_neighbors6_repaired |
| 3.001621579 | 60 | 8 | 1 | baseline | sí | 100000000 | geometry_joint_probe_m60_repaired |
| 3.001200823 | 60 | 8 | 1 | subweyl | sí | 100000000 | geometry_joint_probe_m60_repaired_subweyl |
| 2.988887398 | 60 | 11 | 1 | baseline | sí | 100000000 | geometry_joint_expanded_m60_d11_repaired |
| 2.988861006 | 60 | 11 | 1 | subweyl | sí | 100000000 | geometry_joint_expanded_m60_d11_repaired_subweyl |
| 2.988731893 | 60 | 11 | 1 | pruned_subweyl | sí | 100000000 | geometry_joint_expanded_m60_d11_repaired_pruned |
| 2.978049793 | 60 | 11 | 3 | pruned_subweyl | sí | 100000000 | geometry_m60_d1p1_joint_neighbors7_repaired |
| 2.976276009 | 60 | 11 | 3 | pruned_subweyl | sí | 100000000 | geometry_joint_round7_probe_d14_repaired |
| 2.969936673 | 60 | 16 | 3 | pruned_subweyl | sí | 100000000 | geometry_m60_d1p1_joint_neighbors8_repaired |
| 2.963951907 | 60 | 18 | 5 | pruned_subweyl | sí | 100000000 | geometry_m60_d1p1_joint_neighbors9_repaired |
| 2.963951287 | 60 | 18 | 5 | pruned_subweyl | sí | 10000000000 | geometry_m60_d1p1_joint_neighbors9_repaired |
| 2.960176836 | 60 | 16 | 6 | pruned_subweyl | sí | 100000000 | geometry_m60_d1p1_joint_neighbors10_repaired |
| 2.959227629 | 60 | 16 | 7 | pruned_subweyl | sí | 100000000 | geometry_m60_d1p1_joint_neighbors11_repaired |

Son resultados de cadenas ejecutadas, conservados como historial. El resultado seleccionado y reproducido con los verificadores principales actuales es el de `certificates/FINAL_RESULT.json`. Los metadatos indican qué certificados históricos conservan todos sus enlaces con las versiones actuales. Las versiones anteriores de los verificadores se preservan por separado.

La primera familia incluyó discos y rectángulos; la primera selección utilizó rectángulos; la búsqueda con centros conjuntos puede seleccionar también discos. La tabla no certifica optimalidad entre geometrías. Los ensayos de orden 1000 son búsquedas numéricas de 269 parámetros, no resultados de esta tabla. El intento geométrico de orden 100 se dejó sin certificar al encarecerse la prueba y resultar inferior a los candidatos de orden 40.
