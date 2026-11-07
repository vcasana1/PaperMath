# Handoff para ChatGPT — S(T), 7 de noviembre de 2026

## Resultado que se puede afirmar

Sin RH, |S(T)| <= 0.0751 log T + 16.58585760 para todo T>1. Convención derecha en los ceros; también se cubren límite izquierdo y valor medio. La cadena de pruebas con Arb está ejecutada y sus hashes comprobados. No se ha demostrado optimalidad.

La constante anterior para esta misma pendiente era 23.08071071. Las etapas certificadas intermedias son 20.71059150 y 19.51311422. La pareja final es **(0.0751,16.58585760)**.

## Fuentes autoritativas

Desde la raíz del repositorio o de la carpeta PaperMath extraída:

- numerics/explicit_S_turing/optimization_C/additive_A0751_20261107/FINAL_RESULT.json
- numerics/explicit_S_turing/optimization_C/additive_A0751_20261107/certificates/m40_envelope.json
- numerics/explicit_S_turing/optimization_C/additive_A0751_20261107/candidates/joint_C_m40_repaired.json
- numerics/explicit_S_turing/optimization_C/additive_A0751_20261107/RESULTADO_CONSTANTE_ADITIVA.md

El núcleo final tiene grado 40. La pendiente 0.0751 se fija durante la minimización de C; el coeficiente principal de la envolvente es aproximadamente 0.0750880492884, acompañado de un término positivo de log log T. No se debe suprimir ese término y afirmar una recta con la pendiente principal sin recalcular su constante.

## Qué se hizo

[ADAPT] Construcción de mayorantes racionales y Green–Jensen del manuscrito y del código existentes, con fases primas del núcleo y centros tratadas conjuntamente. Se minimizó C manteniendo 0.0751 y se probaron grados 20 y 40. La reparación numérica añade un tope lineal al coeficiente total. El certificado independiente no confía en la factibilidad numérica ni en las muestras de la malla.

Pruebas ejecutadas: desigualdad global mediante interfaces armónicas y colas verticales infinitas; costes armónicos con Arb; fase global de cada polinomio primo y cola analítica infinita; supremo analítico en log T y cobertura completa de alturas bajas.

La búsqueda emplea la cuadratura positiva procedente de los 455 052 511 primos del autor. El certificado final suma directamente los primos hasta 10^6 y demuestra el resto infinito. No es una verificación de S sobre una lista finita de alturas o ceros.

## Resultados que no deben mezclarse

- La pareja antigua 0.08382, 2.959227629 tiene otro coeficiente. No se puede combinar su constante con 0.0751.
- La v5 ya enuncia limsup |S(T)|/log T < 0.0748883899703, sin altura ni constante aditiva explícitas. Esta entrega no mejora ese coeficiente asintótico.
- Los C_numerical de los archivos de búsqueda no son cotas demostradas. Citar el C_upper certificado.
- No se demuestra RH ni optimalidad global.

## Reproducción y estado

Con Python y las dependencias fijadas del ZIP:

```sh
python numerics/explicit_S_turing/optimization_C/additive_A0751_20261107/src/reproduce_certificate.py --slope 0.0751
python numerics/explicit_S_turing/optimization_C/additive_A0751_20261107/src/audit_and_select.py
```

Trabajar en el Mac, conservar manuscritos y certificados históricos y separar nuevos ensayos de resultados certificados. El usuario pidió una tentativa de reducir C y después subir todo a PaperMath; no convertir la entrega en una modificación automática del manuscrito v6.

Esta pasada usa una ruta [ADAPT] dentro de la familia existente. No se afirma novedad frente a la literatura.

## Validación del ZIP entregado

El ZIP se extrajo en una carpeta nueva y allí se ejecutaron de nuevo las cuatro etapas, usando exclusivamente archivos de esa extracción. Resultado exacto reproducido: 0.0751, 16.58585760. Estado PASS en PACKAGE_VALIDATION.json. SHA-256: `f242a3995dbecd109e134736ba3a8d96e9dba0249b6a3188341aff7cb9c47a06`.
