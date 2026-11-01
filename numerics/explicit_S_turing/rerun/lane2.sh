#!/bin/bash
# Lane 2: short kernel certificates, C_zeta for the six lines, kernel-only optima for the Remark.
cd /home/claude/papermath/numerics/explicit_S_turing/family
for D in line_L5 line_L20 line_L60 line_L150; do
  grep -q "all certified" $D/cert_kernel.txt.new 2>/dev/null || nice -n 5 python3 ../hybrid_asymptotic/certify_hybrid.py $D/sol.json 100 > $D/cert_kernel.txt.new 2>&1
  grep -q "all certified" $D/cert_kernel.txt.new || nice -n 5 python3 ../hybrid_asymptotic/certify_hybrid.py $D/sol.json 2000 > $D/cert_kernel.txt.new 2>&1
done
for D in line_L5 line_L20 line_L60 line_L150 line_C400 line_D6000; do
  grep -q "C_zeta <" $D/cert_czeta_pp.txt.new 2>/dev/null || nice -n 5 python3 cz_gen_pp.py $D/sol.json 1e8 1000 > $D/cert_czeta_pp.txt.new 2>&1
done
cd ../hybrid_asymptotic
[ -e kernel_only.txt ] || { for m in 4 10 20 40; do nice -n 5 python3 kernel_only.py $m 0.7,0.8,0.9; done; for m in 4 10 20; do nice -n 5 python3 kernel_only.py $m 0.7,0.8,0.9 rh; done; } > kernel_only.txt.new 2>&1 && mv kernel_only.txt.new kernel_only.txt
echo LANE2_DONE
