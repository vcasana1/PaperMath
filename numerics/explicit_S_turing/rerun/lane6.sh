#!/bin/bash
# Lane 6: full rerun of every certificate with the final programs (provenance lines, ball with radius, 20-digit enclosure).
# Usage: lane6.sh <items...>  where an item is  K:<line> (kernel), H (hybrid), Z:<line> (C_zeta), E:<line> (elementary N and S)
cd /home/claude/papermath/numerics/explicit_S_turing/family
for it in "$@"; do
  case $it in
    K:*) D=${it#K:}; nice -n 5 python3 ../hybrid_asymptotic/certify_hybrid.py $D/sol.json 100 > $D/cert_kernel.txt.new 2>&1
         grep -q "all certified" $D/cert_kernel.txt.new || nice -n 5 python3 ../hybrid_asymptotic/certify_hybrid.py $D/sol.json 2000 > $D/cert_kernel.txt.new 2>&1;;
    H)   (cd ../hybrid_asymptotic && nice -n 5 python3 certify_hybrid.py hyb_m10_P.json 40 > cert_m10P.txt.new 2>&1);;
    Z:*) D=${it#Z:}; nice -n 5 python3 cz_gen_pp.py $D/sol.json 1e8 1000 > $D/cert_czeta_pp.txt.new 2>&1;;
    E:*) D=${it#E:}; A1=$(python3 -c "import json;print(json.load(open('$D/summary_pp.json'))['A1'])")
         nice -n 5 python3 elem_gen.py $D/sol.json $A1 10000 N > $D/cert_elem.txt.new 2>&1
         nice -n 5 python3 elem_gen.py $D/sol.json $A1 10000 S > $D/cert_elem_S.txt.new 2>&1;;
  esac
done
echo LANE6_DONE "$@"
