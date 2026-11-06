#!/usr/bin/env bash
# Compile the self-contained v6; DO NOT regenerate it from body.tex.
set -euo pipefail
cd "$(dirname "$0")"
NAME=casanya_turing_jensen_v6
mkdir -p "build_$NAME"
cp "$NAME"_l.tex "build_$NAME/$NAME"_l.tex
cd "build_$NAME"
for run in 1 2 3; do
  pdflatex -interaction=nonstopmode -halt-on-error \
    -jobname="$NAME" "$NAME"_l.tex > "pass_$run.stdout"
done
if grep -E 'Undefined control sequence|LaTeX Error:|Fatal error occurred' "$NAME.log"; then
  echo "LaTeX error detected" >&2
  exit 1
fi
if grep -E 'There were undefined references|Citation .* undefined' "$NAME.log"; then
  echo "Unresolved references or citations" >&2
  exit 1
fi
cp "$NAME.pdf" "../$NAME.pdf"
echo "PDF generated in docs/zenodo_note"
