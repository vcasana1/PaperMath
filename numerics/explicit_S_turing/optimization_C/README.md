# Optimización de la constante uniforme de S(T)

Trabajo independiente del manuscrito v11. No se modifican sus fuentes ni los
certificados originales. Rama: `codex/optimize-uniform-S-constant`.

La cifra definitiva y los archivos que la justifican figuran en
`certificates/FINAL_RESULT.json` y en `INFORME_MATEMATICO.md`. Los JSON de
`candidates/` que tienen `certified: false` son salidas de búsqueda, no teoremas.
Un núcleo se acepta únicamente después de los certificados independientes de
(K), aritmética y cobertura de todas las alturas.

## Entorno

Desde este directorio, con Python 3.14 en el Mac utilizado:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Las versiones efectivamente utilizadas se conservan en `requirements.txt` y
`certificates/environment.json`. Arb aumenta la precisión con el orden del núcleo.
Los resultados publicados se imprimen con redondeo dirigido.

Todos los cálculos de esta entrega se ejecutan localmente en el Mac. El archivo
del autor `primoss.bin` se ha validado por comparación exacta con la criba
completa hasta 10^10: 455052511 enteros little-endian uint64. Su ruta y hash
figuran en `inputs/primoss_source.json`. Los ensayos de orden superior usan
todos sus primos, leyendo el archivo por bloques. Las certificaciones de la
suma aritmética regeneran independientemente la misma lista completa, y una
ampliación llega a los 4118054813 primos hasta 10^11.

## Reproducir el resultado certificado

```sh
.venv/bin/python src/reproduce.py
```

El programa vuelve a ejecutar el núcleo inferior de cobertura, su parte
elemental completa, el núcleo final, su constante aritmética y la envolvente.
Comprueba también el punto racional que proporciona la cota inferior universal.
Las salidas nuevas van en `reproduction/`, preservando los resultados de entrega.

La reproducción del certificado dual, cuando se desee, se ejecuta con:

```sh
.venv/bin/python src/lower_bound.py candidates/d095_m10_dual_input.json --verify
```

Ese dual se refiere a una familia fija de un solo núcleo. Su dominio exacto
figura en el certificado; no acota el óptimo absoluto de todas las envolventes.

## Repetir las búsquedas

```sh
OPENBLAS_NUM_THREADS=1 .venv/bin/python src/optimize.py --d 1.01 --m 10 --basis laguerre --eta 0.0000001 --out candidates/research.json
OPENBLAS_NUM_THREADS=1 .venv/bin/python src/adaptive_d.py
OPENBLAS_NUM_THREADS=1 .venv/bin/python src/cut_lp.py --d 1 --m 100 --out candidates/research_m100.json
```

El primer método usa CVXPY/Clarabel. El tercero usa planos de apoyo de bloques
de normas y de las fases, y programas lineales de HiGHS. Las cotas y brechas que
imprimen son numéricas para su discretización. La certificación posterior no
importa sus evaluaciones de funciones ni sus tolerancias de factibilidad.

Los ensayos de órdenes 200 y 1000 se ejecutan con `optimize_extension.py`.
`--m 200` libera todos los 399 parámetros. `--m 1000 --sparse 35` es una
extensión dispersa de orden 1000 con 269 parámetros libres; **no** optimiza
simultáneamente los 1999 parámetros de la familia completa. La recurrencia
de Laguerre ponderada evita desbordamientos numéricos. Sus resultados siguen
necesitando los certificados independientes.

El binario de 3.64 GB no se duplica en el ZIP. Su validación puede repetirse:

```sh
.venv/bin/python src/validate_prime_file.py /ruta/a/primoss.bin
```

El ZIP contiene la cuadratura numérica agregada de todos sus primos para repetir
las búsquedas sin ese archivo. La reproducción de la prueba no depende de esa
cuadratura ni de disponer del binario del autor.

```sh
OPENBLAS_NUM_THREADS=1 .venv/bin/python src/optimize_extension.py --m 1000 --sparse 35 --maxit 3 --primes primoss.bin --out candidates/research_m1000.json
OPENBLAS_NUM_THREADS=1 .venv/bin/python src/evaluate_extension.py certificates/final/solution.json candidates/research_m1000.json
```

La versión `optimize_extension_v1.py` conserva el primer ensayo histórico con
una cola insuficientemente resuelta; sus mejoras aparentes fueron rechazadas
por la reevaluación densa. La versión principal corrige la cuadratura usando
la variable sqrt(log x). Ninguno de esos ensayos numéricos es una cota probada.

## Archivos

- `src/`: búsqueda, certificadores y herramientas de reproducción.
- `inputs/`: coeficientes originales de referencia y petición del autor.
- `candidates/`: coeficientes completos y salidas de certificación.
- `certificates/`: resultado seleccionado, cotas inferiores y metadatos.
- `logs/`: registros completos, incluidos intentos fallidos documentados.
- `COMPARACION.md`: resultados comparables y su alcance.
- `SHA256SUMS`: integridad de la entrega, excluido el propio manifiesto.

La copia ZIP incluye las dependencias de código del repositorio necesarias
(`family/opt_line.py`, `family/elem_gen.py`, `hybrid_asymptotic/certutil.py`,
`hybrid_asymptotic/lpcommon.py`); no incorpora entornos virtuales ni cachés.

El paquete anterior `certificado_S_4_40577136.zip` y los cuatro verificadores
especificados en la petición no fueron localizados. La nueva prueba parte de
las fórmulas y datos de v11; no presupone la validez de 4.40577136.
