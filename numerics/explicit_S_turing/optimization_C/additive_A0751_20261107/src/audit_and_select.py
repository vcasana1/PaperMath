"""Verify stored proof hashes, allowing relocation of the repository, and select C."""
from decimal import Decimal
import hashlib
import json
from pathlib import Path

WORK = Path(__file__).resolve().parents[1]
BASE = WORK.parent
REPO = BASE.parents[2]
OLD = BASE / 'slope_optimization_20261107'

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def relocate(p):
    value = str(p)
    if '/numerics/' in value:
        return REPO / 'numerics' / value.split('/numerics/', 1)[1]
    return Path(p)

def main():
    cases = [('baseline', 'baseline_coupled_envelope.json'),
             ('joint_C_m20_repaired', 'm20_envelope.json'),
             ('joint_C_m40_repaired', 'm40_envelope.json')]
    records = []
    for stem, name in cases:
        ep = WORK / 'certificates' / name
        e = json.loads(ep.read_text())
        assert e['certified'] and e['A'] == '0.0751' and e['domain'] == 'T>1'
        assert e['coupled_centres']
        for path, digest in e['hashes'].items():
            assert sha(relocate(path)) == digest, path
        p = WORK / 'candidates' / (stem + '.json')
        kernel = json.loads(p.with_name(stem + '_geometry_kernel.json').read_text())
        costs = json.loads(p.with_name(stem + '_geometry_costs.json').read_text())
        ap = p.with_name(stem + '_arithmetic_coupled_binned_N1000000.json')
        ar = json.loads(ap.read_text())
        for item in [kernel, costs, ar]:
            assert item['certified'] and item['input_sha256'] == sha(p)
        assert kernel['code_sha256'] == sha(BASE / 'src/certify_geometry_kernel_fast.py')
        assert costs['code_sha256'] == sha(OLD / 'src/certify_geometry_costs_slope.py')
        assert ar['code_sha256'] == sha(BASE / 'src/certify_arithmetic_coupled_fast.py')
        assert ar['centre_mode'] == 'joint_prime_phase'
        pl = BASE / 'certificates/geometry_PL_inputs_subweyl.json'
        assert costs['PL_certificate_sha256'] == sha(pl)
        assert json.loads(pl.read_text())['certified']
        records.append(dict(candidate=str(p.relative_to(WORK)), envelope=str(ep.relative_to(WORK)),
                            A=e['A'], C=e['C_upper'], A_total_upper=e['A_total_upper'],
                            input_sha256=sha(p), status='PASS'))
    best = min(records, key=lambda x: Decimal(x['C']))
    original = json.loads((OLD / 'certificates/A0.0751_envelope.json').read_text())
    assert original['A'] == '0.0751'
    gain = Decimal(original['C_upper']) - Decimal(best['C'])
    assert gain > 0
    result = dict(status='PASS', A='0.0751', C_new=best['C'], C_previous=original['C_upper'],
                  additive_gain=str(gain), domain='T>1', conditional_on_RH=False,
                  convention='right continuous at zeros; also left and midpoint values',
                  selected=best['candidate'], envelope=best['envelope'],
                  input_sha256=best['input_sha256'], global_optimality_proved=False,
                  execution='local Mac', proof_stages=['global kernel', 'harmonic costs',
                  'coupled arithmetic with infinite tail', 'uniform envelope'], candidates=records)
    (WORK / 'FINAL_RESULT.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    return result

if __name__ == '__main__':
    main()
