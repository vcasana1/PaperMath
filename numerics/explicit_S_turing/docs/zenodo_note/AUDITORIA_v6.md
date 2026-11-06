# Auditoría de incorporación — v6, 7 noviembre 2026

## Resultado y alcance

La v6 incorpora, como teorema independiente, la cota incondicional
|S(T)| <= 0.08382 log T + 2.959227629 para todo T>1.
No se ha probado optimalidad global. No se ha modificado el
enunciado independiente de seis rectas para N(T) y S(T).

El certificado nuevo usa dos regiones, NO seis rectas:
la primera corresponde a d=1, m=5, nueve coeficientes,
hasta log T=93.077380; la segunda corresponde a d=1.1,
m=60, 119 coeficientes, 16 rectángulos y 7 discos.
El término positivo B log log T de la segunda región
se absorbe con la holgura en la pendiente 0.08382-A.

## Preservación literal comprobada

Se han comparado con la v5 las secciones:
The identity of Turing type;
The explicit estimate;
Jensen discs and admissible profiles;
The asymptotic estimate;
y los apéndices Data tables, Programs, Outputs of the
certification programs y Exact data.

Estos bloques están conservados íntegramente y sin
cambios. Tres diferencias heredadas en el punto de
partida de la rama (una condición de dominio, una nota
del perfil y una anotación de datos) fueron restauradas
desde la v5 para no introducir modificaciones ajenas.

## Revisiones del resultado nuevo

- Convención de S(T): derecha en las ordenadas; se
  cubren asimismo los límites izquierdo y su promedio.
- Se considera rho=beta+i gamma sin suponer RH.
- El peso se aplica a los ceros reflejados y se
  conserva el factor 2 en el coste de Green-Jensen.
- Los términos de centro se expresan por Euler para c>1
  y se juntan con las fases T log p del núcleo.
- La cota externa Patel--Yang 66.7 t^(27/164)
  está publicada para t>=3 en Journal of Number
  Theory 262 (2024), pp. 301-334.
- La documentación de Codex declara certificación de
  las desigualdades de núcleo, interfaces, colas,
  costes armónicos, interpolación compacta y alturas.
- Datos de envolvente: rama inferior
  < 2.959218418359088442; superior
  < 2.959227628288475263.
  Ambas son menores que 2.959227629.
- Pendiente efectiva total: A <
  0.083528809556647599.
  Coeficiente loglog: B < 0.064611026099352525.

## Trazabilidad

Certificado: PaperMath, rama
codex/optimize-uniform-S-constant, subcarpeta
certificado_S_2_959227629.
Commit científico: f127d3e3948ba1e87e7d4798f8b56cce25d1995f.
SHA256 ZIP: a157aafd247a49dd6e8c002762dce6d66fd4500838c8e16d1456f14d0479b131.

Se consultaron FINAL_RESULT.json, los estados de
reproducción e integridad, las salidas de geometría,
aritmética y envolvente, y la deducción de GEOMETRY.md.
Esta revisión de integración no es una reejecución
independiente de todos los verificadores en otra máquina,
ni una formalización de las pruebas y del código.
No puede garantizar la ausencia de objeciones futuras.

## Estado de entrega

La v6 se entrega en TeX y TXT con idéntico contenido.
No se ha realizado aquí una compilación real a PDF.
Antes de publicación corresponde compilar y revisar
hipervínculos, saltos de línea, TOC y avisos LaTeX.
