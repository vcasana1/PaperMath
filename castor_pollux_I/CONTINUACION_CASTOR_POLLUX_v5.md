# CONTINUACIÓN DE TRABAJO — CASTOR–POLLUX I (estado tras la v5)

**Fecha:** 11 de noviembre de 2026. Sustituye a `CONTINUACION_CASTOR_POLLUX_v4.md`.

## 1. Versiones

| Versión | SHA-256 del `.tex` | Líneas | Páginas |
|---|---|---|---|
| v1 | `3bc78229172e068d3f4b5403e7ff808c565b7f6baa8694b8da2f4774f5f7556a` | 2 051 | 22 |
| v2 | `ecfae630f67a726a50bf3065d86cf5fe6a2047860738a113111a52e5b1f464b8` | 2 056 | 22 |
| v3 | `1465a2c038a3e88ba45c4ea62c11ee4a1e3cc567ce9d75b45ad82c8f1d487f87` | 2 140 | 25 |
| v4 | `316d748bc6a20492926b6da33874194a17a1647ae5c5c86a8c2e0a97294fac13` | 2 140 | 28 |
| **v5 (vigente)** | `39d73e583d5e5fb016f6ea76bfa15a197f2a80359a9996457ba55d9f07ff5ea7` | 2 493 | 37 |

La v5 sale de la v4 con `make_v5_from_v4.py` (14 sustituciones exactas) y el texto nuevo de `v5_new_sections.tex`. Comprobador (v10 embebido): 0 errores, 5 advertencias por patrón (`lem:T`, `prop:Omegadecay`, `prop:Ksharp`, `cor:RH`), diff contra la v4 limpio con `allowed_labels_v5.txt`. Compilación: 0 referencias sin resolver, 0 cajas desbordadas, 12 figuras (las mismas de la v4, sin tocar).

## 2. Qué añade la v5

1. **§15 (sin zeta).** `ℓ(u)=log(πu/|sin πu|)>0`, `G−A = −∫_0^∞ ℓ u^{−s−1}` en `0<σ<2`; `|G−A| ≤ A(σ)−G(σ)`, igualdad solo en `t=0` (Prop. 15.1). Forma de tres términos `G−A = (ψ(1−s/2)−ψ(1+s))/s − Q(s) − Q_0(s)` con `Q` de la Prop. 7.1 y `q_0(u)=log(πu(1−u²)/sin πu)=Σ(Σ_{2k}−1)u^{2k}/k` (Prop. 15.2). **Teorema 15.4, analítico:** `Re(sA(s)) ≤ 𝒬(t) < 0` para `0≤σ≤1`, `|t|≥9` (`𝒬(9)<−0.045`; usa `Σ_2−1>0.64` sin π²/6). Observación 15.5: certificado en bolas `A_nonvanishing_check.py` en `[0,1]×[0,102]`, marcado como asistido por ordenador; nada depende de él.
2. **§16 (sin zeta).** `𝔟=log(2π)−3/2`, `ℬ(u)=4π²∫_0^u(u−λ)ℓ(λ)dλ = 𝒦(u)+2π²u²(log u+𝔟)`, convexo, C¹, serie de coeficientes positivos en `(0,1)`, `0<ℬ<2π²𝔟u⁴`; `G−A = −(s+1)(s+2)Ω(s)/(4π²)` (Prop. 16.1). Desigualdad de inversión `ℬ(u)>u^{2σ+4}ℬ(1/u)` (`u>1`, `0<σ≤1`), pesos `υ^±_σ` positivos, Ω decreciente en `(0,1]` (Prop. 16.2). Región sin soluciones `t²(𝓜_0𝓜_2−𝓜_1²)<2𝓜_0²` (Thm. 16.3). `|Ω| ≤ ‖υ''‖₁/t²` (Prop. 16.4). Núcleo de dos armónicos `𝒦^♯` con `G^♯=A^♯` en `3/4+i(2k+1)π/log 2` (Prop. 16.5). Procede del adjunto d6262b95 (núcleo B), con nombres cambiados para no chocar: β→𝔟, W/B→ℬ, F→Ω, a_σ,b_σ→υ^±_σ, M_j→𝓜_j, x→v.
3. **§17 (con zeta, fuentes verificadas en LIBRARY TOTAL).** `G−A = (π/s)cot(πs/2)ζ(s)` (Prop. 17.1); la condición «toda solución no real de G=A tiene parte real ½» ⇔ RH (Cor. 17.2). `N(T)`, `N_0(T)`, `τ_k = 2π(k−11/8)/W((k−11/8)/e)`; observación numérica: `|γ_k−τ_k| ≤ 0.69` y `|G−A|(½+iτ_k) ∈ [0.054, 0.105]` para `k≤6` (`tauk_check.py`).
4. **§18 Conclusiones.** Sin zeta: lo caracterizado y por qué no basta (la inversión vale en todo `(0,1]`; `𝒦^♯` comparte positividad y periodicidad y tiene soluciones en σ=3/4). Con zeta: la condición pasa a ser RH misma; RvM y `τ_k` solo hablan de partes imaginarias. Si G y A se cortan y dónde: sí (`s=−1` sin zeta; impares `≥3` y `≤−3` y, por Hardy, infinitos puntos de `Re s=½`, con zeta); lo no demostrado es que fuera del eje real solo se corten en `Re s=½` (= RH, abierto, no se sabe imposible).
5. **Nombres:** `p^a→p^k` (Jordan), `a_b→θ_b` (Cor. 11.3), `y` añadida a variables reales; `ε`, `c`, `η`, `ρ_k`, `a^♯_n` evitados (`τ`, `σ+2`, sin nombre, `𝔯_k`, `𝔠_n`).

## 3. Fuentes citadas (verificadas en el PDF de LIBRARY TOTAL)

- Titchmarsh–Heath-Brown 1986 (`318_...pdf`): Thm. 2.1/(2.1.1) p. 13; última igualdad de la primera prueba, p. 15 (`∫ y^{−s−1} sin y = −Γ(−s) sin(½sπ)`, −1<σ<0); (2.1.8) p. 16; §3.1 p. 45 (registro previo); §9.2 p. 211 (definición de N(T)); Thm. 9.4 p. 214; §10.2 p. 256 (Hardy).
- Titchmarsh 1939, *Theory of Functions* (`351_...pdf`): §4.41 p. 149 (reflexión de Γ, 1/Γ entera).

## 4. Abierto

- `A ≠ 0` para `0≤σ≤1`, `|t|<9`: sin prueba analítica (solo el certificado asistido).
- Existencia de una solución no real de `G=A` sin zeta: no demostrada en la nota.
- Momentos de la línea 557 en doble precisión; tabla `tab:check` sin cota de cuadratura ni de cola.
- Los 73 ceros de `G` con `Im s > 40` sin certificado de Rouché.

**GitHub:** `vcasana1/papermath`, rama `castor-pollux-I`, carpeta `castor_pollux_I/` (paquete v5; v1–v4 en `previous_versions/`).

## 5. Protocolo

Comprobar el SHA-256 de la v5 antes de reutilizar este estado. Cada versión nueva lleva número nuevo y su `.txt`. No cambiar nada que no se pida. No escribir zeta en el chat salvo que Doktor lo pida.
