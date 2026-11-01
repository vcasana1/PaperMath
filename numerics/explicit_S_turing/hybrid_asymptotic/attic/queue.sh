#!/bin/bash
# sequential exploration queue (one LP at a time: 7 GB RAM)
cd /home/claude/papermath/numerics/explicit_S_turing/hybrid_asymptotic
while pgrep -f "explore_discs.py 10 0.9 wide" >/dev/null; do sleep 10; done
PROF=B python3 explore_discs.py 10 0.9 vwide >> queue.log 2>&1
PROF=T python3 explore_discs.py 10 0.9 vwide >> queue.log 2>&1
PROF=T python3 explore_basis.py 10 0.9 ext vwide >> queue.log 2>&1
PROF=T python3 explore_discs.py 20 0.9 vwide >> queue.log 2>&1
echo QUEUE_DONE >> queue.log
