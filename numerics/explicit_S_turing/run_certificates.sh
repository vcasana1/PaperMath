#!/bin/bash
# Run every certificate of the article in parallel (one process per certificate; the 25 certificates are independent).
#   ./run_certificates.sh [JOBS]        JOBS = number of parallel processes (default: number of cores)
# Requirements: python3 with python-flint 0.9.0 and numpy (pip install python-flint==0.9.0 numpy).
# Outputs go to family/line_*/cert_*.txt.new and hybrid_asymptotic/cert_m10P.txt.new; when all have finished,
#   python3 rerun/finalize.py          installs them (cert_*.txt), recomputes summary_pp.json and checks the constants,
#   mv hybrid_asymptotic/cert_m10P.txt.new hybrid_asymptotic/cert_m10P.txt
# Approximate CPU times on a 2-vCPU cloud machine: kernels l5 1 s, l20 45 s, l60 2 min, l150 2 min, l400 38 min, l6000 59 min,
# hybrid 14 min; C_zeta 1-3 min each; elementary part 2-3 min per mode.  Longest jobs are started first.
set -u
cd "$(dirname "$0")"
JOBS=${1:-$( (nproc || sysctl -n hw.ncpu) 2>/dev/null )}
LINES="line_D6000 line_C400 line_L150 line_L60 line_L20 line_L5"
job() {   # one certificate; arguments: kind target
  case $1 in
    kernel) (cd family && python3 ../hybrid_asymptotic/certify_hybrid.py $2/sol.json 100 > $2/cert_kernel.txt.new 2>&1
             grep -q "all certified" $2/cert_kernel.txt.new || python3 ../hybrid_asymptotic/certify_hybrid.py $2/sol.json 2000 > $2/cert_kernel.txt.new 2>&1);;
    hybrid) (cd hybrid_asymptotic && python3 certify_hybrid.py hyb_m10_P.json 40 > cert_m10P.txt.new 2>&1);;
    czeta)  (cd family && python3 cz_gen_pp.py $2/sol.json 1e8 1000 > $2/cert_czeta_pp.txt.new 2>&1);;
    elemN|elemS) (cd family && A1=$(python3 -c "import json;print(json.load(open('$2/summary_pp.json'))['A1'])")
             M=${1#elem}; OUT=$([ $M = N ] && echo cert_elem.txt.new || echo cert_elem_S.txt.new)
             python3 elem_gen.py $2/sol.json $A1 10000 $M > $2/$OUT 2>&1);;
  esac
  echo "done: $1 $2"
}
export -f job
{ echo "kernel line_D6000"; echo "kernel line_C400"; echo "hybrid -"
  for L in $LINES; do echo "czeta $L"; done
  for L in $LINES; do echo "elemN $L"; echo "elemS $L"; done
  for L in line_L150 line_L60 line_L20 line_L5; do echo "kernel $L"; done
} | xargs -P "$JOBS" -L 1 bash -c 'job "$0" "$1"'
echo ALL_CERTIFICATES_DONE
