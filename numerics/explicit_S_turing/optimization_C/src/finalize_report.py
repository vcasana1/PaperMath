"""Assemble the current proved result, distinguishing earlier restricted trials."""
import json,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];path=BASE/'INFORME_MATEMATICO.md';marker='<!-- FINAL_RESULTS -->';f=json.loads((BASE/'certificates/FINAL_RESULT.json').read_text())
head=path.read_text().split(marker)[0].rstrip()
start='<!-- CURRENT_RESULT -->';end='<!-- END_CURRENT_RESULT -->'
if start in head:head=head[:head.index(start)]+head[head.index(end)+len(end):]
intro=f'''\n{start}\n
**Resultado actual:** para todo T>1, |S(T)| <= 0.08382 log T + **{f['C_new']}**.
La prueba seleccionada usa un núcleo d={f['d']}, de orden {f['m']}, {f['coefficients']} coeficientes
racionales, {f['rectangles']} rectángulos y {f.get('circles',0)} discos, con los centros acoplados exactamente
a las fases primas. No supone RH. La deducción completa de esta ampliación
está en `GEOMETRY.md`; los coeficientes y certificados seleccionados están en
`{f['solution']}` y `certificates/FINAL_RESULT.json`.

Los apartados siguientes conservan el desarrollo anterior de la familia sin
geometría y su auditoría. Las afirmaciones de familia fija se refieren a esa
familia. Los resultados finales y el alcance de los ensayos ampliados se
recogen después del marcador FINAL_RESULTS y en `FINAL_NUMBERS.md`.
{end}\n'''
first=head.index('\n');head=head[:first]+intro+head[first:]
part='\n\n'+marker+'\n\n## Resultado seleccionado y alcance\n\n'+(BASE/'FINAL_NUMBERS.md').read_text().replace('# Números finales demostrados','### Valores finales')
reproductions=[json.loads(q.read_text()) for q in (BASE/'certificates').glob('reproduction_geometry_C*.json')]
r=min((x for x in reproductions if x.get('complete')),key=lambda x:float(x['C_reproduced'])) if reproductions else json.loads((BASE/'certificates/reproduction_status.json').read_text())
reproduction_matches=(r['C_reproduced']==f['C_new'] and hashlib.sha256((BASE/r['output']/'high.json').read_bytes()).hexdigest()==hashlib.sha256((BASE/f['solution']).read_bytes()).hexdigest())
part+=f"\n### Reproducción independiente ejecutada\n\nLa reproducción completa terminó con C={r['C_reproduced']}. Etapas: {', '.join(r['checks'])}. Registro: `{r['output']}`. `verify_chain.py` comprueba además los hashes de los coeficientes y los certificadores enlazados. La búsqueda numérica no se importa como prueba.\n"
part+='''
### Geometrías y criterio práctico de cierre

Se buscaron inicialmente 168 discos y 840 rectángulos. Después se reoptimizaron
coeficientes y pesos con las fases exactas de los centros, variando centros,
abscisas, anchuras, semialturas y desplazamientos de las formas activas.
`COMPARACION.md`, `certificates/geometry_search_history.json` y los registros
conservan las mejoras certificadas y los candidatos que no superaron la prueba.
No se declara un óptimo entre todos los discos o rectángulos posibles.

Se aplica el criterio del autor: perseguir ganancias de 0.0001 o mayores
mientras el cálculo local siga siendo rápido; detener refinamientos que solo
afectan a la quinta cifra decimal o que resultan excesivamente costosos.
El estado final de esta exploración se documenta en
`certificates/geometry_stop_decision.json`. Es un cierre práctico, no una
prueba de agotamiento matemático.

### Uso del archivo de primos y órdenes grandes

El binario del autor contiene 455052511 enteros uint64 little-endian y se
validó por igualdad exacta con la criba completa hasta 10^10 (42.2 s).
Las búsquedas nuevas usan su agregación positiva completa. Los certificadores
regeneran los primos independientemente y acotan la cola infinita: ni el
binario ni la cuadratura de búsqueda se presuponen correctos en la prueba.

En la familia anterior sin geometría se llegó además a 4118054813 primos
hasta 10^11. Ese aumento tardó unos 2569 s y mejoró C solo en unos 2.5·10^-8.
No se repite esa extensión para ganar cifras que el autor pidió no perseguir.
No se confunde P0, que controla las fases conjuntas, con el corte total N.
`ARITHMETIC_BUDGET.md` compara únicamente funciones aritméticas idénticas.

Se ejecutó un ensayo de orden 200 con 399 parámetros y otro de orden 1000
con 269 parámetros seleccionados. La reevaluación densa no mejoró el objetivo
comparable del núcleo anterior. El ensayo de orden 1000 no libera los 1999
coeficientes de la familia completa: no constituye una exclusión de esa familia.
La primera cuadratura insuficiente y sus aparentes mejoras se rechazaron;
se preservan como historial identificado, no como resultados certificados.

### Holguras y cotas inferiores

`certificates/active_geometry_constraints.json` recoge las holguras intervalares
más pequeñas en las interfaces, las colas completas, los pesos y la holgura de
pendiente. Son datos certificados de factibilidad, no un dual de optimalidad.

La cota inferior universal 0.688655186978719794671238 procede de un punto
racional verificado con Arb y es válida también para esta construcción.
Las cotas duales 3.28065... y 3.06766... pertenecen a familias fijas anteriores
sin rectángulos y **no** se trasladan a la familia ampliada. La brecha global
sigue abierta; no se afirma que el mejor valor encontrado sea el mínimo.
'''
u=BASE/'certificates/unproved_candidate_summary.json'
if u.exists():
    best=json.loads(u.read_text()).get('best')
    if best:part+=f"\n### Candidato numérico separado\n\nEl menor objetivo numérico registrado es {best['C_numerical']:.12f}, en `{best['candidate']}`. Su residual mínimo numérico escalado es {best['minimum_scaled_residual_numerical']}; su error de fases detectado, {best['phase_gap_numerical']}. No se anuncia ese valor como cota uniforme. Los coeficientes de entrada reparados y aceptados se identifican exclusivamente mediante FINAL_RESULT y la cadena independiente.\n"
if not reproduction_matches:part+=f"\nLa reproducción completa anterior corresponde a un checkpoint. La cota seleccionada {f['C_new']} ya tiene sus componentes independientes certificados; su nueva reproducción completa sigue pendiente.\n"
if not (BASE/'certificates/geometry_stop_decision.json').exists():part=part.replace('El estado final de esta exploración se documenta en\n`certificates/geometry_stop_decision.json`. Es un cierre práctico, no una\nprueba de agotamiento matemático.','La exploración sigue en curso; todavía no se declara un cierre práctico ni un agotamiento matemático.')
part+='\nEl resultado nuevo implica también la desigualdad con constante 4.40577136; esto no constituye una auditoría del paquete original que no fue localizado.\n'
stop_path=BASE/'certificates/geometry_stop_decision.json'
if stop_path.exists() and json.loads(stop_path.read_text()).get('status')=='stopped_by_user':part+='\n### Cierre solicitado por el autor\n\nLa investigación se detuvo por solicitud expresa del autor. No se ha agotado la búsqueda ni se han certificado los candidatos posteriores. La entrega se fija en C=2.959227629; la verificación adicional se limita a reproducir ese certificado y comprobar su integridad.\n'
path.write_text(head+part);print('report updated',f['C_new'])
