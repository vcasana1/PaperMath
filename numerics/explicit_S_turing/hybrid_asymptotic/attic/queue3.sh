#!/bin/bash
cd /home/claude/papermath/numerics/explicit_S_turing/hybrid_asymptotic
while pgrep -f queue2.sh >/dev/null; do sleep 20; done
push() { cd /home/claude/papermath && git add -A numerics && git commit -qm "hybrid_asymptotic: $1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015QYJrnTANhbh1zYK1UxFtw" && git push -q origin explicit-S-turing; cd - >/dev/null; }
PROF=W python3 explore_discs.py 10 0.9 vwide >> queue3.log 2>&1; push "Weyl-profile hybrid test"
PROF=C python3 explore_discs.py 10 0.9 vwide >> queue3.log 2>&1; push "convexity-profile hybrid test"
PROF=T python3 explore_discs.py 10 0.9 vwide 0.001 >> queue3.log 2>&1; push "TTY m=10 eta=0.001 solution for certification"
echo QUEUE3_DONE >> queue3.log; push "queue3 done"
