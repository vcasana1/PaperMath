"""Deterministic archive of the frozen delivery and required upstream code."""
import sys,json,hashlib,zipfile
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];EXPLICIT=BASE.parent;REPO=BASE.parents[2]
upstream=['family/opt_line.py','family/elem_gen.py','hybrid_asymptotic/certutil.py','hybrid_asymptotic/lpcommon.py']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
meta=[dict(path='../'+name,sha256=sha(EXPLICIT/name)) for name in upstream]
(BASE/'certificates/upstream_code_sha256.json').write_text(json.dumps(meta,indent=2))
files=sorted(p for p in BASE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and '.venv' not in p.parts and p.name not in ['SHA256SUMS','.DS_Store'])
(BASE/'SHA256SUMS').write_text(''.join(sha(p)+'  '+p.relative_to(BASE).as_posix()+'\n' for p in files))
files.append(BASE/'SHA256SUMS');files.sort()
dest=Path(sys.argv[1]) if len(sys.argv)>1 else REPO.parent/'optimization_C_reproducible_20261106.zip'
prefix='numerics/explicit_S_turing/optimization_C/'
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    def add(name,data):
        item=zipfile.ZipInfo(name,date_time=(2026,11,6,12,0,0));item.compress_type=zipfile.ZIP_DEFLATED;item.external_attr=0o100644<<16
        z.writestr(item,data,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    for p in files:add(prefix+p.relative_to(BASE).as_posix(),p.read_bytes())
    for name in upstream:add('numerics/explicit_S_turing/'+name,(EXPLICIT/name).read_bytes())
    add('LEEME_CERTIFICADO.md',(BASE/'CERTIFICADO.md').read_bytes())
with zipfile.ZipFile(dest) as z:
    assert z.testzip() is None
    for p in files:assert hashlib.sha256(z.read(prefix+p.relative_to(BASE).as_posix())).hexdigest()==sha(p)
    for name in upstream:assert hashlib.sha256(z.read('numerics/explicit_S_turing/'+name)).hexdigest()==sha(EXPLICIT/name)
digest=sha(dest);dest.with_suffix(dest.suffix+'.sha256').write_text(digest+'  '+dest.name+'\n')
print(json.dumps(dict(archive=str(dest),sha256=digest,bytes=dest.stat().st_size,files=len(files)+len(upstream)+1,zip_test='PASS'),indent=2))
