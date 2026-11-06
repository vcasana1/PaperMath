"""Check every delivered SHA-256, without trusting a search program."""
import sys,hashlib
from pathlib import Path
base=Path(__file__).resolve().parents[1];n=0
for line in (base/'SHA256SUMS').read_text().splitlines():
    digest,path=line.split('  ',1);p=base/path
    assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==digest,path
    n+=1
print('SHA-256 VERIFIED',n,'files')
import json
for item in json.loads((base/'certificates/upstream_code_sha256.json').read_text()):
    assert hashlib.sha256((base/item['path']).read_bytes()).hexdigest()==item['sha256'],item['path']
print('UPSTREAM CODE SHA-256 VERIFIED')
