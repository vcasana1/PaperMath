#!/bin/bash
cd /home/claude/papermath/numerics/explicit_S_turing/hybrid_asymptotic
push() { cd /home/claude/papermath && git add -A numerics && git commit -qm "hybrid_asymptotic: $1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015QYJrnTANhbh1zYK1UxFtw" && git push -q origin explicit-S-turing; cd - >/dev/null; }
PROF=T python3 explore_discs.py 20 0.9 vwide >> queue2.log 2>&1; push "m=20 vwide ANTEDB profile run"
PROF=T python3 explore_basis.py 10 0.9 tsmall vwide >> queue2.log 2>&1; push "m=10 t-translate basis run"
echo QUEUE2_DONE >> queue2.log; push "queue2 done"
