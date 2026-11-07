# Coeficiente de log T: resultado explícito del 7 de noviembre de 2026

Se ha certificado, sin asumir RH,

\[
|S(T)|\le 0.0751\log T+23.08071071,\qquad T>1.
\]

La cadena completa tiene estado **PASS** y la pareja se ha reproducido íntegramente en una carpeta nueva, sin volver a ejecutar la búsqueda numérica. Se usa la convención original: S continua por la derecha en los ceros; la cota también cubre el límite izquierdo y el valor medio.

## Parejas verificadas

Todas las constantes siguientes están redondeadas hacia arriba y corresponden a cotas uniformes para todo T>1:

| Coeficiente a de log T | Constante aditiva C | Estado |
|---:|---:|---|
| 0.08382 | 2.959227629 | Certificado anterior, conservado |
| 0.0830 | 3.151694782 | Nueva cadena PASS |
| 0.0828 | 3.242277741 | Nueva cadena PASS |
| 0.0758 | 16.46762913 | Nueva cadena PASS |
| **0.0751** | **23.08071071** | **Nueva cadena PASS y reproducción completa** |

El coeficiente 0.0751 es menor que el umbral solicitado 0.0832. La reducción del coeficiente se obtiene aceptando una constante mayor. Para conservar una constante próxima a 3, la pareja 0.0828, 3.242277741 también cruza ese umbral.

## Procedencia y qué se ha cambiado

**[ADAPT]** Se parte del núcleo asintótico de la v5 y de los programas ya existentes de mayorantes racionales y Green–Jensen. Se lo combina con el perfil de crecimiento explícito `pruned_subweyl`, se añaden las geometrías del certificado anterior y se minimiza directamente el coeficiente total de log T. La constante aritmética se calcula después, con prueba de la cola infinita.

La primera conversión del núcleo antiguo, sin esa reoptimización, ya dio la pareja 0.076, 18.28111288. Los nuevos ensayos de grados 10 y 20 producen las dos últimas filas de la tabla. La pareja con 0.0751 utiliza grado 20, 39 parámetros racionales, 42 discos y 4 rectángulos, con d=0.9. La pareja con 0.0828 utiliza grado 60, 119 parámetros, 6 discos y 12 rectángulos.

No se ha modificado ningún manuscrito ni ningún archivo seguido previamente por Git. Las búsquedas finitas y sus reparaciones no se consideran pruebas: cada resultado de la tabla requiere la certificación independiente posterior.

Una ruta [ADAPT]; no se propone aquí una ruta exterior a esta familia ni se afirma novedad frente a la literatura.

## Cierre de la envolvente

**[DED]** La curva superior certificada para alturas grandes tiene la forma

\[
R+A_{\rm total}L+B\log L+E(L),\qquad L=\log T,
\]

con E(L) acotado explícitamente por E(L0) para L>=L0. Para la mejor pendiente de esta entrega:

- A_total <= 0.07508542266316091887835288.
- B <= 0.4140252696659695619864748.
- L0 = 1076.768520.

Para un coeficiente a>A_total se toma delta=a-A_total>0. El máximo de -delta L+B log L en L>=L0 está en L=max(L0,B/delta). Se añade R y la corrección positiva E(L0), y se combina con la cota de baja altura, válida en el intervalo completo. Para a=0.0751, la constante final redondeada hacia arriba es 23.08071071.

A_total no se debe presentar como coeficiente de una recta con constante finita ignorando el término B log L. Tampoco se debe presentar como coeficiente total la contribución del núcleo antes de sumar el coste de las geometrías.

## Verificación y cambios de código

1. Desigualdad global del núcleo: interfaces completas por aritmética de bolas y principio del mínimo; las dos colas verticales infinitas se verifican mediante aislamiento exacto de raíces.
2. Costes armónicos de las geometrías: integrales y restos con Arb, independientes de la búsqueda.
3. Término aritmético: fases globales, sumas finitas y cola analítica hasta infinito. En las parejas 0.0751 y 0.0758 se usa N0=10^6 (78 498 primos directos); en las parejas 0.0828 y 0.0830 se usa N0=10^8 (5 761 455 primos directos). Estos cortes no limitan la altura de validez de la cota.
4. Envolvente: supremo analítico sobre todas las alturas grandes y cobertura completa de alturas bajas.
5. Control de hashes de entradas, programas e insumos analíticos: PASS.
6. Reproducción completa de la pareja 0.0751 en una carpeta nueva: PASS.

El verificador de envolvente se ha parametrizado por la pendiente. Antes de aplicarlo se comprobó que reproduce exactamente cinco campos numéricos del certificado anterior: C, cota alta, cota baja, A_total y B.

El verificador de costes contiene una simplificación exacta en el extremo izquierdo de los círculos: si x=c-R, entonces arccos((x-c)/R)=pi. Se evalúa pi directamente para evitar que el redondeo de una división en bolas produzca un argumento que salga ligeramente del dominio de arccos. Las fórmulas de integración y de error se conservan.

## Reproducción en el Mac

Desde cualquier carpeta, con el entorno de pruebas instalado:

```sh
/private/tmp/optimization_C_venv/bin/python '/Users/vcasana/Documents/ChatGPT/Möbius/PaperMath_optimization_C/numerics/explicit_S_turing/optimization_C/slope_optimization_20261107/src/reproduce_slope_certificate.py' --slope 0.0751
/private/tmp/optimization_C_venv/bin/python '/Users/vcasana/Documents/ChatGPT/Möbius/PaperMath_optimization_C/numerics/explicit_S_turing/optimization_C/slope_optimization_20261107/src/audit_slope_results.py'
```

El primer programa vuelve a ejecutar las cuatro etapas sobre los coeficientes racionales guardados. No necesita el binario de 455 millones de primos ni acepta la malla numérica de búsqueda como prueba. El segundo comprueba la cadena almacenada y sus hashes. Las pendientes alternativas admitidas por el reproductor son 0.0758, 0.0828 y 0.0830.

Archivos principales:

- [Cadena de prueba](/Users/vcasana/Documents/ChatGPT/Möbius/PaperMath_optimization_C/numerics/explicit_S_turing/optimization_C/slope_optimization_20261107/certificates/proof_chain_status.json).
- [Certificado de la pendiente 0.0751](/Users/vcasana/Documents/ChatGPT/Möbius/PaperMath_optimization_C/numerics/explicit_S_turing/optimization_C/slope_optimization_20261107/certificates/A0.0751_envelope.json).
- [Registro de reproducción completa](/Users/vcasana/Documents/ChatGPT/Möbius/PaperMath_optimization_C/numerics/explicit_S_turing/optimization_C/slope_optimization_20261107/logs/reproduction_A0751.log).
- [Coeficientes racionales del núcleo de grado 20](/Users/vcasana/Documents/ChatGPT/Möbius/PaperMath_optimization_C/numerics/explicit_S_turing/optimization_C/slope_optimization_20261107/candidates/slope_m20_repaired.json).
- [Reproductor](/Users/vcasana/Documents/ChatGPT/Möbius/PaperMath_optimization_C/numerics/explicit_S_turing/optimization_C/slope_optimization_20261107/src/reproduce_slope_certificate.py).

## Límites de lo afirmado

Se ha obtenido una mejora uniforme explícita del coeficiente. No se ha demostrado optimalidad global, ni agotado la elección de grados, parámetros o geometrías. Las búsquedas se ejecutaron localmente en el Mac.

La v5 ya enuncia una cota asintótica menor, limsup |S(T)|/log T < 0.0748883899703, sin altura inicial ni constante aditiva explícitas. Esta entrega no mejora aquel coeficiente asintótico: convierte y reoptimiza la construcción para obtener parejas uniformes explícitas. No se ha realizado en esta pasada una nueva auditoría integral de todos los teoremas de la v5.
