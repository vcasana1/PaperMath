#!/bin/bash
# Lane 5: rerun of the kernel certificates with the final printing of certify_hybrid.py (ball with its radius, 20-digit enclosure).
cd /home/claude/papermath/numerics/explicit_S_turing/family
for D in "$@"; do
  if [ "$D" = hybrid ]; then cd ../hybrid_asymptotic; nice -n 5 python3 certify_hybrid.py hyb_m10_P.json 40 > cert_m10P.txt.new 2>&1; cd ../family; continue; fi
  nice -n 5 python3 ../hybrid_asymptotic/certify_hybrid.py $D/sol.json 100 > $D/cert_kernel.txt.new 2>&1
  grep -q "all certified" $D/cert_kernel.txt.new || nice -n 5 python3 ../hybrid_asymptotic/certify_hybrid.py $D/sol.json 2000 > $D/cert_kernel.txt.new 2>&1
done
echo LANE5_DONE "$@"
