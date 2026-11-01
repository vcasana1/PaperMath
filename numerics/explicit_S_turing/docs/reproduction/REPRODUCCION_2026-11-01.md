# Reproducción independiente de casanya_turing_jensen_v9 — 2026-11-01

Estado global: **REPRODUCCIÓN CONFORME — 25/25; SEIS RECTAS CONFORMES**. Certificados reproducidos: **25/25**.
Inicio: 2026-11-01T15:09:12.340688+01:00. Última actualización: 2026-11-01T16:28:03.558119+01:00.

Repositorio: https://github.com/vcasana1/PaperMath/tree/7c28834103e7c1e2f7d9cd6879b4febe09dbe1f3/numerics/explicit_S_turing
Rama: `explicit-S-turing`. Commit exacto: `7c28834103e7c1e2f7d9cd6879b4febe09dbe1f3`.
Clon independiente: `/Users/vcasana/PaperMath-repro`. El clon no existía antes de esta ejecución.
Python: `3.14.5`; `python-flint==0.9.0`; `numpy==2.5.4`.
Sistema: `macOS-26.6.2-arm64-arm-64bit-Mach-O`. Hardware: `[{"_name": "hardware_overview", "activation_lock_status": "activation_lock_enabled", "boot_rom_version": "18000.161.10", "chip_type": "Apple M2", "machine_model": "Mac14,2", "machine_name": "MacBook Air", "model_number": "Z160003M6Y/A", "number_processors": "proc 8:4:4:0", "os_loader_version": "18000.161.10", "physical_memory": "16 GB"}]`.
Entorno: `.venv-repro/`. Precisión de los certificados: 256 bits, comprobada en cada salida.
Comando de cálculo: `./run_certificates.sh 8`, con ocho procesos. El ejecutable python3 del PATH registra tiempos y ejecuta el Python del entorno; no modifica los programas de certificación.
Los 25 certificados y 38 archivos adicionales del ZIP adjunto coinciden byte a byte con el commit; el TEX adjunto y el ZIP completo también coinciden. CRC del ZIP correcto.
Cada certificado se compara íntegramente tras excluir solamente la línea de versión de Python y los tiempos. Esto incluye cotas, inclusiones, radios, límites, cuentas de cajas/intervalos y procedencia SHA-256.
Los SHA-256 completos de salida pueden cambiar por la versión de Python y los tiempos; se conservan ambos hashes y el diff completo. Los hashes de datos y programas deben coincidir exactamente.
La reproducción verifica estos cálculos finitos y las constantes derivadas; no constituye una nueva evaluación de todas las demostraciones analíticas del manuscrito.

| Certificado | Veredicto | Cota | Cajas (+/−/cola) o intervalos | Tiempo publicado (s) | Tiempo certificado Mac (s) | Pared Mac (s) | Diferencias matemáticas |
|---|---|---|---|---:|---:|---:|---|
| `family/line_L5/cert_kernel.txt` | REPRODUCIDO | 0.201756550427 | 10255/4207/2 | 1 | 2 | 2.665 | ninguna |
| `family/line_L5/cert_czeta_pp.txt` | REPRODUCIDO | 0.703600014465 | — | 52 | 101 | 101.552 | ninguna |
| `family/line_L5/cert_elem.txt` | REPRODUCIDO | 0.665364397774 | 9215 | 60 | 115 | 114.804 | ninguna |
| `family/line_L5/cert_elem_S.txt` | REPRODUCIDO | 0.139490893363 | 9215 | 61 | 116 | 116.487 | ninguna |
| `family/line_L20/cert_kernel.txt` | REPRODUCIDO | 0.108221935485 | 473575/279773/1022 | 46 | 119 | 118.910 | ninguna |
| `family/line_L20/cert_czeta_pp.txt` | REPRODUCIDO | 1.46807533663 | — | 53 | 90 | 90.619 | ninguna |
| `family/line_L20/cert_elem.txt` | REPRODUCIDO | 0.702070709399 | 9215 | 61 | 113 | 112.714 | ninguna |
| `family/line_L20/cert_elem_S.txt` | REPRODUCIDO | -0.182786494342 | 9215 | 62 | 116 | 116.113 | ninguna |
| `family/line_L60/cert_kernel.txt` | REPRODUCIDO | 0.0947215742364 | 1441685/483889/4434 | 109 | 249 | 249.210 | ninguna |
| `family/line_L60/cert_czeta_pp.txt` | REPRODUCIDO | 2.10426948726 | — | 53 | 89 | 89.471 | ninguna |
| `family/line_L60/cert_elem.txt` | REPRODUCIDO | 0.728941557753 | 9215 | 61 | 116 | 116.465 | ninguna |
| `family/line_L60/cert_elem_S.txt` | REPRODUCIDO | -0.158475758991 | 9215 | 62 | 114 | 114.431 | ninguna |
| `family/line_L150/cert_kernel.txt` | REPRODUCIDO | 0.0934806284361 | 1658655/353921/3198 | 121 | 266 | 266.639 | ninguna |
| `family/line_L150/cert_czeta_pp.txt` | REPRODUCIDO | 2.25578345555 | — | 53 | 89 | 89.292 | ninguna |
| `family/line_L150/cert_elem.txt` | REPRODUCIDO | 0.730316846936 | 9215 | 61 | 117 | 117.467 | ninguna |
| `family/line_L150/cert_elem_S.txt` | REPRODUCIDO | -0.157576348369 | 9215 | 62 | 120 | 119.682 | ninguna |
| `family/line_C400/cert_kernel.txt` | REPRODUCIDO | 0.0839860184067 | 11835193/9801985/4194302 | 2319 | 3829 | 3829.130 | ninguna |
| `family/line_C400/cert_czeta_pp.txt` | REPRODUCIDO | 4.46374162170 | — | 81 | 139 | 139.345 | ninguna |
| `family/line_C400/cert_elem.txt` | REPRODUCIDO | 0.737565506071 | 9215 | 79 | 142 | 142.252 | ninguna |
| `family/line_C400/cert_elem_S.txt` | REPRODUCIDO | -0.145826731639 | 9215 | 81 | 144 | 144.098 | ninguna |
| `family/line_D6000/cert_kernel.txt` | REPRODUCIDO | 0.0838141706021 | 14760921/15866017/4194302 | 3123 | 4728 | 4728.304 | ninguna |
| `family/line_D6000/cert_czeta_pp.txt` | REPRODUCIDO | 4.58951034745 | — | 80 | 138 | 138.509 | ninguna |
| `family/line_D6000/cert_elem.txt` | REPRODUCIDO | 0.735737525685 | 9215 | 80 | 125 | 125.490 | ninguna |
| `family/line_D6000/cert_elem_S.txt` | REPRODUCIDO | -0.146410366017 | 9215 | 80 | 128 | 128.138 | ninguna |
| `hybrid_asymptotic/cert_m10P.txt` | REPRODUCIDO | 0.0748596142711 | 2028149/2294869/277098 | 838 | 1531 | 1531.372 | ninguna |

## Constantes de las seis rectas

| Recta | A1 publicado / reproducido | A3_N publicado / reproducido | A3_S publicado / reproducido | Veredicto |
|---|---|---|---|---|
| L5 | 0.20176 / 0.20176 | 1.369 / 1.369 | 0.844 / 0.844 | REPRODUCIDO |
| L20 | 0.10823 / 0.10823 | 2.171 / 2.171 | 1.286 / 1.286 | REPRODUCIDO |
| L60 | 0.09473 / 0.09473 | 2.834 / 2.834 | 1.946 / 1.946 | REPRODUCIDO |
| L150 | 0.09349 / 0.09349 | 2.987 / 2.987 | 2.099 / 2.099 | REPRODUCIDO |
| C400 | 0.08399 / 0.08399 | 5.202 / 5.202 | 4.318 / 4.318 | REPRODUCIDO |
| D6000 | 0.08382 / 0.08382 | 5.326 / 5.326 | 4.444 / 4.444 | REPRODUCIDO |

## Hashes SHA-256 de las salidas

| Certificado | Publicado | Reproducido | Contenido normalizado idéntico |
|---|---|---|---|
| `family/line_L5/cert_kernel.txt` | `0aa4e3454c21e45890c073997d31dc7b4676a2298f24f9e094560f54b42d2dd2` | `b451bc06aa34d2efee0cad187aabf077d72c455144d96639fea78df45a54b192` | True |
| `family/line_L5/cert_czeta_pp.txt` | `2f7dfce74ed4a0080c768ef7b37aedde3cdaf57c509dbc7f9fb8afab2f077cc9` | `12a5ad64c347c49d8114256911a52b90c47d5ef9e7b63d8fd271e2a4ff0dc844` | True |
| `family/line_L5/cert_elem.txt` | `463d78e817b5b64280a906b2836df5c3c96cd6867d0ca04dffca489ccfea991a` | `b1d1c2259a67fcef530115bd98a0a7a269d59e17c7dab9545bbde0d6f2527da5` | True |
| `family/line_L5/cert_elem_S.txt` | `2dd98252c5cb8111d95d6178f8cc16c6152aef88db795ff023003333df477526` | `da7cba222e4c1bbee0dc80d16a7b4eb57f681b05599f33bc45ce64fb6cc6a7c1` | True |
| `family/line_L20/cert_kernel.txt` | `3d433857f9e1fa8fd74d04a708a1a053a960468f83d7d5866f4de818487687ac` | `40432eded0ce54243d064beaac9315d0e8bb137d18860cbbbb28209c7fde4aa0` | True |
| `family/line_L20/cert_czeta_pp.txt` | `7ee75c14a18d3041585f44928853612e2d41268e992e012c74562777aa4542d7` | `24bab6d1a4f4a3be76b1a4d1c8f895516356ba816cea473ec6375923b5f4477e` | True |
| `family/line_L20/cert_elem.txt` | `5a7d1c6cccef3e62671969cd22ec19f0f9e7d0caa22cad902fa1e5439540db50` | `6151cc61ddf425734cf0981f9d7c713ea06bccb0a468cde14398d647584c758b` | True |
| `family/line_L20/cert_elem_S.txt` | `c3a16670531ba4e0245973b716b0bc4bced299d777e02834c7ea44b404212a6b` | `65a07fdfa2624243667da71823a5481d80a0aa15379117e7cd762b6eee5f74e8` | True |
| `family/line_L60/cert_kernel.txt` | `1131bfbccc166097a95215503da3d4d2171fe6a7470d3d4c03b69b1f683f4291` | `5e7bcf1699313e86ab1b887a44f8fb39cd229e20286ba791c8ab913dc7ef223a` | True |
| `family/line_L60/cert_czeta_pp.txt` | `4f7f2faf409f498d54ae5b34628594f2cceb15700b412e0ad2bd4dedc3e4bf04` | `90ad10b14cd11e7c263c4fa2ac8e76439d9c964e1914eb03c838fd1f9f420f35` | True |
| `family/line_L60/cert_elem.txt` | `be876133051603078156fae2179cbf541400a642a8ce394988edd4de334d72d9` | `cdf5905866ab6324f3579e60eb96c055c9af328876a05ce5a76c62d5bcc1d119` | True |
| `family/line_L60/cert_elem_S.txt` | `4f3809f8246abacc81ad010e4c94df8ce7e144aeaf8d7e963abf27a70b648a5c` | `93fea97b2752730c5d8214291ee583ec5b603b0a00f4a6c26e36430817721248` | True |
| `family/line_L150/cert_kernel.txt` | `da13fae17c95af5615c098bd0a033372d9b0a47aa81e0252749eb58edd839c71` | `f8d7c7af3e3a51902e70dc1c2e6d90d7375b7919134879e1054228eb29170690` | True |
| `family/line_L150/cert_czeta_pp.txt` | `e6ee37f46b510567289f251ff9eaeb4ba26a31b714c3f2fc09079003f854cbf9` | `dcac53c72bd9511963ba3c6d7461cdb5afd24617b0199988376fb9f7c8ac1dad` | True |
| `family/line_L150/cert_elem.txt` | `d1dc7021f3241637a12dc24b452728b9d5636b99bf0fc56c5b66156bda147e8d` | `35fe6896532fd5ebc96e5a0f8118d2795d8372fee9b129cc0f8fe5b97ced169d` | True |
| `family/line_L150/cert_elem_S.txt` | `9397f0df4537396719c62000ed570c13cac842e4fcba8e53442b65dc375b2072` | `a3401ce1c26539fb26cbecfea2c363d55e53538f230f0433bad42be090216844` | True |
| `family/line_C400/cert_kernel.txt` | `126e798dcb28ed9db9764779fcb353a46dbac2f2c05388f1add18abdb4558012` | `170899035aa56559a313ca8b56d7b2d7ba7124f8eda315784ce3b773184a89aa` | True |
| `family/line_C400/cert_czeta_pp.txt` | `9b99211b3b7784a87975d390a678e21ee244bf58bd12741c1e4a8ca9f6234a94` | `7d2932ee1ba4d5e02e22f7b7bd329188e3957960b20d6f8c5162bf9a46276a01` | True |
| `family/line_C400/cert_elem.txt` | `65424e2222964bec0c2a0f3e39eecc6d141d6b3b1fb8242aebe24670f8375030` | `14b3fc4d847d1969bc07d84b074501ae4ff300f055353fc62880976752303ddf` | True |
| `family/line_C400/cert_elem_S.txt` | `9e29a245ee39c584599ee89cc76d257c5d78bdba7084dee1a32307d6bbd2ccb9` | `6c5bdcb006509bc727c76bad208737a6fd15c0d209ce5defe30d8592f7abf7a4` | True |
| `family/line_D6000/cert_kernel.txt` | `6f7df4922fe6d15d88f45f0d1759757291ea4bfaafe39113596630dbe1cb711e` | `027bea29811d2a812c3a7dc1b8cfd47587445df17b4cc95af463f2f8a4df6b10` | True |
| `family/line_D6000/cert_czeta_pp.txt` | `a6c3d5ac8e2e2aca71cfb1f80ab27ddc7aee086bc3303ee7e7c8f01a6c1d5046` | `5af54a436b4e8797f77ac094219ddebcfd55bd7b8a8db9a1b4c7a3288773034e` | True |
| `family/line_D6000/cert_elem.txt` | `8db067289535571281944b67bedf936e64f214f17f7da0507d48ac7258a1fcf2` | `b84b284e536d21e36d8342f24839248e284641d2bd5569b201c183d2d80366ae` | True |
| `family/line_D6000/cert_elem_S.txt` | `0d99995fdc43fb3e5070068fcfe994b69fbc10ad38712387d8f2911269d39bcc` | `a29456b2726b83f9220e0faa0caf3753befe37b602653e4c88577023b94d061c` | True |
| `hybrid_asymptotic/cert_m10P.txt` | `bc8835a433693095bbf0f82693f677eca83b3f0770779eb44c70bfe776550756` | `640bd247f8a39445f1a254fa67214c13e77ba7fcebcf9c996a98db6e92745c46` | True |

## Evidencia y adaptación local

Los certificados publicados, datos, resúmenes y programas previos se conservan en `repro_evidence_2026-11-01/baseline/`, con manifiesto SHA-256; los resultados independientes se conservan en `reproduced/`.
Metadatos, versiones, hashes de las fuentes adjuntas, tiempos por invocación, verificaciones y diferencias están en `repro_evidence_2026-11-01/`.
El `finalize.py` publicado usa `/home/claude/papermath/.../family/`; la única adaptación prevista es sustituirla por la ruta al directorio family de este clon. Se conserva el original y el diff. No se ejecuta ningún generador del manuscrito.
Estado de finalización: {'returncode': 0, 'seconds': 0.06262620800407603, 'cwd': '/Users/vcasana/PaperMath-repro/numerics/explicit_S_turing', 'path_only_adaptation': True}. Tiempo transcurrido total: 4731.134 s.
No se hacen commits ni se crea una versión v10.

## Integridad final

{"tracked_numerics_files": 803, "changed_in_reproduction_clone": ["rerun/finalize.py", "hybrid_asymptotic/cert_m10P.txt", "family/line_L60/cert_elem_S.txt", "family/line_L60/cert_elem.txt", "family/line_L60/cert_kernel.txt", "family/line_L60/cert_czeta_pp.txt", "family/line_C400/cert_elem_S.txt", "family/line_C400/cert_elem.txt", "family/line_C400/cert_kernel.txt", "family/line_C400/cert_czeta_pp.txt", "family/line_L20/cert_elem_S.txt", "family/line_L20/cert_elem.txt", "family/line_L20/cert_kernel.txt", "family/line_L20/cert_czeta_pp.txt", "family/line_D6000/cert_elem_S.txt", "family/line_D6000/cert_elem.txt", "family/line_D6000/cert_kernel.txt", "family/line_D6000/cert_czeta_pp.txt", "family/line_L150/cert_elem_S.txt", "family/line_L150/cert_elem.txt", "family/line_L150/cert_kernel.txt", "family/line_L150/cert_czeta_pp.txt", "family/line_L5/cert_elem_S.txt", "family/line_L5/cert_elem.txt", "family/line_L5/cert_kernel.txt", "family/line_L5/cert_czeta_pp.txt"], "all_other_files_unchanged": true, "manuscript_unchanged": true, "supplied_files_unchanged": true, "baseline_sha256_verified": true, "no_commit_created": true}

## Cierre de la reproducción

Inicio: 2026-11-01T15:09:12.340688+01:00. Fin: 2026-11-01T16:28:03.557051+01:00. Duración total: **4731.216 s (78.854 min)**. Los tiempos por certificado son tiempos de pared bajo concurrencia y no deben sumarse como duración total.

**Veredicto global: CONFORME.** Los 25 certificados reproducen todo el contenido numérico publicado; las 76 referencias SHA-256 a datos y programas coinciden. Los 25 hashes de contenido normalizado coinciden; los hashes de los archivos completos difieren por la versión de Python (3.13.18 publicada, 3.14.5 en este Mac) y los tiempos. Los JSON auxiliares y los seis resúmenes coinciden con los publicados.

Las 18 constantes se han vuelto a calcular con intervalos y aritmética Decimal exacta y se han contrastado además con las macros del TEX adjunto; evidencia en `tex_constants_verification.json`. Para A1 se certificó también A1 ≥ c_R1/(2π).

Los 25 bloques de salida de certificados del apéndice del TEX adjunto son byte a byte idénticos a los certificados originales usados como referencia; evidencia en `tex_certificate_listings_verification.json`.

### Inclusiones dirigidas de C

Las inclusiones reproducidas coinciden literalmente con las publicadas.

| Certificado | Inclusión publicada y reproducida |
|---|---|
| `family/line_L5/cert_kernel.txt` | `[0.20175655042691417703, 0.20175655042691417704]` |
| `family/line_L20/cert_kernel.txt` | `[0.10822193548420830107, 0.10822193548420830108]` |
| `family/line_L60/cert_kernel.txt` | `[0.094721574236353990058, 0.094721574236353990059]` |
| `family/line_L150/cert_kernel.txt` | `[0.093480628436037879597, 0.093480628436037879598]` |
| `family/line_C400/cert_kernel.txt` | `[0.083986018406625982801, 0.083986018406625982802]` |
| `family/line_D6000/cert_kernel.txt` | `[0.083814170602092884236, 0.083814170602092884237]` |
| `hybrid_asymptotic/cert_m10P.txt` | `[0.074859614271090718755, 0.074859614271090718756]` |

### Cotas decimales usadas en las seis rectas

Los valores siguientes provienen de los JSON regenerados y coinciden exactamente con los publicados. Las sumas se redondean hacia arriba a tres decimales para obtener A3_N y A3_S.

| Recta | C_zeta superior | Fsup_N superior | Fsup_S superior |
|---|---|---|---|
| L5 | 0.703600014464196 | 0.665364397773905 | 0.139490893362834 |
| L20 | 1.46807533662109 | 0.702070709398509 | -0.182786494342484 |
| L60 | 2.10426948725049 | 0.728941557752270 | -0.158475758991133 |
| L150 | 2.25578345554041 | 0.730316846935794 | -0.157576348369576 |
| C400 | 4.46374162169983 | 0.737565506070646 | -0.145826731639095 |
| D6000 | 4.58951034744730 | 0.735737525684865 | -0.146410366017165 |

`python3 rerun/finalize.py` terminó con código 0 y `finalize ok`, exclusivamente en este clon y con una única adaptación de ruta documentada en `finalize_path.diff`. Después se instaló la salida híbrida según las instrucciones del lanzador. La copia publicada anterior permanece íntegra en `baseline/`; no se han modificado el manuscrito ni los archivos adjuntos, ni creado commits ni v10.

El proceso principal terminó. Se comprobó la ausencia del grupo de cálculo PGID 28245 a las 2026-11-01T16:28:44.700019+01:00; evidencia en `process_absence.json`.

Archivos de entrega: este informe y `REPRODUCCION_2026-11-01_evidencia.zip`, con fuentes conservadas, salidas, diferencias, tiempos, verificaciones y manifiestos SHA-256.
