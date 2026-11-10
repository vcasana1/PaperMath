# CONTINUACIÓN DE TRABAJO — CASTOR–POLLUX I (estado tras la v3)

**Fecha:** 10 de noviembre de 2026. Sustituye a `CONTINUACION_CASTOR_POLLUX_v2.md`.

## 1. Versiones

| Versión | SHA-256 del `.tex` | Líneas | Páginas |
|---|---|---|---|
| v1 | `3bc78229172e068d3f4b5403e7ff808c565b7f6baa8694b8da2f4774f5f7556a` | 2 051 | 22 |
| v2 | `ecfae630f67a726a50bf3065d86cf5fe6a2047860738a113111a52e5b1f464b8` | 2 056 | 22 |
| **v3 (vigente)** | `1465a2c038a3e88ba45c4ea62c11ee4a1e3cc567ce9d75b45ad82c8f1d487f87` | 2 140 | 25 |

Cada versión sale de la anterior con un script de sustituciones exactas (`make_v2_from_v1.py`, `make_v3_from_v2.py`); los diff están en el paquete. El bloque `CorrectVCG` embebido (v10) es idéntico en las tres.

Comprobador sobre la v3: 0 errores, 1 advertencia (`lem:T`, por patrón). Compilación: 0 errores, 0 avisos, 0 referencias sin resolver, 12 figuras.

## 2. Qué añade la v2 (resumen)

Certificado por aritmética de bolas de los seis discos de Rouché (`castor_pollux_I_rouche_certificate_v1.py`), y las correcciones de la revisión: `G/A` solo donde `A≠0`, arcos como observación numérica, «Eight figures», alcance de las técnicas, `i` reservada a la unidad imaginaria (índice entero `b`), tabla `tab:check` como comprobación numérica, signo de `r'` en `lem:T`, tooltips `int_`.

## 3. Qué añade la v3

1. **Proposición 14.1 (`prop:A`), demostrada:** `A` se prolonga a función meromorfa con `A(s) = log(2π)/s + 1/s² + Σ_k Σ_{2k}/(k(2k−s))`; para `Re s < 0`, `A(s) = −∫_0^1 h(u) u^{−s−1} du = (s+1)(s+2) H̃(s)/(4π²)` con `H̃(s) = ∫_0^1 𝒦(u) u^{−s−3} du`; en el eje real, ceros simples en `−2` y `−1`, `A > 0` en `(−1,0)` y `(0,2)`, y al menos un cero en cada `(2l, 2l+2)`. Lleva marca `\VCGreviewed{1}`.
2. **Superficies con malla fina:** `−log₁₀` del módulo de `G`, `A`, `G−A` y `ζ` en `0.05 ≤ Re s ≤ 1.95`, `1 ≤ Im s ≤ 40`, malla `253×889` refinada alrededor de los ceros; un cero es un pico, recortado en 6. Superficie nueva de `A` cerca del eje real (`fig:Areal`), con sus ceros reales como picos y sus polos como hoyos. Orientación normal: el pico va hacia arriba.
3. **Sumas exponenciales** `𝓔_G(x) = (1/79) Σ e^{ix Im z}` sobre los 79 ceros de `G` y `𝓔_A(x) = (1/101) Σ e^{ixz}` sobre los 101 ceros reales de `A`: tres figuras y su descripción. **En el 3D la variable `x` va en el eje vertical** (orden expresa de Doktor para todas las sumas exponenciales; no aplicarlo a las superficies).
4. Números nuevos del texto: relación de malla `|G − A − (π/s)cot(πs/2)ζ| ≤ 1.2·10⁻¹¹`; `|G − A| ≤ 1.1·10⁻¹¹` en los seis puntos `½+it`; `|G|` entre `4.1·10⁻¹²` y `2.8·10⁻¹¹` en los seis ceros de `G`.

Las listas de ceros (`zeros_G.txt`, `zeros_A.txt`) vienen del chat «Demostración de RH desde el md y tex» (rama `castor-pollux-zeros` de `vcasana1/papermath`) y se dan por buenas por orden de Doktor.

## 4. Abierto

- `A ≠ 0` fuera del eje real: solo calculado (recuento por principio del argumento del otro chat), no demostrado. «Exactamente un cero en cada `(2l, 2l+2)`»: demostrado «al menos uno»; «exactamente uno» solo calculado para `l ≤ 99`.
- Choque de `a` (`j∨k`, exponente de `p^a`, números `a_b`), sin corregir.
- Momentos de la línea 557 en doble precisión; tabla `tab:check` sin cota de cuadratura ni de cola.
- Los 73 ceros de `G` con `Im s > 40` no tienen certificado de Rouché; solo los seis de la tabla.

## 5. Protocolo

Comprobar el SHA-256 de la v3 antes de reutilizar este estado. Cada versión nueva lleva número nuevo y su `.txt`. No cambiar nada que no se pida.
