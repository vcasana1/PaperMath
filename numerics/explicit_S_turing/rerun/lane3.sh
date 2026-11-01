#!/bin/bash
# Lane 3 (after lane 1): the two exploratory LP values quoted in the article (Bourgain profile, and e_P without margin),
# then the certification of the new hybrid solution.
cd /home/claude/papermath/numerics/explicit_S_turing/rerun
while ! grep -q LANE1_DONE lane1.log; do sleep 30; done
cd ../hybrid_asymptotic
[ -e expl_m10_d0.90_B_eta0.json ] || PROF=B nice -n 5 python3 explore_discs.py 10 0.9 0 > explore_B.log 2>&1
[ -e expl_m10_d0.90_P_eta0.json ] || PROF=P nice -n 5 python3 explore_discs.py 10 0.9 0 > explore_P0.log 2>&1
grep -q "all certified" cert_P_eta0.001.txt 2>/dev/null || nice -n 5 python3 certify_hybrid.py expl_m10_d0.90_P_eta0.001.json 40 > cert_P_eta0.001.txt 2>&1
echo LANE3_DONE
