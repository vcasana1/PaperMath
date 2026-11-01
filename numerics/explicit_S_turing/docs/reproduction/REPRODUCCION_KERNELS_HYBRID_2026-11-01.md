# Reejecución en el Mac de los seis núcleos y el híbrido — 2026-11-01

**Estado global: CONFORME — 7/7 REPRODUCIDOS EN EL MAC. Resultados conformes: 7/7.**

Inicio: 2026-11-01T18:12:47.904196+01:00. Actualización: 2026-11-01T19:24:11.403847+01:00.
Repositorio: https://github.com/vcasana1/PaperMath/tree/34221259c01796003205382a2969f879e272b7ff/numerics/explicit_S_turing
Commit fijado: `34221259c01796003205382a2969f879e272b7ff`; rama `explicit-S-turing`; clon nuevo: `/Users/vcasana/PaperMath-repro-kernels-2026-11-01`.
Se ejecutó `git pull --ff-only` en el clon limpio antes de fijar el commit y lanzar los cálculos. La reproducción anterior permanece conservada.
Comando ejecutado: `./rerun/rerun_kernels_hybrid.sh 4`. Cuatro procesos como máximo, exclusivamente en este Mac.
Python `3.14.5`; `python-flint 0.9.0`; FLINT `3.6.0`; numpy `2.5.4`. Entorno nuevo `.venv-repro/`. Precisión verificada en las siete salidas: 256 bits.
Sistema `macOS-26.6.2-arm64-arm-64bit-Mach-O`. Hardware: `[{"_name": "hardware_overview", "activation_lock_status": "activation_lock_enabled", "boot_rom_version": "18000.161.10", "chip_type": "Apple M2", "machine_model": "Mac14,2", "machine_name": "MacBook Air", "model_number": "Z160003M6Y/A", "number_processors": "proc 8:4:4:0", "os_loader_version": "18000.161.10", "physical_memory": "16 GB"}]`.
El wrapper python3 mide tiempos y ejecuta el Python del entorno. No modifica el lanzador ni los programas de certificación.
Esta ejecución recalcula siete certificados. Los otros dieciocho certificados C_zeta/elementales pertenecen a la reproducción anterior y aquí no se vuelven a ejecutar.
Los cálculos se generan localmente desde las entradas fijadas; no se usan resultados de la ejecución remota para construirlos.

## Criterio de comparación fijado antes del cálculo

El certificador publicado previamente tenía SHA-256 `f4977c8401a8c2c35b1761b9de4d39307f6fe8a65697799b6009b1784724f55e`. El certificador actual tiene `fdfe7462c1b017d4167aa7199a16a82117c74fd1a1fbb0ed5dbcc69b210402a5`. El diff solo cambia comentarios y el AST ejecutable es idéntico (`certifier_comments.diff`).
Se comparan todos los números, cotas, inclusiones, radios y cuentas de cajas. Las únicas diferencias previstas y admitidas son los tiempos, el nuevo hash del certificador por sus comentarios y la línea Python 3.13.18 publicada frente a Python 3.14.5 local.
También se compara con la reproducción anterior de este mismo Mac, que utiliza la misma versión de Python: en esa comparación solo se admiten tiempos y el hash conocido del certificador. Se conservan los diffs completos y todos los hashes originales.
Por ello, la afirmación “idéntico byte a byte salvo time” no se da por supuesta para los certificados publicados antiguos: sus líneas de procedencia contienen el hash anterior y otra versión de Python.
Cualquier diferencia no prevista detiene el grupo de procesos.

## Resultados individuales

| Certificado | Veredicto | Cota C < | Inclusión dirigida | Cajas + / − / cola | Publicado s | Mac anterior s | Mac nuevo s | Pared nueva s | Diferencia matemática |
|---|---|---|---|---|---:|---:|---:|---:|---|
| `family/line_L5/cert_kernel.txt` | CONFORME | 0.201756550427 | `[0.20175655042691417703, 0.20175655042691417704]` | 10255 / 4207 / 2 | 1 | 2 | 2 | 2.094 | ninguna |
| `family/line_L20/cert_kernel.txt` | CONFORME | 0.108221935485 | `[0.10822193548420830107, 0.10822193548420830108]` | 473575 / 279773 / 1022 | 46 | 119 | 83 | 83.196 | ninguna |
| `family/line_L60/cert_kernel.txt` | CONFORME | 0.0947215742364 | `[0.094721574236353990058, 0.094721574236353990059]` | 1441685 / 483889 / 4434 | 109 | 249 | 226 | 226.003 | ninguna |
| `family/line_L150/cert_kernel.txt` | CONFORME | 0.0934806284361 | `[0.093480628436037879597, 0.093480628436037879598]` | 1658655 / 353921 / 3198 | 121 | 266 | 150 | 150.397 | ninguna |
| `family/line_C400/cert_kernel.txt` | CONFORME | 0.0839860184067 | `[0.083986018406625982801, 0.083986018406625982802]` | 11835193 / 9801985 / 4194302 | 2319 | 3829 | 3452 | 3451.832 | ninguna |
| `family/line_D6000/cert_kernel.txt` | CONFORME | 0.0838141706021 | `[0.083814170602092884236, 0.083814170602092884237]` | 14760921 / 15866017 / 4194302 | 3123 | 4728 | 4280 | 4280.547 | ninguna |
| `hybrid_asymptotic/cert_m10P.txt` | CONFORME | 0.0748596142711 | `[0.074859614271090718755, 0.074859614271090718756]` | 2028149 / 2294869 / 277098 | 838 | 1531 | 1445 | 1445.134 | ninguna |

## SHA-256 de los archivos de salida

| Certificado | Publicado original | Nueva salida completa | Contenido numérico normalizado |
|---|---|---|---|
| `family/line_L5/cert_kernel.txt` | `0aa4e3454c21e45890c073997d31dc7b4676a2298f24f9e094560f54b42d2dd2` | `b266442b5eab74e4798b7e969589039180709e14f6af2b5c49b52d4099fba98d` | `6fe10c62cfd4903b6ed39bd3849848d42a4008e71121d5c419f9ac5a532c02e5` |
| `family/line_L20/cert_kernel.txt` | `3d433857f9e1fa8fd74d04a708a1a053a960468f83d7d5866f4de818487687ac` | `26be457c161be4429ca5920e6116f089daf6e9b25ad9381c7c1621cc9aa744cb` | `981032af89c6e04a5cfcd576fc7ac5335e603e832128377c6bec59ba3c309a64` |
| `family/line_L60/cert_kernel.txt` | `1131bfbccc166097a95215503da3d4d2171fe6a7470d3d4c03b69b1f683f4291` | `cb790c5f2ceca05fced5aa61e1c4e6ddbc568a90c8a828c3242b42cee49b4201` | `e0daa4d8a30cfe3505036545a7aa777183707c15d9a4c61b952b5a11b37073a9` |
| `family/line_L150/cert_kernel.txt` | `da13fae17c95af5615c098bd0a033372d9b0a47aa81e0252749eb58edd839c71` | `df8f31b23dbf1042fde235780474fa1fa6c26ead45d3b2295477371c95b309cc` | `164e4d6dd937d7b454b5ef965a0ea6315e4c7699efd6bb0709c5f6df5eff10e0` |
| `family/line_C400/cert_kernel.txt` | `126e798dcb28ed9db9764779fcb353a46dbac2f2c05388f1add18abdb4558012` | `4d56e4f5758dbdcc0cf6ec7b2c102a933dd56a34b050e256215d2b35a542100e` | `673047e77ccf2cb07c37839ed7c58790e77bda7134e64500639046f073f33828` |
| `family/line_D6000/cert_kernel.txt` | `6f7df4922fe6d15d88f45f0d1759757291ea4bfaafe39113596630dbe1cb711e` | `72e0dfe6e7f19a97f8be8cf54cfa0cf0f00bc9f483ce933e1b2dfa1fb2ab08e5` | `151fcf2bf19e1e8dc52ee23aa2a570b14579ad062858bc939b1081478c196cef` |
| `hybrid_asymptotic/cert_m10P.txt` | `bc8835a433693095bbf0f82693f677eca83b3f0770779eb44c70bfe776550756` | `e685d604889d0be0a71bda3ca7272d11bb2e8c211f089543d9b23e27289b577d` | `1b7ee9deea14f3f604f45f33aac0c53ce620956a79ef229508c24fd6b4e03ca8` |

## Constantes de las seis rectas

A1 se recalcula del coeficiente exacto c_R1 con Arb y redondeo dirigido; A3_N y A3_S se vuelven a sumar con Decimal a partir de los JSON C_zeta/elementales conservados. Esto no implica haber recalculado esos dieciocho certificados en esta segunda ejecución.

| Recta | A1 | A3_N | A3_S | Coincide con el resumen fijado |
|---|---|---|---|---|
| L5 | 0.20176 | 1.369 | 0.844 | Sí |
| L20 | 0.10823 | 2.171 | 1.286 | Sí |
| L60 | 0.09473 | 2.834 | 1.946 | Sí |
| L150 | 0.09349 | 2.987 | 2.099 | Sí |
| C400 | 0.08399 | 5.202 | 4.318 | Sí |
| D6000 | 0.08382 | 5.326 | 4.444 | Sí |

## Evidencia e integridad

Las salidas nuevas quedan como `cert_*.txt.new`, conforme al lanzador. Las copias publicadas se conservan intactas; no se instalan resultados ni se hacen commits ni se genera un manuscrito nuevo.
La evidencia conserva las fuentes exactas, siete entradas, referencias publicadas y del Mac anterior, siete salidas nuevas, registros por invocación, hashes antes/después y diferencias completas.
Tiempo de la fase registrada transcurrido: 4283.462 s. Los tiempos de pared individuales corresponden a ejecución concurrente y no deben sumarse como duración global.
La reproducción verifica estos cálculos finitos. No sustituye la evaluación de las demostraciones analíticas del manuscrito.

Fin: 2026-11-01T19:24:11.402934+01:00. Duración registrada: 4283.461 s (71.391 min).

{"tracked_files_checked": 922, "tracked_files_changed": 0, "manuscripts_unchanged": true, "published_certificates_unchanged": true, "previous_delivery_unchanged": true, "commits_created": 0, "new_outputs": 7, "verified_provenance_hash_references": 22}

## Cierre y entrega

**Veredicto global: CONFORME, 7/7.** Las cotas, inclusiones y cuentas de cajas reproducen las referencias publicadas y la ejecución anterior del Mac. Las 22 referencias SHA-256 impresas en las nuevas salidas corresponden exactamente a las entradas y programas del commit fijado.

Inicio: 2026-11-01T18:12:47.904196+01:00. Fin del cálculo y comprobaciones: 2026-11-01T19:24:11.402934+01:00. Duración de la fase registrada: **4283.461 s (71.391 min)**; excluye la clonación e instalación del entorno.

Las diferencias de archivo están clasificadas en los diffs: tiempos; hash del certificador cambiado exclusivamente por comentarios; y versión de Python respecto a la referencia publicada antigua. Frente al Mac anterior, la línea de Python coincide. Ninguna diferencia matemática.

### Comparación con la rama remota al terminar

Esta consulta se hizo después de cerrar y conservar las salidas locales. Ref remoto: `0bacf0326e6585a5ba84fa5fdfe746301328bc7a`.

- `family/line_L5/cert_kernel.txt`: CONFORME con la referencia remota actualizada; solo difieren tiempos y/o la línea de versión de Python.
- `family/line_L20/cert_kernel.txt`: CONFORME con la referencia remota actualizada; solo difieren tiempos y/o la línea de versión de Python.
- `family/line_L60/cert_kernel.txt`: CONFORME con la referencia remota actualizada; solo difieren tiempos y/o la línea de versión de Python.
- `family/line_L150/cert_kernel.txt`: CONFORME con la referencia remota actualizada; solo difieren tiempos y/o la línea de versión de Python.
- `family/line_C400/cert_kernel.txt`: CONFORME con la referencia remota actualizada; solo difieren tiempos y/o la línea de versión de Python.
- `family/line_D6000/cert_kernel.txt`: CONFORME con la referencia remota actualizada; solo difieren tiempos y/o la línea de versión de Python.
- `hybrid_asymptotic/cert_m10P.txt`: CONFORME con la referencia remota actualizada; solo difieren tiempos y/o la línea de versión de Python.

Se verificaron 922 archivos seguidos por Git: todos permanecen byte a byte intactos. Los siete resultados nuevos quedan como `.new`; los certificados publicados y los manuscritos no se han modificado. La reproducción anterior y sus entregables conservan sus hashes. No se han creado commits.

El grupo de procesos 33443 ya no existe, comprobado a las 2026-11-01T19:24:52.698356+01:00.

Entrega: este informe y `REPRODUCCION_KERNELS_HYBRID_2026-11-01_evidencia.zip`. El ZIP contiene fuentes, entradas, las siete salidas nuevas, dos referencias por certificado, diffs, versiones, tiempos y manifiesto SHA-256.

Para el traspaso, los siete resultados nuevos se incluyen también directamente en las rutas `hybrid_asymptotic/cert_m10P.txt.new` y `family/line_*/cert_kernel.txt.new` de la raíz del ZIP. Sus hashes están en `SHA256_CERTIFICADOS_MAC.txt`. Son salidas originales del programa, sin cambiar su línea de Python ni sus tiempos. No se ha ejecutado finalize.py ni se han instalado los certificados.
