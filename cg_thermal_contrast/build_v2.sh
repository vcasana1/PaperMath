#!/bin/sh
# Build Cg_Thermal_Contrast_v2.tex from the received v1 and compile it (tips renumbered from the .aux).
set -e
python3 make_v2_from_v1.py
python3 make_v2_stage2.py
for i in 1 2 3; do pdflatex -interaction=nonstopmode -halt-on-error Cg_Thermal_Contrast_v2.tex > build.log 2>&1; done
python3 fix_tips.py Cg_Thermal_Contrast_v2.tex Cg_Thermal_Contrast_v2.aux
for i in 1 2 3; do pdflatex -interaction=nonstopmode -halt-on-error Cg_Thermal_Contrast_v2.tex > build.log 2>&1; done
