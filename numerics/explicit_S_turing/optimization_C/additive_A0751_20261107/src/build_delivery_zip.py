"""Build a portable snapshot with all new work and its local proof dependencies."""
import hashlib
from pathlib import Path
import zipfile

WORK = Path(__file__).resolve().parents[1]
BASE = WORK.parent
REPO = BASE.parents[2]
OUT = REPO / 'certificado_S_A0_0751'


def main():
    files = set()
    directories = [BASE / 'src', WORK, BASE / 'slope_optimization_20261107',
                   BASE / 'certificates/final_geometry_C2_959227629']
    for directory in directories:
        files.update(p for p in directory.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name != '.DS_Store')
    files.update(p for p in (BASE.parent / 'hybrid_asymptotic').iterdir()
                 if p.is_file() and p.suffix in ['.py', '.json', '.md', '.txt'])
    files.update(BASE.glob('*.md'))
    files.add(BASE / 'requirements.txt')
    files.update(p for p in (BASE / 'inputs').glob('low_L60*') if p.is_file())
    for value in ['inputs/empirical_primoss_PP1000_width002.npz', 'inputs/primoss_source.json',
                  'certificates/geometry_PL_inputs_subweyl.json']:
        files.add(BASE / value)
    files.add(BASE.parent / 'docs/zenodo_note/casanya_turing_jensen_v5_l.tex')
    payload = {}
    for path in sorted(files):
        assert path.exists(), path
        relative = path.relative_to(REPO).as_posix()
        payload[relative] = path.read_bytes()
    payload['requirements-lock.txt'] = (OUT / 'requirements-lock.txt').read_bytes()
    payload['LEEME.md'] = b'''# Uniform bound for S(T), slope 0.0751

Certified without RH: |S(T)| <= 0.0751 log(T) + 16.58585760 for every T>1.
Preserve this entire PaperMath directory. The original prime binary is not
needed to reproduce the proof. Numerical search data are not accepted as proof.

Use the Python environment recorded in requirements-lock.txt, then run:

    python numerics/explicit_S_turing/optimization_C/additive_A0751_20261107/src/reproduce_certificate.py --slope 0.0751
    python numerics/explicit_S_turing/optimization_C/additive_A0751_20261107/src/audit_and_select.py

The first command creates a new proof execution directory. The second audits
the stored proof inputs and hashes, translating original absolute paths to
this repository root. Historical output files retain their original paths.

Read RESULTADO_CONSTANTE_ADITIVA.md and FINAL_RESULT.json in
numerics/explicit_S_turing/optimization_C/additive_A0751_20261107/.
The older slope work and original certificates are preserved as history.
The old 0.08382, 2.959227629 pair has a different slope. Do not mix the pairs.
No global optimality or RH proof is claimed.
'''
    # The portable manifest covers the exact archived bytes, including all
    # historical outputs; it is independent of the absolute paths in outputs.
    manifest = ''.join(hashlib.sha256(value).hexdigest() + '  ' + key + '\n'
                       for key, value in sorted(payload.items())).encode()
    payload['SHA256SUMS'] = manifest
    dest = OUT / 'certificado_S_A0_0751.zip'
    with zipfile.ZipFile(dest, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for key, value in sorted(payload.items()):
            archive.writestr('PaperMath/' + key, value)
    with zipfile.ZipFile(dest) as archive:
        assert archive.testzip() is None
        for line in manifest.decode().splitlines():
            digest, relative = line.split('  ', 1)
            assert hashlib.sha256(archive.read('PaperMath/' + relative)).hexdigest() == digest
    digest = hashlib.sha256(dest.read_bytes()).hexdigest()
    (OUT / 'certificado_S_A0_0751.zip.sha256').write_text(digest + '  ' + dest.name + '\n')
    print('ZIP', dest)
    print('files', len(payload), 'bytes', dest.stat().st_size, 'sha256', digest)
    return dest

if __name__ == '__main__':
    main()
