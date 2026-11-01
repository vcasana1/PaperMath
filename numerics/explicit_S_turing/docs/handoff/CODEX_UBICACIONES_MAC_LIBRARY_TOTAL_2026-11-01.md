# Instrucciones para Codex — rutas verificadas y alcance (2026-11-01)

## Orden inmediata

**DEJA DE BUSCAR en Descargas los PDF 338–353, el ZIP de importación o índices históricos.** El usuario informa que LIBRARY TOTAL ya está sincronizada entre su Mac y GitHub. Su encargo actual es continuar la investigación matemática de Casaña–Turing–Jensen v9 y ejecutar cálculos con Codex. No repitas por rutina una importación que el usuario ya considera terminada.

### Carpetas y archivos

- **Biblioteca en el Mac:** `/Users/vcasana/Documents/LIBRARY TOTAL/`.
- **Índice único:** `/Users/vcasana/Documents/LIBRARY TOTAL/INDEX.md`.
- **Repo de la biblioteca:** `vcasana1/LIBRARY-TOTAL-28oct2026`, rama `main`, raíz (los PDF numerados están en la raíz, no en `papers/`).
- **Repo de investigación/código:** `vcasana1/PaperMath`, rama `explicit-S-turing`.
- **Código y certificados:** `numerics/explicit_S_turing/` de `PaperMath`.
- **Manuscrito v9 en PaperMath:** `numerics/explicit_S_turing/docs/zenodo_note/casanya_turing_jensen_v9_l.tex`.
- **ZIP de manuscrito y reproducibilidad v9 en PaperMath:** `numerics/explicit_S_turing/docs/zenodo_note/casanya_turing_jensen_v9_zenodo.zip`.
- **Instrucciones matemáticas existentes:** `numerics/explicit_S_turing/docs/handoff/`; ver también `numerics/explicit_S_turing/README.md`.
- **Clon de PaperMath en el Mac:** su ruta local NO consta aquí; averíguala preguntando a `git` y al entorno de Codex, no asumas `/Users/vcasana/Documents/PaperMath`.

### Importación anterior: no volver a ejecutar salvo fallo real

El ZIP de importación original se creó en el entorno aislado de ChatGPT como `/mnt/data/LIBRARY_TOTAL_IMPORT_2026-11-01.zip` (con `papers/338_...pdf` a `papers/352_...pdf`, `MANIFEST.json`, `incorporar_library_total.py` y `evidence/`). **`/mnt/data` NO es una ruta del Mac**. El ZIP no tiene por qué estar en Descargas ni debe ser necesario tras la sincronización. El fichero enviado de Einstein–Marcel Grossmann es de RELATIVIDAD, no la tesis de Grossmann sobre ceros; su copia .duckload estaba incompleta. Un número 353 exige PDF válido, nunca contabilizarlo sin verificar.

### Comprobación mínima sin trabajo redundante

El usuario afirma que Mac y GitHub están iguales; sin embargo, una consulta de GitHub desde este chat el 1/11/2026 seguía mostrando **337 PDF** en `main`. Resuelve la discrepancia con una comprobación rápida, **sin escanear Descargas ni reimportar**:

```bash
LIB="/Users/vcasana/Documents/LIBRARY TOTAL"
test -d "$LIB" || { echo "NO EXISTE $LIB"; exit 1; }
printf 'PDF en Mac: '; find "$LIB" -maxdepth 1 -type f -iname '*.pdf' | wc -l
ls -l "$LIB/INDEX.md"
git -C "$LIB" remote -v
git -C "$LIB" branch --show-current
git -C "$LIB" status --short
git -C "$LIB" rev-parse HEAD
git ls-remote https://github.com/vcasana1/LIBRARY-TOTAL-28oct2026.git refs/heads/main
```

Si LIBRARY TOTAL no es un clon, **no ejecutes** comandos Git que presuponen `.git` ni hagas `git init`; contrasta mediante el repositorio GitHub y hashes reales. Si están 353 PDF en Mac pero 337 en GitHub, informa exactamente de la divergencia antes de modificar nada. Si ya están sincronizados, **cierra esa línea y continúa de inmediato**.

### Trabajo actual

- **ChatGPT:** investigación bibliográfica, lectura VISUAL de los pasajes originales, comprobación de citas y lógica.
- **Codex:** Python, cálculos, optimizaciones, reproducción selectiva y certificación Arb/FLINT, en Mac y entorno virtual cuando estén disponibles; documentación de comandos, hashes y logs.
- La v9 es el documento rector. No mezclar con `casanya_ordinal_primes_v57`.
- **PROHIBIDO** modificar `.tex`, crear v10, generar o recompilar nuevos manuscritos, PDFs o ZIP del paper, sin orden explícita del usuario.
- No reinstales Python innecesariamente; comprueba primero versiones y `venv`. No repitas certificaciones costosas si los hashes y certificados ya permiten validar.
- Deja resultados nuevos en Markdown/JSON/código de investigación separado, no dentro del manuscrito.

**No se trata de reconstruir la biblioteca. Se trata de ampliar las demostraciones y los cálculos de v9.**
