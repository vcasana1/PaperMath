#!/bin/bash
# Lane 1: long kernel certificates (l400, l6000), then the hybrid (LP with the published profile, then certification).
cd /home/claude/papermath/numerics/explicit_S_turing/family
for D in line_D6000 line_C400; do
  grep -q "all certified" $D/cert_kernel.txt.new 2>/dev/null || nice -n 5 python3 ../hybrid_asymptotic/certify_hybrid.py $D/sol.json 100 > $D/cert_kernel.txt.new 2>&1
  grep -q "all certified" $D/cert_kernel.txt.new || nice -n 5 python3 ../hybrid_asymptotic/certify_hybrid.py $D/sol.json 2000 > $D/cert_kernel.txt.new 2>&1
done
cd ../hybrid_asymptotic
[ -e expl_m10_d0.90_P_eta0.001.json ] || PROF=P nice -n 5 python3 explore_discs.py 10 0.9 0.001 > explore_P.log 2>&1
echo LANE1_DONE
