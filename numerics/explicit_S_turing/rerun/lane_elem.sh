#!/bin/bash
# Elementary part (modes N and S) for the lines given as arguments; A1 taken from the existing summary_pp.json.
cd /home/claude/papermath/numerics/explicit_S_turing/family
for D in "$@"; do
  A1=$(python3 -c "import json;print(json.load(open('$D/summary_pp.json'))['A1'])")
  grep -q "SUP over" $D/cert_elem.txt.new 2>/dev/null || nice -n 5 python3 elem_gen.py $D/sol.json $A1 10000 N > $D/cert_elem.txt.new 2>&1
  grep -q "SUP over" $D/cert_elem_S.txt.new 2>/dev/null || nice -n 5 python3 elem_gen.py $D/sol.json $A1 10000 S > $D/cert_elem_S.txt.new 2>&1
done
echo ELEM_DONE "$@"
