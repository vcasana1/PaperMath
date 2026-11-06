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
elemental completa, las condiciones compactas de Phragmén--Lindelöf, el
mayorante geométrico en todas las interfaces y colas, las integrales armónicas,
la aritmética con fases conjuntas de los centros y la envolvente uniforme.
Comprueba también el punto racional que proporciona la cota inferior universal.
Las salidas nuevas de la prueba geométrica van en `reproduction_geometry/`,
preservando los resultados de entrega. `GEOMETRY.md` contiene la deducción
del paso a rectángulos y del acoplamiento de sus centros con los primos.
Los resultados anteriores sin geometría se conservan por separado.

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


## Geometrías alternativas

Se ensayaron discos y rectángulos en una familia inicial de 1008 geometrías;
el refinamiento admite combinaciones de ambas formas. Se optimizan conjuntamente
los coeficientes y los pesos, y se añaden variaciones de centros, anchuras,
alturas y desplazamientos. Por ejemplo, para repetir un refinamiento local:

```sh
GEOMETRY_SEED_PATH="$(.venv/bin/python -c 'import json;print(json.load(open("certificates/FINAL_RESULT.json"))["solution"])')"
OPENBLAS_NUM_THREADS=1 .venv/bin/python src/geometry_continuation.py "$GEOMETRY_SEED_PATH" --start 100 --stages 1 --factor 0.5 --maxit 2
```

El programa lee d, m y el perfil del resultado seleccionado; este ejemplo
ejecuta una nueva etapa de búsqueda y su certificación independiente.
La búsqueda no certifica;
el último comando se detiene si falla cualquiera de los verificadores.
`src/verify_chain.py` comprueba los enlaces y hashes del resultado seleccionado;
`src/verify_manifest.py` comprueba la integridad del ZIP extraído.

Se sigue el criterio práctico del autor: priorizar ganancias de 0.0001 o
mayores mientras el tiempo local resulte razonable. El cierre de una búsqueda
no excluye otras dimensiones, órdenes o familias con mejores constantes.


El resultado seleccionado puede emplear `baseline`, `subweyl` o
`pruned_subweyl` como perfil de borde. `FINAL_RESULT.json` fija explícitamente
los verificadores PL, de costes y de envolvente. La reproducción lee esa
selección y repite la cadena correspondiente. El último perfil utiliza la
entrada sub-Weyl de Patel--Yang y una selección de nodos de Yang; su deducción
y las comprobaciones compactas están documentadas en `GEOMETRY.md`.


El campo `certified: false` del fichero de coeficientes registra su procedencia
como salida de búsqueda. Se conserva sin editar para mantener su hash exacto.
La aceptación matemática se declara en los certificados independientes y en
`FINAL_RESULT.json`; modificar aquel campo después de verificar invalidaría
los enlaces de integridad.


La entrega solicitada se fija en **C=2.959227629** y en `CERTIFICADO.md`.
La búsqueda se detuvo expresamente por indicación del autor; los ensayos
incompletos posteriores se conservan como historial y no se anuncian como
mejoras demostradas. Para continuar una familia desde un resultado congelado,
`geometry_continuation.py` lee d, m y el perfil de su envolvente; admite
`--maxit` para controlar los refinamientos numéricos antes de certificar.
