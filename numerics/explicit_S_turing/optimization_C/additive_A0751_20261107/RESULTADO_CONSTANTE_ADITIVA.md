# Cota uniforme con coeficiente 0.0751

Resultado certificado, sin asumir RH:

$$|S(T)|\le 0.0751\log T+16.58585760,\qquad T>1.$$

La constante aditiva anterior era 23.08071071. La mejora es **6.49485311**, manteniendo exactamente el coeficiente 0.0751. No se ha demostrado optimalidad global.

| Construcción | Coeficiente de log T | Constante C |
|---|---:|---:|
| Primera cota explícita de esta familia | 0.0751 | 23.08071071 |
| Mismo núcleo, fases acopladas | 0.0751 | 20.71059150 |
| Reoptimización de grado 20 | 0.0751 | 19.51311422 |
| **Reoptimización de grado 40** | **0.0751** | **16.58585760** |

El resultado final utiliza grado 40, 79 parámetros racionales, 43 discos y 4 rectángulos, con d=0.9. Las cuatro etapas han pasado: desigualdad global del núcleo, costes armónicos, aritmética acoplada con cola infinita y envolvente uniforme. Los cálculos se han ejecutado en el Mac.

**[ADAPT]** Se ha adaptado la construcción de mayorantes racionales y Green–Jensen ya existente: fases del núcleo y de los centros tratadas conjuntamente, y minimización de C con el coeficiente 0.0751 fijado. Durante la reparación numérica se impone una restricción al coeficiente total; la aceptación final depende de los verificadores independientes con Arb. Una ruta [ADAPT], con dos variantes y dos grados; no se afirma novedad frente a la literatura ni se explora aquí una ruta exterior a esta familia.

## Certificado

- A_total <= 0.07508804928842704994878591.
- Coeficiente de log log T <= 0.3041957005315630725756451.
- Cambio a la envolvente de altura grande: log T = 745.904876.
- La cota final cubre todas las alturas T>1, incluyendo la convención derecha en los ceros, el límite izquierdo y el valor medio.

La cola aritmética se demuestra hasta infinito. El certificado directo usa N0=10^6 y P0=1000. La búsqueda numérica utiliza la cuadratura positiva derivada del binario completo primoss.bin, con 455 052 511 primos; esa cuadratura no se acepta como prueba. El coeficiente total A_total no se puede sustituir por el coeficiente de una recta ignorando el término positivo de log log T.

## Reproducción

Desde esta carpeta, con el entorno Python de pruebas:

```sh
python src/reproduce_certificate.py --slope 0.0751
python src/audit_and_select.py
```

El primer programa ejecuta de nuevo las cuatro etapas en una carpeta nueva. El segundo comprueba hashes y selecciona la menor constante certificada. Se conserva el historial de candidatos y resultados anteriores. Los candidatos de malla finita no se deben citar como cotas demostradas.

La v5 ya enuncia un resultado asintótico con coeficiente 0.0748883899703, sin constante aditiva ni altura inicial explícitas. Este paquete mejora la constante de una cota uniforme explícita y no aquel coeficiente asintótico.
