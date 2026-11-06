"""Insert the selected proved numbers and measured stopping evidence."""
import json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];path=BASE/'INFORME_MATEMATICO.md';marker='<!-- FINAL_RESULTS -->'
head=path.read_text().split(marker)[0].rstrip();f=json.loads((BASE/'certificates/FINAL_RESULT.json').read_text())
part='\n\n'+marker+'\n\n## Resultado seleccionado y alcance\n\n'+(BASE/'FINAL_NUMBERS.md').read_text().replace('# Números finales demostrados','### Valores finales')
part+='\n### Verificación ejecutada\n\n'
p=BASE/'certificates/reproduction_status.json'
if p.exists():
    r=json.loads(p.read_text());part+=f"La reproducción completa terminó con C={r['C_reproduced']}. Etapas superadas: {', '.join(r['checks'])}. Registro: `{r['output']}`.\n"
part+='\n### Criterio de cierre indicado por el autor\n\n'
part+='Se priorizan mejoras de 0.0001 o mayores mientras el cálculo siga siendo rápido en el Mac. Se dejan de perseguir mejoras limitadas a la quinta cifra decimal o posteriores, y se evita extender cálculos cuyo coste resulte excesivo. Esto sustituye un criterio de agotamiento absoluto, que no se ha demostrado.\n\n'
part+='La suma ya se extendió de 455052511 primos hasta 10^10 a 4118054813 primos hasta 10^11 para un núcleo de orden 100. El beneficio de ese aumento fue de unas pocas centésimas de millonésima, muy por debajo del nuevo umbral. `ARITHMETIC_BUDGET.md` conserva los tiempos y los términos de error. No se confunde el corte P0 de fases conjuntas con el número total de primos incluidos.\n\n'
part+='El binario del autor fue validado por igualdad exacta con la criba completa (42.2 s en esta ejecución), sin modificarlo. Los ensayos nuevos agregan todos sus 455052511 primos. Las agregaciones y cuadraturas son herramientas numéricas de búsqueda; la prueba aritmética sigue siendo independiente.\n\n'
p=BASE/'certificates/extension_numerical_recheck.json'
if p.exists():
    rows=json.loads(p.read_text());part+='### Órdenes superiores: reevaluación numérica separada\n\n| Archivo | Orden | Nodos de Gauss por panel | Objetivo numérico |\n|---|---:|---:|---:|\n'
    for r in rows:part+=f"| {Path(r['candidate']).name} | {r['m']} | {r['gauss_nodes']} | {r['C_numerical']:.12f} |\n"
    part+='\nEstos números son evaluaciones numéricas de un objetivo aproximante, no cotas uniformes certificadas. La comparación se hace con los mismos datos y una cuadratura más densa en sqrt(log x). No se sustituyen por ellos los valores probados anteriores. El ensayo de orden 1000 libera 269 parámetros seleccionados, frente a los 1999 de la familia completa; no se afirma optimalidad en esa familia.\n'
    part+='\nEl ensayo corregido de orden 1000 (`d100_m1000_sparse_resolved.json`) terminó en 272.6 s. Su objetivo reevaluado no mejora al del núcleo vigente. No se inició una certificación aritmética costosa de ese candidato. El núcleo de orden 200 sí superó la prueba global de (K), aislando las 803 raíces de su polinomio derivado en 45.1 s, pero su reevaluación aritmética numérica tampoco ofreció la mejora requerida; no se publica una nueva constante a partir de él. Estos resultados explican el cierre práctico, sin excluir una mejora futura con otros parámetros ni con los 1999 coeficientes libres.\n'
part+='\n### Restricciones próximas al contacto\n\n'
p=BASE/'certificates/active_constraints.json'
if p.exists():
    a=json.loads(p.read_text());part+=f"Para el núcleo seleccionado, A está entre {a['leading_slope_lower']} y {a['leading_slope_upper']}; la holgura inferior del límite de t²(U-f) es {a['tail_limit_lower']}. Los veinte puntos críticos más próximos al contacto y sus holguras dirigidas figuran en `certificates/active_constraints.json`. Son holguras certificadas, no una prueba dual de optimalidad.\n"
part+='\nLa brecha global sigue siendo amplia. Las dos familias de un solo núcleo con dual certificado figuran en `certificates/fixed_family_gap_d095_m10.json` y `certificates/fixed_family_gap_d1006257_m10.json`; sus cotas inferiores no se trasladan a la unión de todas las envolventes. Para las demás familias no se ha obtenido un dual específico; sí les aplica la cota inferior universal.\n'
path.write_text(head+part)
print('report updated',f['C_new'])
