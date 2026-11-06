"""Run the preserved v11 elementary verifier and bind its output to its inputs."""
import sys,subprocess,json,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];script=BASE.parent/'family/elem_gen.py'
source=Path(sys.argv[1]);A1=sys.argv[2];T0=sys.argv[3] if len(sys.argv)>3 else '10000'
subprocess.run([sys.executable,str(script),str(source),A1,T0,'S'],check=True)
dest=source.with_name(source.stem+'_elemS.json');r=json.loads(dest.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
r.update(certified=True,input_sha256=sha(source),elementary_code_sha256=sha(script),wrapper_code_sha256=sha(Path(__file__)))
dest.write_text(json.dumps(r,indent=2));print('ELEMENTARY OUTPUT BOUND TO INPUT',r['input_sha256'],flush=True)
