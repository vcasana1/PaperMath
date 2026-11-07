"""Re-execute a uniform slope certificate using exact saved coefficients.
Search programs and floating-point feasibility checks are not proof inputs.
Run from any working directory with the proof environment's Python.
"""
import argparse
import datetime
import json
import shutil
import subprocess
import sys
from pathlib import Path

WORK = Path(__file__).resolve().parents[1]
BASE = WORK.parent
CASES = {
    '0.0751': ('slope_m20_repaired', False, 10**6, 1000, '23.08071071'),
    '0.0758': ('slope_m10_repaired', False, 10**6, 1000, '16.46762913'),
    '0.0828': ('A0830_repaired', True, 10**8, 10000, '3.242277741'),
    '0.0830': ('A0830_repaired', True, 10**8, 10000, '3.151694782'),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--slope', choices=CASES, default='0.0751')
    parser.add_argument('--dest', type=Path)
    args = parser.parse_args()
    stem, coupled, n0, p0, expected = CASES[args.slope]
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    dest = (args.dest or WORK / 'reproduction' / stamp / ('A' + args.slope)).resolve()
    dest.mkdir(parents=True, exist_ok=False)
    sol = dest / 'solution.json'
    shutil.copyfile(WORK / 'candidates' / (stem + '.json'), sol)
    commands = [
        ('kernel', [BASE / 'src/certify_geometry_kernel_fast.py', sol]),
        ('costs', [WORK / 'src/certify_geometry_costs_slope.py', sol]),
        ('arithmetic', [BASE / 'src' / ('certify_arithmetic_coupled_fast.py' if coupled else 'certify_arithmetic_binned.py'), sol,
                        '--N', n0, '--P0', p0, '--step', '0.02']),
    ]
    arithmetic = sol.with_name('solution_arithmetic_' + ('coupled_binned' if coupled else 'binned') + '_N' + str(n0) + '.json')
    commands.append(('envelope', [WORK / 'src/certify_geometry_envelope_slope.py', sol, arithmetic,
                                 '--slope', args.slope, '--Lswitch', 'auto',
                                 '--low', BASE / 'inputs/low_L60.json',
                                 '--low-arithmetic', BASE / 'inputs/low_L60_arithmetic_N1000000.json',
                                 '--low-elementary', BASE / 'inputs/low_L60_elemS.json']))
    for label, command in commands:
        with (dest / (label + '.log')).open('w') as stream:
            subprocess.run([sys.executable, *map(str, command)], check=True, cwd=BASE, stdout=stream, stderr=subprocess.STDOUT)
        print(label, 'PASS', flush=True)
    envelope = sol.with_name('solution_' + ('joint_geometry_envelope' if coupled else 'geometry_envelope') + '.json')
    result = json.loads(envelope.read_text())
    assert result['certified'] and result['A'] == args.slope
    assert result['C_upper'] == expected, (result['C_upper'], expected)
    status = dict(complete=True, slope=args.slope, C_upper=expected, domain='T>1',
                  expected_C_reproduced=True, envelope=str(envelope))
    (dest / 'reproduction_status.json').write_text(json.dumps(status, indent=2))
    print(json.dumps(status, indent=2), flush=True)


if __name__ == '__main__':
    main()
