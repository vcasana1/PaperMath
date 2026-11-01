#!/bin/bash
cd /home/claude/papermath/numerics/explicit_S_turing/hybrid_asymptotic
while pgrep -f "explore_basis.py 10 0.9 tsmall" >/dev/null; do sleep 20; done
push() { cd /home/claude/papermath && git add -A numerics && git commit -qm "hybrid_asymptotic: $1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015QYJrnTANhbh1zYK1UxFtw" && git push -q origin explicit-S-turing; cd - >/dev/null; }
PROF=E python3 explore_discs.py 10 0.9 vwide >> queue5.log 2>&1; push "explicit-profile (E) hybrid m=10 vwide"
PROF=T python3 explore_discs.py 10 0.9 vwide 0.001 >> queue5.log 2>&1; push "TTY m=10 eta=0.001 solution for certification"
PROF=W python3 explore_discs.py 10 0.9 vwide >> queue5.log 2>&1; push "Weyl-profile hybrid test"
PROF=C python3 explore_discs.py 10 0.9 vwide >> queue5.log 2>&1; push "convexity-profile hybrid test"
echo QUEUE5_DONE >> queue5.log; push "queue5 done"
