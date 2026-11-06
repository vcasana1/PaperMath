# Certificado de S(T): 2.959227629

Se certifica, incondicionalmente y sin asumir RH,

\[|S(T)|\le 0.08382\log T+2.959227629,\qquad T>1.\]

La cota cubre también las ordenadas de ceros con las convenciones indicadas
en el certificado. No se afirma optimalidad global.

El resultado seleccionado es `certificates/FINAL_RESULT.json`. Sus coeficientes
exactos y pruebas están en `certificates/final_geometry_C2_959227629/`.
Se usa d=1.1, orden 60, 119 coeficientes, 16 rectángulos y 7 discos.
La aritmética suma directamente hasta 10^8 y certifica la cola infinita.
Las búsquedas utilizaron la agregación completa de los 455052511 primos del
binario del autor; se conserva además un contraste directo hasta 10^10 para
el checkpoint anterior. El binario de 3.64 GB no es necesario para reproducir
la prueba: los verificadores generan los primos independientemente.

## Reproducción

Desde el directorio `numerics/explicit_S_turing/optimization_C` del ZIP extraído:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python src/verify_manifest.py
.venv/bin/python src/reproduce.py
.venv/bin/python src/verify_chain.py
```

Compruebe el manifiesto antes de reproducir: la reproducción crea registros y
actualiza su estado. Las versiones utilizadas están en `requirements.txt` y
`certificates/environment.json`. Los registros de la reproducción de entrega
se identifican en `certificates/reproduction_status.json`.

`GEOMETRY.md` contiene la deducción matemática de la ampliación geométrica y
del acoplamiento de centros. `INFORME_MATEMATICO.md` distingue pruebas,
exploraciones y cotas inferiores. `COMPARACION.md` conserva los resultados.

La investigación se detuvo por solicitud del autor. Se incluyen los ensayos
posteriores incompletos como historial; no aportan constantes certificadas.
