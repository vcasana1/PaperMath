#!/bin/bash
cd /home/claude/papermath/numerics/explicit_S_turing/hybrid_asymptotic
while pgrep -f "queue2.sh|queue3.sh" >/dev/null; do sleep 20; done
push() { cd /home/claude/papermath && git add -A numerics && git commit -qm "hybrid_asymptotic: $1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015QYJrnTANhbh1zYK1UxFtw" && git push -q origin explicit-S-turing; cd - >/dev/null; }
PROF=E python3 explore_discs.py 10 0.9 vwide >> queue4.log 2>&1; push "explicit-profile (E) hybrid m=10 vwide"
echo QUEUE4_DONE >> queue4.log; push "queue4 done"
