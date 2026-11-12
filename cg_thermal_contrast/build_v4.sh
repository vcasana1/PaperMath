#!/bin/sh
# Build Cg_Thermal_Contrast_v4.tex from the received v3 and compile it (tips renumbered from the .aux).
set -e
python3 make_v4_from_v3.py Cg_Thermal_Contrast_v3.tex Cg_Thermal_Contrast_v4.tex
for i in 1 2 3; do pdflatex -interaction=nonstopmode -halt-on-error Cg_Thermal_Contrast_v4.tex > build.log 2>&1; done
python3 fix_tips.py Cg_Thermal_Contrast_v4.tex Cg_Thermal_Contrast_v4.aux
for i in 1 2 3; do pdflatex -interaction=nonstopmode -halt-on-error Cg_Thermal_Contrast_v4.tex > build.log 2>&1; done
