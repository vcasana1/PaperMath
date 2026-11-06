# Incidencias conservadas

Los resultados utilizables son los seleccionados en `certificates/FINAL_RESULT.json`.
Un log de desarrollo que termina en error o sin frase de certificación completa
no es un certificado.

- La primera formulación cónica tenía escalas extremas; Clarabel devolvió un
  error numérico. Se ponderaron las filas dentro de las normas y se cambió de
  base.
- La primera implementación aritmética omitía un factor 1/pi. Sus salidas se
  rechazaron; la salida identificada se conserva separada en
  `development_rejected/`. Todas las cotas aceptadas usan la normalización
  correcta y certificación posterior.
- Las potencias genéricas de ciertos intervalos Arb con ambos signos devolvían
  `nan`; los programas abortaron. Se sustituyeron por multiplicaciones o
  potencias enteras adecuadas.
- La reducción excesiva del margen de (K) produjo un candidato con una
  violación entre puntos de malla. Se refinan ahora los mínimos continuos y se
  verifica globalmente con aislamiento exacto de puntos críticos.
- La forma de f regular en t=0 pierde precisión en coma flotante para t enorme.
  La búsqueda usa la forma directa allí. Los certificados siempre usan Arb.
- El extremo fijo de la cola aritmética era válido pero demasiado holgado para
  algunos órdenes altos. Ahora se elige adaptativamente.
- Varias subdivisiones intervalares duplicadas de orden 100 se interrumpieron
  al disponer de la prueba global por raíces del numerador exacto de la
  derivada. Los registros parciales se mantienen como evidencia del coste.
- El sumador por momentos se contrastó con la suma directa antes de aumentar
  el corte. Las potencias adicionales de primos pequeños se descuentan de la
  cola, evitando doble contabilidad.

No se modificaron los certificados originales ni el manuscrito v11. La búsqueda
del paquete 4.40577136 no encontró coincidencias en las rutas accesibles; se
conservan también los errores de acceso de esa búsqueda.
