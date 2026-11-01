# Driver: certify one explicit line |N(T) - main(T)| <= A1 log T + A3_N and |S(T)| <= A1 log T + A3_S for all T >= 1.
#   1. certify_hybrid.py (no discs): the kernel inequality f <= U, with T1 = 100 (T1 = 2000 if that run fails);
#   2. cz_gen_pp.py: C_zeta < Czeta_upper  (N0 = 1e8, per-prime phase maximum for p <= 1000);
#   3. elem_gen.py, modes N and S: sup_{T>=1} max(F_u, F_l) < Fsup_upper  (T0 = 1e4);
#   4. A1 = C1 rounded upwards to 5 decimals, A3 = Czeta_upper + Fsup_upper rounded upwards to 3 decimals (exact decimal arithmetic).
# Usage:  python3 certify_line_pp.py <tag> <solution.json>                  (writes line_<tag>/sol.json and the certificates there)
#         python3 certify_line_pp.py <tag> <L*> [sweep*.jsonl pattern]      (picks the best sweep candidate for the target height L*)
import json, sys, os, subprocess, glob
from decimal import Decimal, ROUND_CEILING, localcontext
HERE = os.path.dirname(os.path.abspath(__file__))
def locate(name):   # repository layout (../hybrid_asymptotic/) or flat archive (same folder)
    for p in (os.path.join(HERE, name), os.path.join(HERE, '..', 'hybrid_asymptotic', name)):
        if os.path.exists(p): return p
    raise FileNotFoundError(name)

tag = sys.argv[1]; src = sys.argv[2]; pat = sys.argv[3] if len(sys.argv) > 3 else 'sweep*.jsonl'
if src.endswith('.json'): r = json.load(open(src))
else:
    L = float(src); rs = [json.loads(l) for f in glob.glob(pat) for l in open(f)]
    r = min((x for x in rs if x['Lstar'] == L), key=lambda x: x['val'])
D = 'line_'+tag; os.makedirs(D, exist_ok=True); sol = D+'/sol.json'; json.dump(r, open(sol, 'w'))
A1s = str(Decimal(repr(r['C1'])).quantize(Decimal('0.00001'), rounding=ROUND_CEILING))   # elem_gen.py checks A1 >= C1 exactly
print('candidate', tag, 'd =', r['d'], 'C1 =', r['C1'], 'A3 (estimate) =', r['A3_est'], '-> A1 =', A1s, flush=True)

def run(cmd, log):
    with open(D+'/'+log, 'w') as fh: p = subprocess.run(cmd, stdout=fh, stderr=subprocess.STDOUT)
    out = open(D+'/'+log).read(); lines = out.strip().splitlines(); print(lines[-1] if lines else '(no output)', flush=True)
    return p.returncode, out
rc1, o1 = run(['python3', locate('certify_hybrid.py'), sol, '100'], 'cert_kernel.txt')
if not (rc1 == 0 and 'all certified' in o1): rc1, o1 = run(['python3', locate('certify_hybrid.py'), sol, '2000'], 'cert_kernel.txt')
rc2, o2 = run(['python3', os.path.join(HERE, 'cz_gen_pp.py'), sol, '1e8', '1000'], 'cert_czeta_pp.txt')
rc3, o3 = run(['python3', os.path.join(HERE, 'elem_gen.py'), sol, A1s, '10000', 'N'], 'cert_elem.txt')
rc4, o4 = run(['python3', os.path.join(HERE, 'elem_gen.py'), sol, A1s, '10000', 'S'], 'cert_elem_S.txt')

def finish():
    # the certified upper bounds are decimal strings rounded upwards; add them in exact decimal arithmetic and round upwards
    with localcontext() as dc:
        dc.prec = 60
        cz = Decimal(json.load(open(sol.replace('.json', '_czpp.json')))['Czeta_upper'])
        fN = Decimal(json.load(open(sol.replace('.json', '_elem.json')))['Fsup_upper'])
        fS = Decimal(json.load(open(sol.replace('.json', '_elemS.json')))['Fsup_upper'])
        AN = (cz+fN).quantize(Decimal('0.001'), rounding=ROUND_CEILING); AS = (cz+fS).quantize(Decimal('0.001'), rounding=ROUND_CEILING)
    json.dump({'A1': A1s, 'A3_N': str(AN), 'A3_S': str(AS), 'Czeta_pp_upper': str(cz), 'Fsup_N': str(fN), 'Fsup_S': str(fS),
               'd': r['d'], 'B': r['B'], 'Lstar': r['Lstar']}, open(D+'/summary_pp.json', 'w'), indent=1)
    print('LINE %s CERTIFIED: |N(T)-main(T)| <= %s log T + %s ;  |S(T)| <= %s log T + %s   (T >= 1)' % (tag, A1s, AN, A1s, AS), flush=True)
if rc1 == 0 and 'all certified' in o1 and rc2 == 0 and rc3 == 0 and rc4 == 0: finish()
else: print('LINE %s FAILED' % tag, flush=True); sys.exit(1)
