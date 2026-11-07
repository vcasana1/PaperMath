"""Check the complete stored proof chain and its exact file hashes."""
import hashlib
import json
from pathlib import Path

WORK = Path(__file__).resolve().parents[1]
BASE = WORK.parent

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def audit():
    cases = {
        '0.0751': ('slope_m20_repaired', False, '23.08071071'),
        '0.0758': ('slope_m10_repaired', False, '16.46762913'),
        '0.0828': ('A0830_repaired', True, '3.242277741'),
        '0.0830': ('A0830_repaired', True, '3.151694782'),
    }
    records = []
    for a, (stem, coupled, expected) in cases.items():
        ep = WORK / 'certificates' / ('A' + a + '_envelope.json')
        e = json.loads(ep.read_text())
        assert e['certified'] and e['A'] == a and e['C_upper'] == expected
        assert e['domain'] == 'T>1'
        for file, digest in e['hashes'].items():
            assert sha(file) == digest, file
        p = WORK / 'candidates' / (stem + '.json')
        digest = sha(p)
        kernel = json.loads(p.with_name(stem + '_geometry_kernel.json').read_text())
        costs = json.loads(p.with_name(stem + '_geometry_costs.json').read_text())
        n0 = 10**8 if coupled else 10**6
        ap = p.with_name(stem + '_arithmetic_' + ('coupled_binned' if coupled else 'binned') + '_N' + str(n0) + '.json')
        arithmetic = json.loads(ap.read_text())
        for item in [kernel, costs, arithmetic]:
            assert item['certified'] and item['input_sha256'] == digest
        assert kernel['code_sha256'] == sha(BASE / 'src/certify_geometry_kernel_fast.py')
        cost_sources = [BASE / 'src/certify_geometry_costs_pruned.py', WORK / 'src/certify_geometry_costs_slope.py']
        assert costs['code_sha256'] in {sha(q) for q in cost_sources}
        program = 'certify_arithmetic_coupled_fast.py' if coupled else 'certify_arithmetic_binned.py'
        assert arithmetic['code_sha256'] == sha(BASE / 'src' / program)
        pl = BASE / 'certificates/geometry_PL_inputs_subweyl.json'
        assert costs['PL_certificate_sha256'] == sha(pl)
        assert json.loads(pl.read_text())['certified']
        records.append(dict(A=a, C=expected, proof_chain='PASS', envelope=str(ep.relative_to(WORK)),
                            input_sha256=digest, N0=n0, direct_prime_count=arithmetic['prime_count']))
    reproductions = list((WORK / 'reproduction').rglob('reproduction_status.json'))
    assert any((s := json.loads(p.read_text()))['complete'] and s['slope'] == '0.0751' and s['expected_C_reproduced'] for p in reproductions)
    status = dict(status='PASS', domain='T>1', conditional_on_RH=False,
                  strongest_slope='0.0751', strongest_slope_C='23.08071071',
                  strongest_result_fully_reproduced=True, global_optimality_proved=False,
                  cases=records)
    (WORK / 'certificates/proof_chain_status.json').write_text(json.dumps(status, indent=2))
    print(json.dumps(status, indent=2))
    return status

if __name__ == '__main__':
    audit()
