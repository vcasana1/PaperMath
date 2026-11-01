#!/bin/bash
# Lane 4: hybrid LP with the refined violation search (fine linear grid + local maximisation), then certification;
# then the two exploratory values (Bourgain profile; e_P without margin) with the same program.
cd /home/claude/papermath/numerics/explicit_S_turing/hybrid_asymptotic
mkdir -p attic/lp_before_refinement && mv -f expl_m10_d0.90_P_eta0.001.json expl_m10_d0.90_B_eta0.json expl_m10_d0.90_P_eta0.json explore_P.log explore_B.log explore_P0.log cert_P_eta0.001.txt attic/lp_before_refinement/ 2>/dev/null
PROF=P nice -n 5 python3 explore_discs.py 10 0.9 0.001 > explore_P.log 2>&1
nice -n 5 python3 certify_hybrid.py expl_m10_d0.90_P_eta0.001.json 40 > cert_P_eta0.001.txt 2>&1
echo CERT_DONE
PROF=B nice -n 5 python3 explore_discs.py 10 0.9 0 > explore_B.log 2>&1
PROF=P nice -n 5 python3 explore_discs.py 10 0.9 0 > explore_P0.log 2>&1
echo LANE4_DONE
