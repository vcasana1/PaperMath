"""Execute a full proof with a measured local-runtime limit and clean timeout."""
import sys,json,time,subprocess,os,signal,argparse
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('source');ap.add_argument('output');ap.add_argument('--seconds',type=int,default=900);ap.add_argument('--profile',default='pruned_subweyl');args=ap.parse_args();t=time.time();out=Path(args.output);log=BASE/'logs'/('bounded_proof_'+out.stem+'.log')
cmd=[sys.executable,str(BASE/'src/geometry_pipeline.py'),args.source,args.output,'--general','--joint','--profile',args.profile,'--Lswitch','auto']
with log.open('w') as stream:
 child=subprocess.Popen(cmd,cwd=BASE,stdout=stream,stderr=subprocess.STDOUT,start_new_session=True)
 try:code=child.wait(timeout=args.seconds);timed_out=False
 except subprocess.TimeoutExpired:
  os.killpg(child.pid,signal.SIGTERM);child.wait();code=None;timed_out=True
status=dict(complete=code==0,timed_out=timed_out,exit_code=code,seconds=time.time()-t,limit_seconds=args.seconds,source=args.source,output=args.output,log=str(log.relative_to(BASE)))
if status['complete']:
 e=json.loads((BASE/out.with_name(out.stem+'_joint_geometry_envelope.json')).read_text());assert e['certified'];status['C_upper']=e['C_upper']
(BASE/'certificates'/('bounded_proof_'+out.stem+'.json')).write_text(json.dumps(status,indent=2));print(json.dumps(status,indent=2),flush=True)
if not status['complete']:sys.exit(2)
