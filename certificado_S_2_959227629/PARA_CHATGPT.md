# Traspaso a ChatGPT: certificado uniforme de S(T), C = 2.959227629

Documento preparado el 7 de noviembre de 2026. Resume la entrega y sus límites;
las fuentes primarias de esta ejecución son los archivos y registros enlazados.

## Estado y encargo vigente

El autor pidió detener la optimización por ahora, entregar el certificado ZIP y
subirlo a GitHub en una subcarpeta de PaperMath. **La investigación está detenida
por petición del autor, no por agotamiento matemático.** No reanudar búsquedas
ni lanzar cálculos costosos salvo nueva petición explícita.

## Resultado entregado

$$

\boxed{|S(T)|\le 0.08382\log T+2.959227629,\qquad T>1.}

$$

La cadena entregada certifica la cota sin asumir RH y cubre todas las alturas
T>1. En ordenadas de ceros incluye la convención continua por la derecha,
el límite izquierdo y el valor medio, según el certificado de envolvente.
**2.959 es una abreviatura informal: no sustituir la constante demostrada por
2.959000000 ni por 2.595.**

| Cantidad | Valor | Alcance |
|---|---:|---|
| Referencia anterior | 4.40577136 | Indicada por el autor; no se localizó su paquete original |
| Mejor cota superior entregada | 2.959227629 | Uniforme, certificada y reproducida |
| Cota inferior universal demostrada en esta ejecución | 0.688655186978719794671238 | Necesaria para cualquier desigualdad uniforme de esta pendiente; no determina el óptimo |

No se ha probado optimalidad global. Las cotas duales 3.28065... y 3.06766...
corresponden a familias fijas anteriores sin geometría; **no** son cotas
inferiores para la familia ampliada con discos y rectángulos.

## GitHub y descarga

- Repositorio: https://github.com/vcasana1/PaperMath
- Subcarpeta de entrega: https://github.com/vcasana1/PaperMath/tree/codex/optimize-uniform-S-constant/certificado_S_2_959227629
- ZIP: https://github.com/vcasana1/PaperMath/blob/codex/optimize-uniform-S-constant/certificado_S_2_959227629/certificado_S_2_959227629.zip?raw=true
- SHA-256: a157aafd247a49dd6e8c002762dce6d66fd4500838c8e16d1456f14d0479b131
- Tamaño del ZIP original: 23226651 bytes.
- Rama independiente: `codex/optimize-uniform-S-constant`.
- Commit científico que fija los datos y verificadores: `f127d3e3948ba1e87e7d4798f8b56cce25d1995f`.
- Fuentes completas de ese commit: https://github.com/vcasana1/PaperMath/tree/f127d3e3948ba1e87e7d4798f8b56cce25d1995f/numerics/explicit_S_turing/optimization_C

La subcarpeta añade este traspaso y una copia idéntica del ZIP ya entregado.
El ZIP conserva su SHA-256 original; el Markdown se entrega aparte.

## Rutas locales del Mac

- Repositorio: `/Users/vcasana/Documents/ChatGPT/Möbius/PaperMath_optimization_C`.
- Directorio de trabajo del certificado: `/Users/vcasana/Documents/ChatGPT/Möbius/PaperMath_optimization_C/numerics/explicit_S_turing/optimization_C`.
- ZIP original: `/Users/vcasana/Documents/ChatGPT/Möbius/certificado_S_2_959227629.zip`.
- Subcarpeta para GitHub: `/Users/vcasana/Documents/ChatGPT/Möbius/PaperMath_optimization_C/certificado_S_2_959227629`.
- Binario de primos del autor: `/Users/vcasana/Documents/·.· MATLAB/·.· bin_unicos/primoss.bin`.

Si ChatGPT no dispone de acceso al Mac, debe leer el ZIP o las fuentes públicas;
no debe afirmar que ha ejecutado programas locales sin haberlo hecho.
Los cálculos realizados en esta ejecución se ejecutaron en el Mac, no en la nube.

## Datos exactos seleccionados

El directorio base dentro del ZIP es `numerics/explicit_S_turing/optimization_C/`.
Todas las rutas siguientes son relativas a ese directorio:

- `certificates/FINAL_RESULT.json`: índice del resultado seleccionado.
- `certificates/final_geometry_C2_959227629/solution.json`: coeficientes y geometrías exactos.
- `certificates/final_geometry_C2_959227629/solution_geometry_kernel.json`: prueba global del mayorante geométrico.
- `certificates/final_geometry_C2_959227629/solution_arithmetic.json`: cota aritmética, incluidas las colas infinitas.
- `certificates/final_geometry_C2_959227629/solution_geometry_costs.json`: integrales armónicas certificadas.
- `certificates/final_geometry_C2_959227629/PL_inputs.json`: condiciones compactas de los datos verticales.
- `certificates/final_geometry_C2_959227629/solution_joint_geometry_envelope.json`: cobertura uniforme y transición.
- `certificates/universal_lower_zeros.json`: cota inferior universal.
- `certificates/reproduction_status.json`: reproducción completa ejecutada.
- `certificates/proof_chain_status.json`: comprobación de enlaces y hashes.
- `CERTIFICADO.md`, `GEOMETRY.md`, `INFORME_MATEMATICO.md`: lectura científica.
- `COMPARACION.md`: historial y alcance de los resultados.

Parámetros: d=1.1, m=60, 119 coeficientes racionales,
16 rectángulos y 7 discos, con pesos no negativos.
Perfil de borde: `pruned_subweyl`. Los centros se acoplan a las mismas
fases primas del núcleo.

La pendiente total se certificó <= 0.08352880955664759899676537.
El término de log log T se absorbe usando la holgura respecto de 0.08382 y un
máximo analítico en log T. La transición está en log T=93.077380; el núcleo
inferior cubre desde T=1 y la rama alta se controla hasta infinito.

## Procedencia y estructura de la prueba

- [ADAPT] Se parte de las identidades y núcleos de v11. Su copia de referencia
  está en `inputs/reference_v11_local.tex`; los originales no se modificaron.
- [ADAPT/DED] Se amplía el mayorante con pesos de Green de discos y rectángulos.
  Se certifican todas las interfaces de las celdas armónicas en racionales
  exactos y ambas colas verticales mediante todas las raíces críticas.
- [DED] Los términos de los centros de Jensen se incorporan a las mismas fases
  primas del núcleo mediante la serie de Euler absolutamente convergente.
- [LIT/ADAPT] Los datos verticales y la interpolación se documentan con sus
  fuentes y dominios en `GEOMETRY.md`. El perfil elegido usa la entrada sub-Weyl
  de Patel–Yang y los nodos k=4,5,6,7 de Yang, omitiendo k=8,9.
- La búsqueda con CVXPY es numérica. Los verificadores independientes usan Arb
  mediante python-flint; una malla favorable no se acepta como demostración.

No se reivindica novedad bibliográfica de las construcciones. Este traspaso
no es una auditoría matemática nueva: remite a las pruebas y registros entregados.

## Primos y orden del núcleo: qué se hizo realmente

El archivo `primoss.bin` se validó por igualdad exacta con una criba segmentada
completa hasta 10^10. Contiene 455052511 enteros uint64 little-endian, de
2 a 9999999967; SHA-256 `79b99094b72787de8c53b3b3a068956587747ef8eec5cba222ca004b95fc5272`. Se preservó sin modificarlo.
Las búsquedas utilizaron la agregación positiva de todos esos primos.

El certificado seleccionado suma directamente hasta N=100000000 y acopla las
potencias de los primos hasta P0=10000; **P0 no es el número total de primos**.
La cola restante hasta infinito está acotada rigurosamente. El ZIP no duplica el
binario de 3.64 GB: los verificadores regeneran los primos independientemente.
Un checkpoint anterior se contrastó directamente con los 455052511 primos
hasta 10^10 y se reprodujo con C=2.963951287. No confundir ese checkpoint con
el certificado seleccionado, cuyo C es menor.

Se probaron órdenes superiores. El ensayo de orden 1000 liberó 269 parámetros
seleccionados; **no** se optimizaron los 1999 coeficientes de la familia completa.
Sus resultados numéricos no constituyen una exclusión del orden 1000.

## Verificación ejecutada y cómo reproducir

La reproducción completa seleccionada terminó en `reproduction_geometry/20261106_205118` con
C_reproduced=C_claimed=2.959227629. Superó estas etapas:

1. Núcleo inferior de cobertura.
2. Aritmética inferior.
3. Parte elemental inferior completa.
4. Condiciones compactas PL.
5. Núcleo geométrico global e infinito.
6. Costes armónicos.
7. Aritmética superior con fases conjuntas y cola infinita.
8. Envolvente uniforme.
9. Cota inferior universal.

En una extracción del ZIP, desde su directorio base:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/verify_manifest.py
.venv/bin/python src/reproduce.py
.venv/bin/python src/verify_chain.py
```

Comprobar el manifiesto **antes** de reproducir: la reproducción crea registros
y actualiza su estado. Las versiones medidas figuran en
`certificates/environment.json`; se usó Python 3.14.5, python-flint 0.9.0 y
FLINT 3.6.0 en macOS arm64. No reemplazar los coeficientes por los de tablas
redondeadas. El campo `certified: false` del archivo de coeficientes conserva
su procedencia numérica: la aceptación está en los certificados independientes;
no editar ese campo ni otros bytes después de verificar sus hashes.

## Ensayos interrumpidos: no son cotas demostradas

El autor detuvo los siguientes ensayos antes de su certificación completa:

- `candidates/geometry_m60_d1p1_joint_neighbors12.json`.
- `candidates/geometry_joint_m60_round11_union.json`.
- `candidates/geometry_joint_m80_round11_union.json`.

El mejor objetivo numérico registrado fue aproximadamente 2.958331428916,
en el último archivo, de orden 80. Su residual escalado numérico era negativo
(aproximadamente -4.01419e-5); **no** se anuncia 2.9583 como cota uniforme.
La referencia detallada es `certificates/unproved_candidate_summary.json`.
No confundir salidas de búsqueda, reparaciones numéricas, pruebas parciales y
certificados completos.

## Preferencias y continuidad, solo si se solicita

El autor pidió usar el Mac y continuar mientras las mejoras afectasen a la
cuarta cifra decimal o antes y el cálculo siguiera siendo razonablemente rápido.
Posteriormente pidió detenerse. La parada se conserva en
`certificates/geometry_stop_decision.json`; no es una prueba de agotamiento.

Si solicita reanudar, conservar el certificado 2.959227629 intacto y trabajar
con nuevos archivos. Leer antes `GEOMETRY.md`, `FINAL_RESULT.json` y los
registros de los ensayos pendientes. Para una familia fija, separar la mejor
cota superior certificada de cualquier óptimo numérico o cota dual de otra
familia. No modificar v11, los manuscritos originales ni los certificados
históricos. No asumir RH ni transferir resultados de relojes sintéticos a los
ceros verdaderos de zeta.

## Instrucción de lectura para un nuevo chat

Lee este traspaso y los índices del certificado. Confirma qué archivos puedes
consultar y distingue lo reproducido de lo que solo has leído. Explica el
resultado entregado sin atribuir optimalidad global. Si se pide una auditoría,
comprueba las fórmulas y dominios antes de aceptarlos; si se pide continuación,
reanuda únicamente dentro del alcance autorizado y conserva los resultados
anteriores.
