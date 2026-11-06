"""Executed outer search: add local geometric variations without claiming globality."""
import sys,json
from pathlib import Path
from decimal import Decimal
from geometry_jensen import rectangle_cost,circle_cost
if len(sys.argv)>4:
    from geometry_profile_costs import configure
    configure(sys.argv[4])
s=json.loads(Path(sys.argv[1]).read_text());out=[];seen=set();factor=Decimal(sys.argv[3]) if len(sys.argv)>3 else Decimal(1)
def add(g):
    g={k:v for k,v in g.items() if k!='cost'};key=json.dumps(g,sort_keys=True)
    if key in seen:return
    seen.add(key)
    if g['kind']=='rectangle':
        if not (.5<=g['a']<1<g['c']<g['b']<=7 and g['H']>0):return
        g['cost']=rectangle_cost(g['a'],g['b'],g['c'],g['H'])
    else:
        if not (g['c']>1 and g['R']>0 and g['c']-g['R']>=.5):return
        g['cost']=circle_cost(g['c'],g['R'])
    out.append(g)
for g,w in zip(s['geometries'],s['geometry_weights']):
    if float(w)<1e-6:continue
    add(g)
    steps={'a':'.025','b':'.25','c':'.025','H':'.1','v':'.1'} if g['kind']=='rectangle' else {'c':'.025','R':'.025','v':'.1'}
    for key,step in steps.items():
        for sign in [-1,1]:
            h=dict(g);h[key]=float(Decimal(str(g[key]))+sign*factor*Decimal(step));add(h)
    if g['kind']=='rectangle':
        # PL profile breakpoints are natural candidate interfaces.
        anchors=[.5]+[1-k/(2**k-2) for k in range(4,10)]
        for left in sorted(anchors,key=lambda x:abs(x-g['a']))[:2]:
            h=dict(g);h['a']=left;add(h)
        for right in [3.5,6.5]:h=dict(g);h['b']=right;add(h)
        for height in [.75,1.25]:h=dict(g);h['H']=height;add(h)
Path(sys.argv[2]).write_text(json.dumps(out,indent=2));print('geometric neighbors',len(out))
