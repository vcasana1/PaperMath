"""Validate the user's binary against a complete segmented sieve, locally."""
import sys,json,math,time,hashlib
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parents[1]
path=Path(sys.argv[1]);start=time.time();N=10**10;chunk=5000000
assert path.stat().st_size%8==0
a=np.memmap(path,dtype='<u8',mode='r');root=math.isqrt(N)
s=np.ones(root+1,bool);s[:2]=False
for p in range(2,math.isqrt(root)+1):
    if s[p]:s[p*p::p]=False
base=np.flatnonzero(s).tolist();offset=0
for lo in range(2,N+1,chunk):
    hi=min(N,lo+chunk-1);seg=np.ones(hi-lo+1,bool)
    for p in base:
        if p*p>hi:break
        first=max(p*p,((lo+p-1)//p)*p);seg[first-lo::p]=False
    actual=np.flatnonzero(seg).astype(np.uint64)+lo
    assert np.array_equal(a[offset:offset+len(actual)],actual),('prime file mismatch',lo,hi,offset)
    offset+=len(actual)
    if (lo-2)//chunk%200==0:print('validated to',hi,'primes',offset,'seconds',time.time()-start,flush=True)
assert offset==len(a)
h=hashlib.sha256()
with path.open('rb') as f:
    while b:=f.read(16*1024**2):h.update(b)
r=dict(certified_complete=True,path=str(path),dtype='<u8',count=offset,N=N,first=int(a[0]),last=int(a[-1]),sha256=h.hexdigest(),
       method='exact elementwise equality with every prime from a complete segmented sieve through N',seconds=time.time()-start)
(BASE/'inputs/primoss_source.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2),flush=True)
