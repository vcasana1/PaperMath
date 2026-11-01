# After the rerun lanes: install the new certificates (cert_*.txt.new -> cert_*.txt), recompute summary_pp.json of each
# line exactly as certify_line_pp.finish does (exact decimal arithmetic, rounding upwards), and report every change.
import json, os, shutil, sys
from decimal import Decimal, ROUND_CEILING, localcontext
FAM = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'family') + os.sep   # works from any clone
for tag in ['L5', 'L20', 'L60', 'L150', 'C400', 'D6000']:
    D = FAM+'line_%s/' % tag
    for fn, marker in [('cert_kernel.txt', 'all certified'), ('cert_czeta_pp.txt', 'C_zeta <'), ('cert_elem.txt', 'SUP over'), ('cert_elem_S.txt', 'SUP over')]:
        new = D+fn+'.new'
        assert os.path.exists(new) and marker in open(new).read(), (tag, fn)
        shutil.move(new, D+fn)
    old = json.load(open(D+'summary_pp.json')); sol = D+'sol.json'
    with localcontext() as dc:
        dc.prec = 60
        cz = Decimal(json.load(open(sol.replace('.json', '_czpp.json')))['Czeta_upper'])
        fN = Decimal(json.load(open(sol.replace('.json', '_elem.json')))['Fsup_upper'])
        fS = Decimal(json.load(open(sol.replace('.json', '_elemS.json')))['Fsup_upper'])
        AN = (cz+fN).quantize(Decimal('0.001'), rounding=ROUND_CEILING); AS = (cz+fS).quantize(Decimal('0.001'), rounding=ROUND_CEILING)
    r = json.load(open(sol))
    new = {'A1': old['A1'], 'A3_N': str(AN), 'A3_S': str(AS), 'Czeta_pp_upper': str(cz), 'Fsup_N': str(fN), 'Fsup_S': str(fS), 'd': r['d'], 'B': r['B'], 'Lstar': r['Lstar']}
    for k in ('A1', 'A3_N', 'A3_S', 'Czeta_pp_upper', 'Fsup_N', 'Fsup_S'):
        if old[k] != new[k]: print('%s: %s  %s -> %s' % (tag, k, old[k], new[k]))
    assert new['A3_N'] == old['A3_N'] and new['A3_S'] == old['A3_S'], 'a constant of the theorem changed'
    json.dump(new, open(D+'summary_pp.json', 'w'), indent=1)
    print(tag, 'A1 =', new['A1'], 'A3_N =', new['A3_N'], 'A3_S =', new['A3_S'])
print('finalize ok')
