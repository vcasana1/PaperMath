#!/bin/bash
# Rerun only the seven certificates that hash certify_hybrid.py: the hybrid and the six kernel inequalities
# (used after a change to certify_hybrid.py; the other 18 certificates do not depend on it).
set -u
cd "$(dirname "$0")/.."
JOBS=${1:-2}
job() {
  case $1 in
    kernel) (cd family && python3 ../hybrid_asymptotic/certify_hybrid.py $2/sol.json 100 > $2/cert_kernel.txt.new 2>&1
             grep -q "all certified" $2/cert_kernel.txt.new || python3 ../hybrid_asymptotic/certify_hybrid.py $2/sol.json 2000 > $2/cert_kernel.txt.new 2>&1);;
    hybrid) (cd hybrid_asymptotic && python3 certify_hybrid.py hyb_m10_P.json 40 > cert_m10P.txt.new 2>&1);;
  esac
  echo "done: $1 $2 $(date +%T)"
}
export -f job
{ echo "kernel line_D6000"; echo "kernel line_C400"; echo "hybrid -"
  for L in line_L150 line_L60 line_L20 line_L5; do echo "kernel $L"; done
} | xargs -P "$JOBS" -L 1 bash -c 'job $0 $1'
echo "all launched jobs finished $(date +%T)"
